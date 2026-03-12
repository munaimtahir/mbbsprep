from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, UpdateView

from core.models import PaymentProof
from ..forms import PaymentReviewForm
from .user_views import StaffRequiredMixin


class PaymentListView(StaffRequiredMixin, ListView):
    """List pending payments"""
    model = PaymentProof
    template_name = 'staff/payments/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 25

    def get_queryset(self):
        return PaymentProof.objects.filter(status='pending').select_related(
            'user', 'subscription_plan'
        ).order_by('-submitted_at')


class PaymentReviewView(StaffRequiredMixin, UpdateView):
    """Review payment proof"""
    model = PaymentProof
    form_class = PaymentReviewForm
    template_name = 'staff/payments/payment_review.html'
    success_url = reverse_lazy('staff:payment_list')

    def get_queryset(self):
        return PaymentProof.objects.select_related('user', 'subscription_plan', 'reviewed_by')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.admin_notes = form.cleaned_data.get('admin_notes', '')
        action = form.cleaned_data['action']

        if action == 'approve':
            self.object.approve_payment(self.request.user)
            messages.success(self.request, 'Payment approved and premium access activated.')
        elif action == 'reject':
            self.object.reject_payment(self.request.user, self.object.admin_notes)
            messages.success(self.request, 'Payment rejected successfully.')
        else:
            self.object.status = 'pending'
            self.object.reviewed_by = self.request.user
            self.object.reviewed_at = timezone.now()
            self.object.save(update_fields=['status', 'admin_notes', 'reviewed_by', 'reviewed_at'])
            messages.info(self.request, 'Payment left pending for later review.')

        return HttpResponseRedirect(self.get_success_url())


class PaymentHistoryView(StaffRequiredMixin, ListView):
    """View payment history"""
    model = PaymentProof
    template_name = 'staff/payments/payment_history.html'
    context_object_name = 'payments'
    paginate_by = 50

    def get_queryset(self):
        return PaymentProof.objects.exclude(status='pending').select_related(
            'user', 'subscription_plan', 'reviewed_by'
        ).order_by('-reviewed_at', '-submitted_at')
