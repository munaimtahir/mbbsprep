from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from core.models.user_models import UserProfile
import csv
import io
from datetime import timedelta

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

    USER_ROLE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Administrator'),
    ]

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    year_of_study = forms.ChoiceField(
        choices=[('', 'Select Year')] + list(UserProfile.YEAR_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    province = forms.ChoiceField(
        choices=[('', 'Select Province')] + list(UserProfile.PROVINCE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    college_type = forms.ChoiceField(
        choices=[('', 'Select Type')] + list(UserProfile.COLLEGE_TYPE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    college_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    phone_number = forms.CharField(
        required=False,
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    user_role = forms.ChoiceField(
        choices=USER_ROLE_CHOICES,
        initial='student',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    is_premium = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
    premium_expires_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control', 'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M',
        ),
        help_text='Leave blank to default to one year from now for premium users.',
    )
    send_welcome_email = forms.BooleanField(
        required=False,
        initial=True,
        help_text='Send the standard welcome email after creating the user.',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'is_active']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['premium_expires_at'].input_formats = ['%Y-%m-%dT%H:%M']

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('A user with this email already exists.')
        return email

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords don't match")
        return confirm_password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        is_premium = cleaned_data.get('is_premium')
        premium_expires_at = cleaned_data.get('premium_expires_at')

        if password:
            try:
                validate_password(password)
            except ValidationError as exc:
                self.add_error('password', exc)

        if premium_expires_at and premium_expires_at <= timezone.now():
            self.add_error('premium_expires_at', 'Premium expiry must be in the future.')

        if not is_premium:
            cleaned_data['premium_expires_at'] = None

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])

        user_role = self.cleaned_data.get('user_role', 'student')
        user.is_staff = user_role in {'faculty', 'admin'}
        user.is_superuser = user_role == 'admin'
        user.is_active = self.cleaned_data.get('is_active', True)
        user._skip_welcome_email = not self.cleaned_data.get('send_welcome_email', True)

        if commit:
            user.save()
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.year_of_study = self.cleaned_data.get('year_of_study', '')
            profile.province = self.cleaned_data.get('province', '')
            profile.college_type = self.cleaned_data.get('college_type', '')
            profile.college_name = self.cleaned_data.get('college_name', '')
            profile.phone_number = self.cleaned_data.get('phone_number', '')
            profile.is_premium = self.cleaned_data.get('is_premium', False)
            profile.premium_expires_at = self.cleaned_data.get('premium_expires_at')
            if profile.is_premium and not profile.premium_expires_at:
                profile.premium_expires_at = timezone.now() + timedelta(days=365)
            profile.save()
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
        help_text='Upload a CSV or Excel file with user data.',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv,.xlsx,.xls'
        })
    )
    default_password = forms.CharField(
        required=False,
        initial='TempPass123!',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Used when a row does not include its own password.',
    )
    default_role = forms.ChoiceField(
        choices=UserCreateForm.USER_ROLE_CHOICES,
        initial='student',
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Used when a row does not include its own role.',
    )
    send_welcome_emails = forms.BooleanField(
        required=False,
        initial=True,
        label='Send welcome emails to new users',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    skip_errors = forms.BooleanField(
        required=False,
        initial=False,
        label='Import valid rows even if some rows contain errors',
        help_text='When enabled, only valid rows will be imported after confirmation.',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
    
    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']

        lower_name = csv_file.name.lower()
        if lower_name.endswith(('.xlsx', '.xls')):
            return csv_file

        if not lower_name.endswith('.csv'):
            raise ValidationError('File must be a CSV or Excel file.')

        try:
            csv_file.seek(0)
            content = csv_file.read().decode('utf-8')
            csv_file.seek(0)

            reader = csv.DictReader(io.StringIO(content))
            required_fields = ['email', 'first_name', 'last_name']
            
            if not all(field in reader.fieldnames for field in required_fields):
                raise ValidationError(
                    f'CSV must contain these columns: {", ".join(required_fields)}'
                )
            
            for row_num, row in enumerate(reader, start=2):
                if not row.get('email', '').strip():
                    raise ValidationError(f'Row {row_num}: Email is required')
                email = row.get('email', '').strip()
                if User.objects.filter(email__iexact=email).exists():
                    raise ValidationError(f'Row {row_num}: Email "{email}" already exists')
                    
        except UnicodeDecodeError:
            raise ValidationError('File must be UTF-8 encoded.')
        except csv.Error as e:
            raise ValidationError(f'Invalid CSV format: {e}')
        
        return csv_file
