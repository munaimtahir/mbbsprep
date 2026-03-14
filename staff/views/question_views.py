from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.db.models import Q, Count, Prefetch
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from core.models import Question, Option, Subject, Topic, Tag
from ..forms import QuestionForm, OptionFormSet, BulkQuestionUploadForm
from .user_views import StaffRequiredMixin
import csv
import os
import time


class QuestionListView(StaffRequiredMixin, ListView):
    """List all questions with search and filtering"""
    model = Question
    template_name = 'staff/questions/question_list.html'
    context_object_name = 'questions'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Question.objects.select_related(
            'topic', 'topic__subject'
        ).prefetch_related(
            'tags', 'options'
        ).order_by('-created_at')
        
        # Search functionality
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(question_text__icontains=search_query) |
                Q(topic__name__icontains=search_query) |
                Q(topic__subject__name__icontains=search_query) |
                Q(tags__name__icontains=search_query) |
                Q(explanation__icontains=search_query)
            ).distinct()
        
        # Filter by subject
        subject_id = self.request.GET.get('subject')
        if subject_id:
            queryset = queryset.filter(topic__subject_id=subject_id)
        
        # Filter by topic
        topic_id = self.request.GET.get('topic')
        if topic_id:
            queryset = queryset.filter(topic_id=topic_id)
        
        # Filter by difficulty
        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)
        elif status == 'premium':
            queryset = queryset.filter(is_premium=True)
        elif status == 'free':
            queryset = queryset.filter(is_premium=False)
        
        # Filter by tags
        tag_id = self.request.GET.get('tag')
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add filter options
        context['subjects'] = Subject.objects.filter(is_active=True)
        context['topics'] = Topic.objects.filter(is_active=True).select_related('subject')
        context['tags'] = Tag.objects.filter(is_active=True)
        context['difficulty_choices'] = Question.DIFFICULTY_CHOICES
        
        # Current filter values
        context['current_search'] = self.request.GET.get('search', '')
        context['current_subject'] = self.request.GET.get('subject', '')
        context['current_topic'] = self.request.GET.get('topic', '')
        context['current_difficulty'] = self.request.GET.get('difficulty', '')
        context['current_status'] = self.request.GET.get('status', '')
        context['current_tag'] = self.request.GET.get('tag', '')
        
        # Statistics
        total_questions = Question.objects.count()
        active_questions = Question.objects.filter(is_active=True).count()
        premium_questions = Question.objects.filter(is_premium=True).count()
        
        context['stats'] = {
            'total': total_questions,
            'active': active_questions,
            'inactive': total_questions - active_questions,
            'premium': premium_questions,
            'free': total_questions - premium_questions,
        }
        
        return context


class QuestionCreateView(StaffRequiredMixin, CreateView):
    """Create new question with enhanced form"""
    model = Question
    form_class = QuestionForm
    template_name = 'staff/questions/question_add.html'
    success_url = reverse_lazy('staff:question_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add additional context for the template
        context['subjects'] = Subject.objects.filter(is_active=True)
        context['topics'] = Topic.objects.filter(is_active=True)
        context['tags'] = Tag.objects.filter(is_active=True)
        
        # Initialize empty formset for new questions
        if not self.request.POST:
            context['option_formset'] = OptionFormSet()
        
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        
        # Process options manually since we're using a custom structure
        options_data = self.extract_options_from_post(request.POST)
        
        if form.is_valid() and self.validate_options(options_data):
            return self.form_valid(form, options_data)
        else:
            return self.form_invalid(form)
    
    def extract_options_from_post(self, post_data):
        """Extract option data from POST request"""
        options = []
        correct_answer_index = post_data.get('correct_answer')
        
        # Count how many options were submitted
        option_count = 0
        for key in post_data.keys():
            if key.startswith('option_') and key.endswith('_text'):
                option_count += 1
        
        for i in range(option_count):
            option_text = post_data.get(f'option_{i}_text', '').strip()
            if option_text:  # Only include non-empty options
                options.append({
                    'text': option_text,
                    'is_correct': str(i) == correct_answer_index,
                    'order': i + 1
                })
        
        return options
    
    def validate_options(self, options_data):
        """Validate options data"""
        if len(options_data) < 2:
            return False
        
        correct_count = sum(1 for opt in options_data if opt['is_correct'])
        return correct_count == 1
    
    def form_valid(self, form, options_data):
        """Save the question and its options"""
        try:
            # Save the question
            self.object = form.save()
            
            # Create options
            for option_data in options_data:
                Option.objects.create(
                    question=self.object,
                    option_text=option_data['text'],
                    is_correct=option_data['is_correct'],
                    order=option_data['order']
                )
            
            messages.success(
                self.request, 
                f'✅ MCQ "{self.object.question_text[:50]}..." has been added successfully!'
            )
            return redirect(self.success_url)
            
        except Exception as e:
            messages.error(
                self.request,
                f'❌ Error saving MCQ: {str(e)}'
            )
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            '❌ Please correct the errors below and try again.'
        )
        return super().form_invalid(form)


class QuestionEditView(StaffRequiredMixin, UpdateView):
    """Edit existing question with options"""
    model = Question
    form_class = QuestionForm
    template_name = 'staff/questions/question_edit.html'
    success_url = reverse_lazy('staff:question_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': f'Edit MCQ #{self.object.id}',
            'breadcrumbs': [
                {'title': 'Dashboard', 'url': reverse_lazy('staff:dashboard')},
                {'title': 'MCQs', 'url': reverse_lazy('staff:question_list')},
                {'title': f'Edit MCQ #{self.object.id}', 'url': None}
            ],
            'options': self.object.options.all().order_by('order'),
            'revision_history': getattr(self.object, 'revision_history', [])  # For future implementation
        })
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Handle delete action
        if 'delete_mcq' in request.POST:
            return self.handle_delete()
        
        # Handle reset action
        if 'reset_form' in request.POST:
            messages.info(request, 'ℹ️ Form has been reset to saved values.')
            return redirect('staff:question_edit', pk=self.object.pk)
        
        # Handle normal form submission
        form = self.get_form()
        
        if form.is_valid():
            # Process options data
            options_data = self.extract_options_data(request.POST)
            
            if not options_data:
                form.add_error(None, 'At least 2 options are required.')
                return self.form_invalid(form)
            
            if not self.validate_options(options_data):
                form.add_error(None, 'Exactly one correct answer must be selected.')
                return self.form_invalid(form)
            
            return self.form_valid(form, options_data)
        else:
            return self.form_invalid(form)
    
    def handle_delete(self):
        """Handle MCQ deletion with confirmation"""
        question_text = self.object.question_text[:50]
        question_id = self.object.id
        
        try:
            self.object.delete()
            messages.success(
                self.request,
                f'🗑️ MCQ #{question_id} "{question_text}..." has been deleted successfully.'
            )
            return redirect('staff:question_list')
        except Exception as e:
            messages.error(
                self.request,
                f'❌ Error deleting MCQ: {str(e)}'
            )
            return redirect('staff:question_edit', pk=self.object.pk)
    
    def extract_options_data(self, post_data):
        """Extract options data from POST request"""
        options = []
        correct_answer_index = post_data.get('correct_answer', '')
        
        # Count total options from form data
        option_count = 0
        for key in post_data.keys():
            if key.startswith('option_') and key.endswith('_text'):
                option_count += 1
        
        # Extract each option
        for i in range(option_count):
            option_text = post_data.get(f'option_{i}_text', '').strip()
            if option_text:  # Only include non-empty options
                options.append({
                    'text': option_text,
                    'is_correct': str(i) == correct_answer_index,
                    'order': i + 1
                })
        
        return options
    
    def validate_options(self, options_data):
        """Validate options data"""
        if len(options_data) < 2:
            return False
        
        correct_count = sum(1 for opt in options_data if opt['is_correct'])
        return correct_count == 1
    
    def form_valid(self, form, options_data):
        """Save the updated question and its options"""
        try:
            # Save the question
            self.object = form.save()
            
            # Delete existing options
            self.object.options.all().delete()
            
            # Create new options
            for option_data in options_data:
                Option.objects.create(
                    question=self.object,
                    option_text=option_data['text'],
                    is_correct=option_data['is_correct'],
                    order=option_data['order']
                )
            
            messages.success(
                self.request, 
                f'✅ MCQ #{self.object.id} has been updated successfully!'
            )
            return redirect(self.success_url)
            
        except Exception as e:
            messages.error(
                self.request,
                f'❌ Error updating MCQ: {str(e)}'
            )
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            '❌ Please correct the errors below and try again.'
        )
        return super().form_invalid(form)


class QuestionDeleteView(StaffRequiredMixin, DeleteView):
    """Delete question"""
    model = Question
    template_name = 'staff/questions/question_confirm_delete.html'
    success_url = reverse_lazy('staff:question_list')


class BulkQuestionUploadView(StaffRequiredMixin, FormView):
    """Bulk upload questions via CSV/Excel"""
    template_name = 'staff/questions/bulk_upload.html'
    form_class = BulkQuestionUploadForm
    success_url = reverse_lazy('staff:question_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Bulk Upload MCQs',
            'breadcrumbs': [
                {'title': 'Dashboard', 'url': reverse_lazy('staff:dashboard')},
                {'title': 'MCQs', 'url': reverse_lazy('staff:question_list')},
                {'title': 'Bulk Upload', 'url': None}
            ]
        })
        return context
    
    def dispatch(self, request, *args, **kwargs):
        # Handle template download
        if request.method == 'GET' and request.GET.get('action') == 'download_template':
            return self.download_template()
        
        # Handle error rows download
        if request.method == 'GET' and request.GET.get('action') == 'download_errors':
            session_key = request.GET.get('session_key')
            if session_key and session_key in request.session:
                return self.download_error_rows(request.session[session_key])
        
        return super().dispatch(request, *args, **kwargs)
    
    def download_template(self):
        """Generate and download CSV template"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="mcq_bulk_upload_template.csv"'
        
        writer = csv.writer(response)
        
        # Header row
        writer.writerow([
            'Subject', 'Topic', 'Question Text', 'Option A', 'Option B', 'Option C', 'Option D',
            'Option E', 'Option F', 'Correct Answer', 'Difficulty', 'Tags', 'Explanation', 'Reference'
        ])
        
        # Sample row with examples
        writer.writerow([
            'Anatomy', 'Cardiovascular System', 
            'Which of the following is the primary pacemaker of the heart?',
            'AV node', 'SA node', 'Bundle of His', 'Purkinje fibers', '', '',
            'B', 'Easy', 'High Yield, Cardiology', 
            'The SA node is the natural pacemaker of the heart, generating electrical impulses.',
            'Guyton & Hall p.115'
        ])
        
        # Add some empty rows for data entry
        for _ in range(10):
            writer.writerow([''] * 14)
        
        return response
    
    def download_error_rows(self, error_data):
        """Download rows that had errors for correction"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="mcq_errors_to_fix.csv"'
        
        writer = csv.writer(response)
        
        # Header row
        writer.writerow([
            'Row Number', 'Error Message', 'Subject', 'Topic', 'Question Text', 
            'Option A', 'Option B', 'Option C', 'Option D', 'Option E', 'Option F', 
            'Correct Answer', 'Difficulty', 'Tags', 'Explanation', 'Reference'
        ])
        
        # Error rows
        for error in error_data:
            row_data = [error['row_number'], error['error']] + error['data']
            writer.writerow(row_data)
        
        return response
    
    def form_valid(self, form):
        try:
            result = self.process_uploaded_file(form)
            
            if result['success']:
                messages.success(
                    self.request, 
                    f"✅ Upload completed! {result['added_count']} MCQs added successfully."
                    + (f" {result['error_count']} rows had errors." if result['error_count'] > 0 else "")
                )
                
                # Store error data in session if there are errors
                if result['errors']:
                    session_key = f"upload_errors_{int(time.time())}"
                    self.request.session[session_key] = result['errors']
                    self.request.session['last_upload_errors'] = session_key
                
            else:
                messages.error(self.request, f"❌ Upload failed: {result['message']}")
                
        except Exception as e:
            messages.error(self.request, f"❌ Upload failed: {str(e)}")
        
        return super().form_valid(form)
    
    def process_uploaded_file(self, form):
        """Process the uploaded CSV/Excel file"""
        import pandas as pd
        import time
        
        file = form.cleaned_data['csv_file']
        default_subject = form.cleaned_data.get('default_subject')
        default_difficulty = form.cleaned_data.get('default_difficulty')
        default_tags = form.cleaned_data.get('default_tags', [])
        overwrite_existing = form.cleaned_data.get('overwrite_existing', False)
        
        try:
            # Read file based on extension
            file_extension = os.path.splitext(file.name)[1].lower()
            if file_extension == '.csv':
                df = pd.read_csv(file)
            else:  # Excel files
                df = pd.read_excel(file)
            
            # Validate required columns
            required_columns = ['Question Text', 'Option A', 'Option B', 'Correct Answer']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return {
                    'success': False,
                    'message': f"Missing required columns: {', '.join(missing_columns)}"
                }
            
            # Process each row
            added_count = 0
            error_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    result = self.process_row(row, default_subject, default_difficulty, default_tags, overwrite_existing)
                    if result['success']:
                        added_count += 1
                    else:
                        error_count += 1
                        errors.append({
                            'row_number': index + 2,  # +2 because pandas is 0-indexed and we have header
                            'error': result['error'],
                            'data': [str(row.get(col, '')) for col in df.columns]
                        })
                except Exception as e:
                    error_count += 1
                    errors.append({
                        'row_number': index + 2,
                        'error': f"Processing error: {str(e)}",
                        'data': [str(row.get(col, '')) for col in df.columns]
                    })
            
            return {
                'success': True,
                'added_count': added_count,
                'error_count': error_count,
                'errors': errors
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f"File processing error: {str(e)}"
            }
    
    def process_row(self, row, default_subject, default_difficulty, default_tags, overwrite_existing):
        """Process a single row from the upload file"""
        try:
            # Extract basic question data
            question_text = str(row.get('Question Text', '')).strip()
            if not question_text or question_text == 'nan':
                return {'success': False, 'error': 'Question text is required'}
            
            # Get or create subject
            subject_name = str(row.get('Subject', '')).strip()
            if not subject_name or subject_name == 'nan':
                if default_subject:
                    subject = default_subject
                else:
                    return {'success': False, 'error': 'Subject is required'}
            else:
                subject, created = Subject.objects.get_or_create(
                    name=subject_name,
                    defaults={'is_active': True}
                )
            
            # Get or create topic
            topic_name = str(row.get('Topic', '')).strip()
            if not topic_name or topic_name == 'nan':
                return {'success': False, 'error': 'Topic is required'}
            
            topic, created = Topic.objects.get_or_create(
                name=topic_name,
                subject=subject,
                defaults={'is_active': True}
            )
            
            # Check if question already exists
            if not overwrite_existing:
                existing = Question.objects.filter(
                    question_text=question_text,
                    topic=topic
                ).first()
                if existing:
                    return {'success': False, 'error': 'Question already exists'}
            
            # Get difficulty
            difficulty = str(row.get('Difficulty', '')).strip().lower()
            if not difficulty or difficulty == 'nan':
                if default_difficulty:
                    difficulty = default_difficulty
                else:
                    difficulty = 'medium'  # Default
            
            # Map difficulty values
            difficulty_map = {
                'easy': 'easy', 'e': 'easy',
                'medium': 'medium', 'med': 'medium', 'm': 'medium',
                'hard': 'hard', 'h': 'hard', 'difficult': 'hard'
            }
            difficulty = difficulty_map.get(difficulty, 'medium')
            
            # Create or update question
            question_data = {
                'question_text': question_text,
                'topic': topic,
                'difficulty': difficulty,
                'explanation': str(row.get('Explanation', '')).strip() if str(row.get('Explanation', '')) != 'nan' else '',
                'reference': str(row.get('Reference', '')).strip() if str(row.get('Reference', '')) != 'nan' else '',
                'is_active': True,
                'is_premium': False
            }
            
            if overwrite_existing:
                question, created = Question.objects.update_or_create(
                    question_text=question_text,
                    topic=topic,
                    defaults=question_data
                )
            else:
                question = Question.objects.create(**question_data)
                created = True
            
            # Process options
            options_data = []
            for index, letter in enumerate(['A', 'B', 'C', 'D', 'E', 'F'], start=1):
                option_text = str(row.get(f'Option {letter}', '')).strip()
                if option_text and option_text != 'nan':
                    options_data.append({
                        'letter': letter,
                        'order': index,
                        'option_text': option_text,
                    })
            
            if len(options_data) < 2:
                question.delete()  # Clean up
                return {'success': False, 'error': 'At least 2 options are required'}
            
            # Get correct answer
            correct_answer = str(row.get('Correct Answer', '')).strip().upper()
            if not correct_answer or correct_answer == 'NAN':
                question.delete()
                return {'success': False, 'error': 'Correct answer is required'}
            
            # Validate correct answer
            valid_answers = [opt['letter'] for opt in options_data]
            if correct_answer not in valid_answers:
                question.delete()
                return {'success': False, 'error': f'Correct answer "{correct_answer}" not found in options'}
            
            # Clear existing options if updating
            if not created:
                question.options.all().delete()
            
            # Create options
            for opt_data in options_data:
                Option.objects.create(
                    question=question,
                    option_text=opt_data['option_text'],
                    order=opt_data['order'],
                    is_correct=(opt_data['letter'] == correct_answer)
                )
            
            # Process tags
            tags_text = str(row.get('Tags', '')).strip()
            if tags_text and tags_text != 'nan':
                tag_names = [tag.strip() for tag in tags_text.split(',') if tag.strip()]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name,
                        defaults={'is_active': True}
                    )
                    question.tags.add(tag)
            
            # Add default tags
            for tag in default_tags:
                question.tags.add(tag)
            
            return {'success': True}
            
        except Exception as e:
            return {'success': False, 'error': f"Row processing error: {str(e)}"}


class QuestionBulkActionView(StaffRequiredMixin, ListView):
    """Handle bulk actions on questions"""
    model = Question
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        question_ids = request.POST.getlist('question_ids')
        
        if not question_ids:
            return JsonResponse({'success': False, 'message': 'No questions selected'})
        
        questions = Question.objects.filter(id__in=question_ids)
        
        if action == 'activate':
            questions.update(is_active=True)
            message = f"{questions.count()} questions activated successfully"
        elif action == 'deactivate':
            questions.update(is_active=False)
            message = f"{questions.count()} questions deactivated successfully"
        elif action == 'make_premium':
            questions.update(is_premium=True)
            message = f"{questions.count()} questions marked as premium"
        elif action == 'make_free':
            questions.update(is_premium=False)
            message = f"{questions.count()} questions marked as free"
        elif action == 'delete':
            count = questions.count()
            questions.delete()
            message = f"{count} questions deleted successfully"
        else:
            return JsonResponse({'success': False, 'message': 'Invalid action'})
        
        return JsonResponse({'success': True, 'message': message})


class QuestionExportView(StaffRequiredMixin, ListView):
    """Export questions to CSV"""
    model = Question
    
    def get(self, request, *args, **kwargs):
        # Get filtered queryset based on current filters
        view = QuestionListView()
        view.request = request
        questions = view.get_queryset()
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="questions.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'ID', 'Subject', 'Topic', 'Question', 'Difficulty', 
            'Status', 'Premium', 'Tags', 'Created'
        ])
        
        for question in questions:
            writer.writerow([
                question.id,
                question.topic.subject.name,
                question.topic.name,
                question.question_text[:100] + "..." if len(question.question_text) > 100 else question.question_text,
                question.get_difficulty_display(),
                'Active' if question.is_active else 'Inactive',
                'Yes' if question.is_premium else 'No',
                ', '.join([tag.name for tag in question.tags.all()]),
                question.created_at.strftime('%Y-%m-%d')
            ])
        
        return response


class QuestionToggleStatusView(StaffRequiredMixin, ListView):
    """Toggle question status via AJAX"""
    model = Question
    
    def post(self, request, *args, **kwargs):
        question_id = request.POST.get('question_id')
        try:
            question = Question.objects.get(id=question_id)
            question.is_active = not question.is_active
            question.save()
            
            return JsonResponse({
                'success': True,
                'is_active': question.is_active,
                'message': f'Question {"activated" if question.is_active else "deactivated"} successfully'
            })
        except Question.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Question not found'})


class GetTopicsAjaxView(StaffRequiredMixin, ListView):
    """Get topics for a subject via AJAX"""
    model = Topic
    
    def get(self, request, *args, **kwargs):
        subject_id = request.GET.get('subject_id')
        if subject_id:
            topics = Topic.objects.filter(
                subject_id=subject_id, 
                is_active=True
            ).values('id', 'name')
            return JsonResponse({'topics': list(topics)})
        return JsonResponse({'topics': []})
