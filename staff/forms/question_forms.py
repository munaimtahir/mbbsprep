from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from core.models.academic_models import Subject, Topic, Question, Option
import csv
import io


class QuestionForm(forms.ModelForm):
    """Form for creating and editing questions"""
    
    class Meta:
        model = Question
        fields = [
            'question_text', 'topic', 'difficulty', 'explanation', 
            'reference', 'tags', 'is_premium', 'is_active'
        ]
        widgets = {
            'question_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter the question text...'
            }),
            'topic': forms.Select(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'explanation': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter explanation for the correct answer...'
            }),
            'reference': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Reference source (e.g., Robbins p.117)'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'style': 'height: 100px;'
            }),
            'is_premium': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic'].queryset = Topic.objects.all()


class OptionForm(forms.ModelForm):
    """Form for creating and editing question options"""
    
    class Meta:
        model = Option
        fields = ['option_text', 'is_correct']
        widgets = {
            'option_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter option text...'
            }),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# Create formset for options
OptionFormSet = inlineformset_factory(
    Question,
    Option,
    form=OptionForm,
    extra=4,  # Number of empty forms to display
    max_num=4,  # Maximum number of options
    min_num=2,  # Minimum number of options
    validate_min=True,
    validate_max=True,
    can_delete=True
)


class BulkQuestionUploadForm(forms.Form):
    """Form for bulk uploading questions via CSV"""
    
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with question data. Required columns: question_text, topic, difficulty, explanation, option_a, option_b, option_c, option_d, correct_answer',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv'
        })
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
            required_fields = [
                'question_text', 'topic', 'difficulty', 'explanation',
                'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer'
            ]
            
            if not all(field in reader.fieldnames for field in required_fields):
                raise ValidationError(
                    f'CSV must contain these columns: {", ".join(required_fields)}'
                )
            
            # Validate each row
            for row_num, row in enumerate(reader, start=2):
                if not row.get('question_text', '').strip():
                    raise ValidationError(f'Row {row_num}: Question text is required')
                if not row.get('topic', '').strip():
                    raise ValidationError(f'Row {row_num}: Topic is required')
                
                # Validate difficulty
                difficulty = row.get('difficulty', '').strip().lower()
                if difficulty not in ['easy', 'medium', 'hard']:
                    raise ValidationError(f'Row {row_num}: Difficulty must be Easy, Medium, or Hard')
                
                # Validate correct answer
                correct_answer = row.get('correct_answer', '').strip().upper()
                if correct_answer not in ['A', 'B', 'C', 'D']:
                    raise ValidationError(f'Row {row_num}: Correct answer must be A, B, C, or D')
                
                # Check if options are provided
                for option in ['option_a', 'option_b', 'option_c', 'option_d']:
                    if not row.get(option, '').strip():
                        raise ValidationError(f'Row {row_num}: {option.replace("_", " ").title()} is required')
                    
        except UnicodeDecodeError:
            raise ValidationError('File must be UTF-8 encoded.')
        except csv.Error as e:
            raise ValidationError(f'Invalid CSV format: {e}')
        
        return csv_file


class QuestionSearchForm(forms.Form):
    """Form for searching questions"""
    
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search questions...',
        })
    )
    
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        required=False,
        empty_label="All Subjects",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    topic = forms.ModelChoiceField(
        queryset=Topic.objects.all(),
        required=False,
        empty_label="All Topics",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    difficulty = forms.ChoiceField(
        choices=[
            ('', 'All Difficulties'),
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    is_active = forms.ChoiceField(
        choices=[
            ('', 'All Questions'),
            ('true', 'Active Only'),
            ('false', 'Inactive Only'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
