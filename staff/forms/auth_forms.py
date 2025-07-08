from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


class StaffLoginForm(AuthenticationForm):
    """Custom login form for staff/admin users"""
    
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autofocus': True
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Password'
        self.fields['remember_me'].label = 'Remember me'
    
    def clean(self):
        """Validate that the user is staff"""
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            user = authenticate(
                request=self.request if hasattr(self, 'request') else None,
                username=username,
                password=password
            )
            
            if user and not user.is_staff:
                raise ValidationError(
                    "You do not have permission to access the admin area."
                )
        
        return cleaned_data
