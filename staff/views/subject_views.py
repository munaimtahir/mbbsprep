from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction, models
from core.models import Subject, Topic
from .user_views import StaffRequiredMixin


class SubjectListView(StaffRequiredMixin, ListView):
    """List all subjects"""
    model = Subject
    template_name = 'staff/subjects/subject_list_new.html'  # Updated to use new template
    context_object_name = 'subjects'
    
    def get_queryset(self):
        """Filter subjects based on search and status"""
        queryset = Subject.objects.all()
        
        # Search functionality
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        # Status filter
        status = self.request.GET.get('status', '').strip()
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'archived':
            queryset = queryset.filter(is_active=False)
        
        return queryset.order_by('name')
    
    def get_context_data(self, **kwargs):
        """Add additional context for the template"""
        context = super().get_context_data(**kwargs)
        
        # Calculate statistics
        all_subjects = Subject.objects.all()
        context['active_subjects'] = all_subjects.filter(is_active=True).count()
        
        # Get total topics and questions count
        try:
            from core.models import Question
            context['total_topics'] = Topic.objects.count()
            context['total_questions'] = Question.objects.count()
        except ImportError:
            context['total_topics'] = 0
            context['total_questions'] = 0
        
        return context


@method_decorator(csrf_exempt, name='dispatch')
class SubjectCreateAjaxView(StaffRequiredMixin, View):
    """AJAX view to create a new subject"""
    
    def post(self, request):
        try:
            data = {
                'name': request.POST.get('name', '').strip(),
                'code': request.POST.get('code', '').strip(),
                'description': request.POST.get('description', '').strip(),
                'is_active': request.POST.get('is_active', 'true') == 'true'
            }
            
            # Validation
            if not data['name']:
                return JsonResponse({'success': False, 'message': 'Subject name is required'})
            
            # Check for duplicate name
            if Subject.objects.filter(name=data['name']).exists():
                return JsonResponse({'success': False, 'message': 'A subject with this name already exists'})
            
            # Check for duplicate code if provided
            if data['code'] and Subject.objects.filter(code=data['code']).exists():
                return JsonResponse({'success': False, 'message': 'A subject with this code already exists'})
            
            # Create subject
            subject = Subject.objects.create(**data)
            
            return JsonResponse({
                'success': True,
                'message': 'Subject created successfully',
                'subject': {
                    'id': subject.id,
                    'name': subject.name,
                    'code': subject.code,
                    'description': subject.description,
                    'is_active': subject.is_active,
                    'topics_count': 0,
                    'questions_count': 0
                }
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error creating subject: {str(e)}'})


@method_decorator(csrf_exempt, name='dispatch')
class SubjectEditAjaxView(StaffRequiredMixin, View):
    """AJAX view to edit an existing subject"""
    
    def get(self, request, pk):
        """Get subject data for editing"""
        try:
            subject = get_object_or_404(Subject, pk=pk)
            return JsonResponse({
                'success': True,
                'subject': {
                    'id': subject.id,
                    'name': subject.name,
                    'code': subject.code,
                    'description': subject.description,
                    'is_active': subject.is_active,
                    'topics_count': subject.topics.count(),
                    'questions_count': getattr(subject, 'questions', subject.topics.all().aggregate(
                        total=models.Count('questions'))['total'] or 0)
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error loading subject: {str(e)}'})
    
    def post(self, request, pk):
        """Update subject data"""
        try:
            subject = get_object_or_404(Subject, pk=pk)
            
            data = {
                'name': request.POST.get('name', '').strip(),
                'code': request.POST.get('code', '').strip(),
                'description': request.POST.get('description', '').strip(),
                'is_active': request.POST.get('is_active', 'true') == 'true'
            }
            
            # Validation
            if not data['name']:
                return JsonResponse({'success': False, 'message': 'Subject name is required'})
            
            # Check for duplicate name (excluding current subject)
            if Subject.objects.exclude(pk=pk).filter(name=data['name']).exists():
                return JsonResponse({'success': False, 'message': 'A subject with this name already exists'})
            
            # Check for duplicate code if provided (excluding current subject)
            if data['code'] and Subject.objects.exclude(pk=pk).filter(code=data['code']).exists():
                return JsonResponse({'success': False, 'message': 'A subject with this code already exists'})
            
            # Update subject
            for field, value in data.items():
                setattr(subject, field, value)
            subject.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Subject updated successfully',
                'subject': {
                    'id': subject.id,
                    'name': subject.name,
                    'code': subject.code,
                    'description': subject.description,
                    'is_active': subject.is_active,
                    'topics_count': subject.topics.count(),
                    'questions_count': getattr(subject, 'questions', subject.topics.all().aggregate(
                        total=models.Count('questions'))['total'] or 0)
                }
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error updating subject: {str(e)}'})


@method_decorator(csrf_exempt, name='dispatch')
class SubjectToggleStatusView(StaffRequiredMixin, View):
    """AJAX view to toggle subject active status (archive/restore)"""
    
    def post(self, request):
        try:
            subject_id = request.POST.get('subject_id')
            action = request.POST.get('action')  # 'archive' or 'restore'
            
            if not subject_id or action not in ['archive', 'restore']:
                return JsonResponse({'success': False, 'message': 'Invalid request parameters'})
            
            subject = get_object_or_404(Subject, pk=subject_id)
            
            if action == 'archive':
                subject.is_active = False
                message = f'Subject "{subject.name}" has been archived'
            else:  # restore
                subject.is_active = True
                message = f'Subject "{subject.name}" has been restored'
            
            subject.save()
            
            return JsonResponse({
                'success': True,
                'message': message,
                'subject_id': subject.id,
                'is_active': subject.is_active
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error updating subject status: {str(e)}'})


class GetSubjectTopicsView(StaffRequiredMixin, View):
    """AJAX view to get topics for a subject"""
    
    def get(self, request, pk):
        try:
            subject = get_object_or_404(Subject, pk=pk)
            topics = subject.topics.all().order_by('order', 'name')
            
            topics_data = []
            for topic in topics:
                # Get question count for topic
                question_count = 0
                try:
                    from core.models import Question
                    question_count = Question.objects.filter(topic=topic).count()
                except ImportError:
                    pass
                
                topics_data.append({
                    'id': topic.id,
                    'name': topic.name,
                    'description': topic.description,
                    'order': topic.order,
                    'is_active': topic.is_active,
                    'question_count': question_count
                })
            
            return JsonResponse({
                'success': True,
                'topics': topics_data
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error loading topics: {str(e)}'})


@method_decorator(csrf_exempt, name='dispatch')
class TopicCreateAjaxView(StaffRequiredMixin, View):
    """AJAX view to create a new topic"""
    
    def post(self, request):
        try:
            subject_id = request.POST.get('subject_id')
            name = request.POST.get('name', '').strip()
            
            if not subject_id or not name:
                return JsonResponse({'success': False, 'message': 'Subject and topic name are required'})
            
            subject = get_object_or_404(Subject, pk=subject_id)
            
            # Check for duplicate topic name within the subject
            if subject.topics.filter(name=name).exists():
                return JsonResponse({'success': False, 'message': 'A topic with this name already exists in this subject'})
            
            # Get next order
            last_topic = subject.topics.order_by('-order').first()
            order = (last_topic.order + 1) if last_topic else 1
            
            # Create topic
            topic = Topic.objects.create(
                subject=subject,
                name=name,
                order=order,
                is_active=True
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Topic created successfully',
                'topic': {
                    'id': topic.id,
                    'name': topic.name,
                    'description': topic.description,
                    'order': topic.order,
                    'is_active': topic.is_active,
                    'question_count': 0
                }
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error creating topic: {str(e)}'})


@method_decorator(csrf_exempt, name='dispatch')
class TopicEditAjaxView(StaffRequiredMixin, View):
    """AJAX view to edit an existing topic"""
    
    def post(self, request, pk):
        try:
            topic = get_object_or_404(Topic, pk=pk)
            name = request.POST.get('name', '').strip()
            
            if not name:
                return JsonResponse({'success': False, 'message': 'Topic name is required'})
            
            # Check for duplicate name within the same subject (excluding current topic)
            if topic.subject.topics.exclude(pk=pk).filter(name=name).exists():
                return JsonResponse({'success': False, 'message': 'A topic with this name already exists in this subject'})
            
            # Update topic
            topic.name = name
            topic.save()
            
            # Get question count
            question_count = 0
            try:
                from core.models import Question
                question_count = Question.objects.filter(topic=topic).count()
            except ImportError:
                pass
            
            return JsonResponse({
                'success': True,
                'message': 'Topic updated successfully',
                'topic': {
                    'id': topic.id,
                    'name': topic.name,
                    'description': topic.description,
                    'order': topic.order,
                    'is_active': topic.is_active,
                    'question_count': question_count
                }
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error updating topic: {str(e)}'})


# Keep existing views for compatibility
class SubjectCreateView(StaffRequiredMixin, CreateView):
    """Create new subject"""
    model = Subject
    template_name = 'staff/subjects/subject_form.html'
    fields = ['name', 'code', 'description', 'year_applicable', 'is_active']
    success_url = reverse_lazy('staff:subject_list')


class SubjectEditView(StaffRequiredMixin, UpdateView):
    """Edit existing subject"""
    model = Subject
    template_name = 'staff/subjects/subject_form.html'
    fields = ['name', 'code', 'description', 'year_applicable', 'is_active']
    success_url = reverse_lazy('staff:subject_list')


class TopicListView(StaffRequiredMixin, ListView):
    """List all topics"""
    model = Topic
    template_name = 'staff/topics/topic_list.html'
    context_object_name = 'topics'


class TopicCreateView(StaffRequiredMixin, CreateView):
    """Create new topic"""
    model = Topic
    template_name = 'staff/topics/topic_form.html'
    fields = ['subject', 'name', 'description', 'order', 'is_active']
    success_url = reverse_lazy('staff:topic_list')


class TopicEditView(StaffRequiredMixin, UpdateView):
    """Edit existing topic"""
    model = Topic
    template_name = 'staff/topics/topic_form.html'
    fields = ['subject', 'name', 'description', 'order', 'is_active']
    success_url = reverse_lazy('staff:topic_list')
