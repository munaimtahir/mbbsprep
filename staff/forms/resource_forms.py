from django import forms

from core.models.academic_models import Topic
from core.models.resource_models import Flashcard, Note, VideoResource


class NoteForm(forms.ModelForm):
    """Form for creating and editing notes"""
    
    class Meta:
        model = Note
        fields = ['title', 'topic', 'content', 'pdf_file', 'is_premium', 'is_active', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Note title...'
            }),
            'topic': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Note content...'
            }),
            'pdf_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
            }),
            'is_premium': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'style': 'height: 100px;'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic'].queryset = Topic.objects.all()


class VideoResourceForm(forms.ModelForm):
    """Form for creating and editing video resources"""

    video_url = forms.URLField(
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'YouTube, Vimeo, or other video URL...',
            }
        ),
    )
    
    class Meta:
        model = VideoResource
        fields = [
            'title', 'topic', 'description', 'video_url', 'duration_minutes',
            'thumbnail', 'is_premium', 'is_active', 'tags'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Video title...'
            }),
            'topic': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Video description...'
            }),
            'duration_minutes': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Duration in minutes...'
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'is_premium': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'style': 'height: 100px;'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic'].queryset = Topic.objects.all()

    def clean_video_url(self):
        video_url = self.cleaned_data['video_url'].strip()
        if video_url and '://' not in video_url:
            video_url = f'https://{video_url}'
        return video_url


class FlashcardForm(forms.ModelForm):
    """Form for creating and editing flashcards"""
    
    class Meta:
        model = Flashcard
        fields = ['topic', 'front_text', 'back_text', 'is_premium', 'is_active', 'tags']
        widgets = {
            'topic': forms.Select(attrs={'class': 'form-control'}),
            'front_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Question/Term (front of card)...'
            }),
            'back_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Answer/Definition (back of card)...'
            }),
            'is_premium': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'style': 'height: 100px;'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic'].queryset = Topic.objects.all()


class ResourceSearchForm(forms.Form):
    """Form for searching resources"""
    
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search resources...',
        })
    )
    
    topic = forms.ModelChoiceField(
        queryset=Topic.objects.all(),
        required=False,
        empty_label="All Topics",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    resource_type = forms.ChoiceField(
        choices=[
            ('', 'All Types'),
            ('note', 'Notes'),
            ('video', 'Videos'),
            ('flashcard', 'Flashcards'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    is_premium = forms.ChoiceField(
        choices=[
            ('', 'All Resources'),
            ('true', 'Premium Only'),
            ('false', 'Free Only'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    is_active = forms.ChoiceField(
        choices=[
            ('', 'All Resources'),
            ('true', 'Active Only'),
            ('false', 'Inactive Only'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
