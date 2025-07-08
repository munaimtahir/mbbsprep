from django import forms
from core.models.tag_models import Tag, Subtag


class TagForm(forms.ModelForm):
    """Form for creating and editing tags"""
    
    class Meta:
        model = Tag
        fields = [
            'name', 'description', 'color', 'is_active',
            'apply_to_all_resources', 'apply_to_mcq', 'apply_to_videos', 'apply_to_notes'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tag name...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Tag description...'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'value': '#0057A3'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'apply_to_all_resources': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'apply_to_mcq': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'apply_to_videos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'apply_to_notes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SubtagForm(forms.ModelForm):
    """Form for creating and editing subtags"""
    
    class Meta:
        model = Subtag
        fields = ['tag', 'name', 'description', 'color', 'is_active']
        widgets = {
            'tag': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subtag name...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Subtag description...'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'placeholder': 'Leave blank to inherit from parent tag'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tag'].queryset = Tag.objects.filter(is_active=True)


class TagSearchForm(forms.Form):
    """Form for searching tags"""
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search tags...',
        })
    )
    
    is_active = forms.ChoiceField(
        choices=[
            ('', 'All Tags'),
            ('true', 'Active Only'),
            ('false', 'Inactive Only'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    apply_to = forms.ChoiceField(
        choices=[
            ('', 'All Applications'),
            ('mcq', 'MCQ Only'),
            ('videos', 'Videos Only'),
            ('notes', 'Notes Only'),
            ('all', 'All Resources'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
