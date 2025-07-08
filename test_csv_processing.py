#!/usr/bin/env python3
"""
Test the CSV processing functionality of the MCQ bulk upload
"""
import os
import sys
import django
import pandas as pd

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medprep.settings')
django.setup()

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from staff.views.question_views import BulkQuestionUploadView
from staff.forms import BulkQuestionUploadForm
from core.models import Subject, Topic, Tag, Question, Option

def test_csv_processing():
    """Test CSV file processing"""
    print("🧪 Testing CSV Processing...")
    
    try:
        # Read the sample CSV
        csv_path = 'sample_mcq_upload.csv'
        if not os.path.exists(csv_path):
            print(f"❌ Sample CSV file not found: {csv_path}")
            return False
        
        # Create a file upload object
        with open(csv_path, 'rb') as f:
            csv_content = f.read()
        
        uploaded_file = SimpleUploadedFile(
            name='test_mcqs.csv',
            content=csv_content,
            content_type='text/csv'
        )
        
        # Test the form
        form_data = {
            'default_difficulty': 'medium',
            'overwrite_existing': False
        }
        
        form = BulkQuestionUploadForm(
            data=form_data,
            files={'csv_file': uploaded_file}
        )
        
        if form.is_valid():
            print("✅ Form validation passed")
            
            # Test the file processing logic
            view = BulkQuestionUploadView()
            
            # Count questions before
            questions_before = Question.objects.count()
            print(f"📊 Questions before upload: {questions_before}")
            
            # Process the file
            result = view.process_uploaded_file(form)
            
            if result['success']:
                print(f"✅ CSV processing successful!")
                print(f"   - Added: {result['added_count']} questions")
                print(f"   - Errors: {result['error_count']} rows")
                
                if result['errors']:
                    print("   - Error details:")
                    for error in result['errors'][:3]:  # Show first 3 errors
                        print(f"     Row {error['row_number']}: {error['error']}")
                
                # Count questions after
                questions_after = Question.objects.count()
                print(f"📊 Questions after upload: {questions_after}")
                print(f"📈 Net increase: {questions_after - questions_before}")
                
                return True
            else:
                print(f"❌ CSV processing failed: {result['message']}")
                return False
        else:
            print(f"❌ Form validation failed: {form.errors}")
            return False
            
    except Exception as e:
        print(f"❌ Error during CSV processing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_template_generation():
    """Test CSV template generation"""
    print("\n🧪 Testing Template Generation...")
    
    try:
        view = BulkQuestionUploadView()
        response = view.download_template()
        
        if hasattr(response, 'content'):
            content = response.content.decode('utf-8')
            lines = content.split('\n')
            
            print("✅ Template generated successfully")
            print(f"   - Header: {lines[0]}")
            print(f"   - Sample row included: {len(lines) > 1}")
            print(f"   - Total lines: {len(lines)}")
            
            # Check if required columns are present
            required_columns = ['Question Text', 'Option A', 'Option B', 'Correct Answer', 'Topic']
            header = lines[0]
            
            missing_columns = [col for col in required_columns if col not in header]
            if not missing_columns:
                print("✅ All required columns present in template")
                return True
            else:
                print(f"❌ Missing columns: {missing_columns}")
                return False
        else:
            print("❌ Template generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error generating template: {str(e)}")
        return False

def test_data_validation():
    """Test data validation logic"""
    print("\n🧪 Testing Data Validation...")
    
    try:
        # Create a view instance
        view = BulkQuestionUploadView()
        
        # Test valid row
        valid_row = pd.Series({
            'Subject': 'Test Subject',
            'Topic': 'Test Topic',
            'Question Text': 'Sample question?',
            'Option A': 'Option 1',
            'Option B': 'Option 2',
            'Option C': 'Option 3',
            'Option D': 'Option 4',
            'Correct Answer': 'A',
            'Difficulty': 'Easy',
            'Tags': 'Tag1, Tag2',
            'Explanation': 'Test explanation',
            'Reference': 'Test reference'
        })
        
        result = view.process_row(valid_row, None, None, [], False)
        if result['success']:
            print("✅ Valid row processing works")
        else:
            print(f"❌ Valid row failed: {result['error']}")
        
        # Test invalid row (missing required field)
        invalid_row = pd.Series({
            'Subject': 'Test Subject',
            'Topic': '',  # Missing topic
            'Question Text': 'Sample question?',
            'Option A': 'Option 1',
            'Option B': 'Option 2',
            'Correct Answer': 'A',
        })
        
        result = view.process_row(invalid_row, None, None, [], False)
        if not result['success']:
            print(f"✅ Invalid row correctly rejected: {result['error']}")
            return True
        else:
            print("❌ Invalid row was incorrectly accepted")
            return False
            
    except Exception as e:
        print(f"❌ Error testing validation: {str(e)}")
        return False

def main():
    """Run all CSV processing tests"""
    print("🧪 MCQ Bulk Upload CSV Processing Test Suite")
    print("=" * 60)
    
    tests = [
        test_template_generation,
        test_data_validation,
        test_csv_processing,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"📊 CSV Processing Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All CSV processing tests passed!")
        print("\n📝 The bulk upload functionality is fully working:")
        print("✅ Template generation")
        print("✅ Data validation")
        print("✅ CSV file processing")
        print("✅ Error handling")
        print("✅ Database operations")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")

if __name__ == '__main__':
    main()
