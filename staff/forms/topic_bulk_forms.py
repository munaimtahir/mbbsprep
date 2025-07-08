from django import forms
from django.core.exceptions import ValidationError
import csv
import io


class TopicBulkUploadForm(forms.Form):
    """Form for bulk uploading topics from CSV"""
    
    csv_file = forms.FileField(
        label="CSV File",
        help_text="Upload a CSV file with columns: LOs, Sub-Topic, Topic, Subject, Type, Module, Assessment",
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv'
        })
    )
    
    create_subjects = forms.BooleanField(
        required=False,
        initial=True,
        label="Create new subjects if they don't exist",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    create_tags = forms.BooleanField(
        required=False,
        initial=True,
        label="Create tags from Topic, Sub-Topic, Type, Module, Assessment columns",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def clean_csv_file(self):
        file = self.cleaned_data.get('csv_file')
        
        if not file:
            raise ValidationError("Please upload a CSV file.")
        
        if not file.name.endswith('.csv'):
            raise ValidationError("File must be a CSV file.")
        
        # Read and validate CSV structure
        try:
            file.seek(0)
            content = file.read().decode('utf-8-sig')  # Handle BOM
            csv_reader = csv.DictReader(io.StringIO(content))
            
            required_columns = ['LOs', 'Sub-Topic', 'Topic', 'Subject', 'Type', 'Module', 'Assessment']
            
            # Check if all required columns exist
            fieldnames = csv_reader.fieldnames
            missing_columns = [col for col in required_columns if col not in fieldnames]
            
            if missing_columns:
                raise ValidationError(f"Missing required columns: {', '.join(missing_columns)}")
            
            # Validate that there's at least one row of data
            rows = list(csv_reader)
            if not rows:
                raise ValidationError("CSV file appears to be empty or contains only headers.")
            
            # Reset file pointer for later processing
            file.seek(0)
            
        except UnicodeDecodeError:
            raise ValidationError("File encoding error. Please ensure the CSV file is saved with UTF-8 encoding.")
        except csv.Error as e:
            raise ValidationError(f"CSV parsing error: {str(e)}")
        except Exception as e:
            raise ValidationError(f"Error reading CSV file: {str(e)}")
        
        return file
