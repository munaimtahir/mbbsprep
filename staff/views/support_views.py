from django.views.generic import ListView, TemplateView
from .user_views import StaffRequiredMixin


class SupportInboxView(StaffRequiredMixin, ListView):
    """View support messages"""
    template_name = 'staff/support/inbox.html'
    context_object_name = 'messages'
    paginate_by = 25
    
    def get_queryset(self):
        # Will be implemented when contact model is available
        return []


class SupportMessageView(StaffRequiredMixin, TemplateView):
    """Placeholder view for individual support message"""
    template_name = 'staff/support/message_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message_id'] = kwargs.get('pk')
        return context
