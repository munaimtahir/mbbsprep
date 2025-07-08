from django import forms
from core.models.subscription_models import PaymentProof, SubscriptionPlan


class PaymentReviewForm(forms.ModelForm):
    """Form for reviewing payment proofs"""
    
    ACTION_CHOICES = [
        ('approve', 'Approve Payment'),
        ('reject', 'Reject Payment'),
        ('pending', 'Keep Pending'),
    ]
    
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = PaymentProof
        fields = ['status', 'admin_notes']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'admin_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Add notes for the user (especially for rejections)...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make status field read-only as it's handled by action
        self.fields['status'].widget.attrs['readonly'] = True


class PaymentSearchForm(forms.Form):
    """Form for searching payment proofs"""
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by user, transaction ID...',
        })
    )
    
    status = forms.ChoiceField(
        choices=[
            ('', 'All Statuses'),
            ('pending', 'Pending Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('expired', 'Expired'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    subscription_plan = forms.ModelChoiceField(
        queryset=SubscriptionPlan.objects.filter(is_active=True),
        required=False,
        empty_label="All Plans",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    payment_method = forms.ChoiceField(
        choices=[
            ('', 'All Methods'),
            ('jazzcash', 'JazzCash'),
            ('easypaisa', 'EasyPaisa'),
            ('bank_transfer', 'Bank Transfer'),
            ('other', 'Other'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class SubscriptionPlanForm(forms.ModelForm):
    """Form for creating and editing subscription plans"""
    
    class Meta:
        model = SubscriptionPlan
        fields = ['name', 'plan_type', 'price', 'duration_days', 'features', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Plan name...'
            }),
            'plan_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Price in PKR...'
            }),
            'duration_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Duration in days...'
            }),
            'features': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'List plan features...'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
