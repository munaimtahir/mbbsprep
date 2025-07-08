import csv
import io
from django.views.generic import FormView
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db import transaction
from .user_views import StaffRequiredMixin
from ..forms import TopicBulkUploadForm
from core.models import Subject, Topic, Tag, Subtag


class TopicBulkUploadView(StaffRequiredMixin, FormView):
    """Bulk upload topics from CSV file"""
    template_name = 'staff/topics/bulk_upload.html'
    form_class = TopicBulkUploadForm
    success_url = reverse_lazy('staff:topic_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Bulk Upload Topics',
            'breadcrumbs': [
                {'url': reverse_lazy('staff:dashboard'), 'name': 'Dashboard'},
                {'url': reverse_lazy('staff:topic_list'), 'name': 'Topics'},
                {'name': 'Bulk Upload'}
            ]
        })
        return context
    
    def form_valid(self, form):
        """Handle valid form submission"""
        try:
            csv_file = form.cleaned_data.get('csv_file')
            create_subjects = form.cleaned_data.get('create_subjects', True)
            create_tags = form.cleaned_data.get('create_tags', True)
            
            if csv_file:
                # Process the CSV file
                result = self.process_csv_file(csv_file, create_subjects, create_tags)
                
                if result.get('success', False):
                    messages.success(
                        self.request,
                        f"Successfully processed {result.get('processed', 0)} rows. "
                        f"Created {result.get('created_topics', 0)} topics, "
                        f"{result.get('created_subjects', 0)} subjects, "
                        f"{result.get('created_tags', 0)} tags."
                    )
                else:
                    messages.warning(self.request, f"Upload completed with issues: {result.get('error', 'Unknown error')}")
            else:
                messages.error(self.request, "No CSV file provided.")
                
        except Exception as e:
            # Even if processing fails, we still redirect with an error message
            messages.error(self.request, f"Processing error: {str(e)}")
        
        # ALWAYS redirect - this guarantees a 302 response
        return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form):
        """Handle invalid form submission - also redirect to avoid 200 response"""
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        
        # Redirect even on form errors to ensure consistent behavior
        return HttpResponseRedirect(self.get_success_url())
    
    def process_csv_file(self, csv_file, create_subjects=True, create_tags=True):
        """Process the CSV file and create topics, subjects, and tags"""
        
        result = {
            'success': False,
            'processed': 0,
            'created_topics': 0,
            'created_subjects': 0,
            'created_tags': 0,
            'errors': [],
            'error': None
        }
        
        try:
            # Read CSV content
            csv_file.seek(0)
            content = csv_file.read().decode('utf-8-sig')
            csv_reader = csv.DictReader(io.StringIO(content))
            
            with transaction.atomic():
                for row_num, row in enumerate(csv_reader, start=2):  # Start at 2 for proper line numbering
                    try:
                        # Clean and validate row data
                        lo_text = row.get('LOs', '').strip()
                        sub_topic = row.get('Sub-Topic', '').strip()
                        topic_name = row.get('Topic', '').strip()
                        subject_name = row.get('Subject', '').strip()
                        subject_type = row.get('Type', '').strip()
                        module = row.get('Module', '').strip()
                        assessment = row.get('Assessment', '').strip()
                        
                        # Skip empty rows
                        if not lo_text and not topic_name:
                            continue
                        
                        # Process subject
                        subject = self.get_or_create_subject(subject_name, create_subjects)
                        if not subject:
                            result['errors'].append(f"Row {row_num}: Subject '{subject_name}' not found")
                            continue
                        
                        # Process topic
                        topic = self.get_or_create_topic(subject, topic_name, lo_text)
                        if topic and hasattr(topic, '_created') and topic._created:
                            result['created_topics'] += 1
                        
                        # Process tags if enabled
                        if create_tags and topic:
                            self.process_tags_for_topic(
                                topic, topic_name, sub_topic, subject_type, 
                                module, assessment, result
                            )
                        
                        result['processed'] += 1
                        
                    except Exception as e:
                        result['errors'].append(f"Row {row_num}: {str(e)}")
                        continue
                
                result['success'] = True
                
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
        
        return result
    
    def get_or_create_subject(self, subject_name, create_if_missing=True):
        """Get or create subject"""
        if not subject_name:
            return None
        
        try:
            subject = Subject.objects.get(name__iexact=subject_name)
            return subject
        except Subject.DoesNotExist:
            if create_if_missing:
                # Generate a simple code from subject name
                code = ''.join([word[0].upper() for word in subject_name.split()[:3]])
                subject = Subject.objects.create(
                    name=subject_name,
                    code=code,
                    description=f"Auto-created from bulk upload: {subject_name}"
                )
                subject._created = True
                return subject
            return None
    
    def get_or_create_topic(self, subject, topic_name, description=''):
        """Get or create topic"""
        if not topic_name:
            return None
        
        topic, created = Topic.objects.get_or_create(
            subject=subject,
            name=topic_name,
            defaults={
                'description': description or f"Auto-created from bulk upload: {topic_name}",
                'order': Topic.objects.filter(subject=subject).count() + 1
            }
        )
        
        if created:
            topic._created = True
        
        return topic
    
    def process_tags_for_topic(self, topic, topic_name, sub_topic, subject_type, module, assessment, result):
        """Create and associate tags with the topic"""
        tag_data = [
            ('Topic', topic_name, '#0057A3'),
            ('Sub-Topic', sub_topic, '#28A745'),
            ('Type', subject_type, '#FFC107'),
            ('Module', module, '#17A2B8'),
            ('Assessment', assessment, '#DC3545')
        ]
        
        for tag_type, tag_value, default_color in tag_data:
            if not tag_value:
                continue
            
            try:
                # Create or get the main tag
                tag, created = Tag.objects.get_or_create(
                    name=f"{tag_type}: {tag_value}",
                    defaults={
                        'description': f"Auto-created {tag_type.lower()} tag from bulk upload",
                        'color': default_color,
                        'apply_to_all_resources': True
                    }
                )
                
                if created:
                    result['created_tags'] += 1
                
                # Associate tag with topic (if Topic model has tags relationship)
                if hasattr(topic, 'tags'):
                    topic.tags.add(tag)
                
                # Create subtag if this is a sub-topic
                if tag_type == 'Sub-Topic' and tag_value:
                    # Try to find parent topic tag
                    parent_tag_name = f"Topic: {topic_name}"
                    try:
                        parent_tag = Tag.objects.get(name=parent_tag_name)
                        subtag, subtag_created = Subtag.objects.get_or_create(
                            tag=parent_tag,
                            name=tag_value,
                            defaults={
                                'description': f"Auto-created subtag from bulk upload",
                                'color': '#28A745'
                            }
                        )
                        if subtag_created:
                            result['created_tags'] += 1
                    except Tag.DoesNotExist:
                        pass  # Parent tag doesn't exist, skip subtag creation
                
            except Exception as e:
                result['errors'].append(f"Error creating tag '{tag_type}: {tag_value}': {str(e)}")


class TopicBulkUploadTemplateView(StaffRequiredMixin, FormView):
    """Download CSV template for bulk upload"""
    
    def get(self, request, *args, **kwargs):
        """Download CSV template"""
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="topics_bulk_upload_template.csv"'
        
        writer = csv.writer(response)
        
        # Write header
        writer.writerow(['LOs', 'Sub-Topic', 'Topic', 'Subject', 'Type', 'Module', 'Assessment'])
        
        # Write sample data
        writer.writerow([
            'Describe the structure and function of cell membrane',
            'Cell Membrane',
            'Cell and Genetics',
            'Biochemistry',
            'Major Subject',
            'Foundation-1 Module',
            'MCQS'
        ])
        writer.writerow([
            'Define pH and pH scale concepts',
            'Water, pH and Buffers',
            'Cell and Genetics',
            'Biochemistry',
            'Major Subject',
            'Foundation-1 Module',
            'MCQS'
        ])
        
        return response
