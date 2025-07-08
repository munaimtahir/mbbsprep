import json
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from core.models import Tag, Subtag
from ..forms import TagForm, SubtagForm
from .user_views import StaffRequiredMixin


class TagAjaxMixin(StaffRequiredMixin):
    """Base mixin for tag AJAX operations"""
    def render_to_json_response(self, context, status=200):
        """Return JSON response"""
        return JsonResponse(context, status=status)


class TagGetAjaxView(TagAjaxMixin, View):
    """Get tag data for editing"""
    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        resource_types = []
        
        if tag.apply_to_all_resources:
            resource_types.append('all')
        else:
            if tag.apply_to_mcq:
                resource_types.append('mcq')
            if tag.apply_to_videos:
                resource_types.append('video')
            if tag.apply_to_notes:
                resource_types.append('note')
        
        data = {
            'id': tag.id,
            'name': tag.name,
            'description': tag.description,
            'color': tag.color,
            'is_active': tag.is_active,
            'resources': resource_types,
        }
        
        return self.render_to_json_response({
            'success': True,
            'tag': data
        })


class TagCreateAjaxView(TagAjaxMixin, View):
    """Create a new tag via AJAX"""
    def post(self, request):
        try:
            # Try to parse JSON data first
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                # Handle form data
                data = request.POST.dict()
            
            # Set default values for optional fields if not provided
            if 'color' not in data:
                data['color'] = '#0057A3'
            if 'is_active' not in data:
                data['is_active'] = True
            if 'apply_to_all_resources' not in data:
                data['apply_to_all_resources'] = False
            if 'apply_to_mcq' not in data:
                data['apply_to_mcq'] = False
            if 'apply_to_videos' not in data:
                data['apply_to_videos'] = False
            if 'apply_to_notes' not in data:
                data['apply_to_notes'] = False
            
            form = TagForm(data)
            
            if form.is_valid():
                tag = form.save()
                return self.render_to_json_response({
                    'success': True,
                    'message': 'Tag created successfully',
                    'id': tag.id,
                    'name': tag.name,
                    'color': tag.color,
                    'is_active': tag.is_active
                })
            else:
                # Check if it's a duplicate name error
                if 'name' in form.errors:
                    name_errors = form.errors['name']
                    if any('already exists' in str(error) for error in name_errors):
                        # Return existing tag if duplicate
                        try:
                            existing_tag = Tag.objects.get(name=data['name'])
                            return self.render_to_json_response({
                                'success': True,
                                'message': 'Tag already exists',
                                'id': existing_tag.id,
                                'name': existing_tag.name,
                                'color': existing_tag.color,
                                'is_active': existing_tag.is_active
                            })
                        except Tag.DoesNotExist:
                            pass
                
                return self.render_to_json_response({
                    'success': False,
                    'message': 'Failed to create tag',
                    'errors': form.errors
                }, status=400)
        except Exception as e:
            return self.render_to_json_response({
                'success': False,
                'message': f'Error processing request: {str(e)}'
            }, status=500)


class TagUpdateAjaxView(TagAjaxMixin, View):
    """Update existing tag via AJAX"""
    def post(self, request, pk):
        try:
            # Try to parse JSON data first
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                # Handle form data
                data = request.POST.dict()
            
            tag = get_object_or_404(Tag, pk=pk)
            form = TagForm(data, instance=tag)
            
            if form.is_valid():
                tag = form.save()
                return self.render_to_json_response({
                    'success': True,
                    'message': 'Tag updated successfully',
                    'id': tag.id,
                    'name': tag.name,
                    'color': tag.color,
                    'is_active': tag.is_active
                })
            else:
                return self.render_to_json_response({
                    'success': False,
                    'message': 'Failed to update tag',
                    'errors': form.errors
                }, status=400)
        except Exception as e:
            return self.render_to_json_response({
                'success': False,
                'message': f'Error processing request: {str(e)}'
            }, status=500)
            return self.render_to_json_response({
                'success': True,
                'message': 'Tag updated successfully',
                'id': tag.id,
                'name': tag.name,
                'color': tag.color,
                'is_active': tag.is_active
            })
        else:
            return self.render_to_json_response({
                'success': False,
                'message': 'Failed to update tag',
                'errors': form.errors
            }, status=400)


class TagToggleStatusView(TagAjaxMixin, View):
    """Toggle tag active status"""
    def post(self, request):
        data = json.loads(request.body)
        tag_id = data.get('tag_id')
        
        try:
            tag = Tag.objects.get(pk=tag_id)
            tag.is_active = not tag.is_active
            tag.save()
            
            return self.render_to_json_response({
                'success': True,
                'message': f"Tag {'activated' if tag.is_active else 'archived'} successfully",
                'is_active': tag.is_active
            })
        except Tag.DoesNotExist:
            return self.render_to_json_response({
                'success': False,
                'message': 'Tag not found'
            }, status=404)


class TagBulkActionView(TagAjaxMixin, View):
    """Process bulk actions on tags"""
    def post(self, request):
        data = json.loads(request.body)
        tag_ids = data.get('tag_ids', [])
        action = data.get('action')
        
        if not tag_ids:
            return self.render_to_json_response({
                'success': False,
                'message': 'No tags selected'
            }, status=400)
            
        if action not in ['archive', 'restore', 'delete']:
            return self.render_to_json_response({
                'success': False,
                'message': 'Invalid action'
            }, status=400)
        
        # Process based on action
        try:
            tags = Tag.objects.filter(pk__in=tag_ids)
            
            if action == 'archive':
                tags.update(is_active=False)
                message = 'Tags archived successfully'
            elif action == 'restore':
                tags.update(is_active=True)
                message = 'Tags restored successfully'
            elif action == 'delete':
                # Check if any tags have subtags
                has_subtags = Subtag.objects.filter(tag__in=tags).exists()
                if has_subtags:
                    return self.render_to_json_response({
                        'success': False,
                        'message': 'Cannot delete tags with subtags'
                    }, status=400)
                    
                tags.delete()
                message = 'Tags deleted successfully'
                
            return self.render_to_json_response({
                'success': True,
                'message': message
            })
            
        except Exception as e:
            return self.render_to_json_response({
                'success': False,
                'message': f'Error: {str(e)}'
            }, status=500)


class GetTagSubtagsView(TagAjaxMixin, View):
    """Get subtags for a tag"""
    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        subtags = tag.subtags.all()
        
        subtags_data = [
            {
                'id': subtag.id,
                'name': subtag.name,
                'is_active': subtag.is_active,
                'resource_count': subtag.get_resource_count()
            }
            for subtag in subtags
        ]
        
        return self.render_to_json_response({
            'success': True,
            'subtags': subtags_data
        })


class SubtagCreateAjaxView(TagAjaxMixin, View):
    """Create a new subtag via AJAX"""
    def post(self, request):
        data = json.loads(request.body)
        form = SubtagForm(data)
        
        if form.is_valid():
            subtag = form.save()
            return self.render_to_json_response({
                'success': True,
                'message': 'Subtag created successfully',
                'id': subtag.id,
                'name': subtag.name,
                'is_active': subtag.is_active,
                'resource_count': 0
            })
        else:
            return self.render_to_json_response({
                'success': False,
                'message': 'Failed to create subtag',
                'errors': form.errors
            }, status=400)


class SubtagUpdateAjaxView(TagAjaxMixin, View):
    """Update existing subtag via AJAX"""
    def post(self, request, pk):
        data = json.loads(request.body)
        subtag = get_object_or_404(Subtag, pk=pk)
        form = SubtagForm(data, instance=subtag)
        
        if form.is_valid():
            subtag = form.save()
            return self.render_to_json_response({
                'success': True,
                'message': 'Subtag updated successfully',
                'id': subtag.id,
                'name': subtag.name,
                'is_active': subtag.is_active,
                'resource_count': subtag.get_resource_count()
            })
        else:
            return self.render_to_json_response({
                'success': False,
                'message': 'Failed to update subtag',
                'errors': form.errors
            }, status=400)


class SubtagToggleStatusView(TagAjaxMixin, View):
    """Toggle subtag active status"""
    def post(self, request):
        data = json.loads(request.body)
        subtag_id = data.get('subtag_id')
        
        try:
            subtag = Subtag.objects.get(pk=subtag_id)
            subtag.is_active = not subtag.is_active
            subtag.save()
            
            return self.render_to_json_response({
                'success': True,
                'message': f"Subtag {'activated' if subtag.is_active else 'archived'} successfully",
                'is_active': subtag.is_active
            })
        except Subtag.DoesNotExist:
            return self.render_to_json_response({
                'success': False,
                'message': 'Subtag not found'
            }, status=404)


class SubtagDeleteView(TagAjaxMixin, View):
    """Delete a subtag"""
    def post(self, request):
        data = json.loads(request.body)
        subtag_id = data.get('subtag_id')
        
        try:
            subtag = Subtag.objects.get(pk=subtag_id)
            subtag.delete()
            
            return self.render_to_json_response({
                'success': True,
                'message': 'Subtag deleted successfully'
            })
        except Subtag.DoesNotExist:
            return self.render_to_json_response({
                'success': False,
                'message': 'Subtag not found'
            }, status=404)
