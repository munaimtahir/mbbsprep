from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from core.models.user_models import UserProfile
import csv
import io

User = get_user_model()


class UserSearchForm(forms.Form):
    """Form for searching users"""
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, email, or username...',
        })
    )
    
    is_active = forms.ChoiceField(
        choices=[
            ('', 'All Users'),
            ('true', 'Active Only'),
            ('false', 'Inactive Only'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    is_premium = forms.ChoiceField(
        choices=[
            ('', 'All Users'),
            ('true', 'Premium Only'),
            ('false', 'Free Only'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class UserCreateForm(forms.ModelForm):
    """Form for creating new users"""
    
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            # Create profile
            UserProfile.objects.get_or_create(user=user)
        return user


class UserEditForm(forms.ModelForm):
    """Form for editing existing users"""
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class BulkUserUploadForm(forms.Form):
    """Form for bulk uploading users via CSV"""
    
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with user data. Required columns: username, email, first_name, last_name',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv'
        })
    )
    
    send_welcome_email = forms.BooleanField(
        required=False,
        initial=True,
        label='Send welcome emails to new users',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']
        
        if not csv_file.name.endswith('.csv'):
            raise ValidationError('File must be a CSV file.')
        
        # Read and validate CSV content
        try:
            csv_file.seek(0)
            content = csv_file.read().decode('utf-8')
            csv_file.seek(0)  # Reset file pointer
            
            reader = csv.DictReader(io.StringIO(content))
            required_fields = ['username', 'email', 'first_name', 'last_name']
            
            if not all(field in reader.fieldnames for field in required_fields):
                raise ValidationError(
                    f'CSV must contain these columns: {", ".join(required_fields)}'
                )
            
            # Validate each row
            for row_num, row in enumerate(reader, start=2):
                if not row.get('username', '').strip():
                    raise ValidationError(f'Row {row_num}: Username is required')
                if not row.get('email', '').strip():
                    raise ValidationError(f'Row {row_num}: Email is required')
                
                # Check for duplicate usernames in CSV
                username = row.get('username', '').strip()
                if User.objects.filter(username=username).exists():
                    raise ValidationError(f'Row {row_num}: Username "{username}" already exists')
                    
        except UnicodeDecodeError:
            raise ValidationError('File must be UTF-8 encoded.')
        except csv.Error as e:
            raise ValidationError(f'Invalid CSV format: {e}')
        
        return csv_file
