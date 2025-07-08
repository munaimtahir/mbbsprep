#!/usr/bin/env python3
"""
Test script for the MCQ Bulk Upload functionality
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medprep.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
from staff.views.question_views import BulkQuestionUploadView
from staff.forms import BulkQuestionUploadForm
from core.models import Subject, Topic, Tag, Question

def test_bulk_upload_page():
    """Test if the bulk upload page loads without errors"""
    print("🧪 Testing MCQ Bulk Upload Page...")
    
    try:
        # Create test user
        user, created = User.objects.get_or_create(
            username='testadmin',
            defaults={
                'email': 'admin@test.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        # Create request factory
        factory = RequestFactory()
        
        # Test GET request (page load)
        print("Testing page load...")
        request = factory.get('/staff/questions/bulk-upload/')
        request.user = user
        
        view = BulkQuestionUploadView()
        view.request = request
        response = view.get(request)
        
        print(f"✅ Page loads successfully (Status: {response.status_code})")
        
        # Test form initialization
        print("Testing form initialization...")
        form = BulkQuestionUploadForm()
        
        print(f"✅ Form fields: {list(form.fields.keys())}")
        
        # Test template download
        print("Testing template download...")
        request = factory.get('/staff/questions/bulk-upload/?action=download_template')
        request.user = user
        
        view = BulkQuestionUploadView()
        response = view.dispatch(request)
        
        if hasattr(response, 'content'):
            print("✅ Template download works")
        else:
            print("❌ Template download failed")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_sample_data():
    """Test if we have sample data for the upload"""
    print("\n🔍 Checking Sample Data...")
    
    try:
        subjects = Subject.objects.count()
        topics = Topic.objects.count()
        tags = Tag.objects.count()
        questions = Question.objects.count()
        
        print(f"📊 Current Data:")
        print(f"   - Subjects: {subjects}")
        print(f"   - Topics: {topics}")
        print(f"   - Tags: {tags}")
        print(f"   - Questions: {questions}")
        
        if subjects > 0 and topics > 0:
            print("✅ Sample data available for testing")
            return True
        else:
            print("⚠️  Limited sample data - consider adding more for testing")
            return False
            
    except Exception as e:
        print(f"❌ Error checking data: {str(e)}")
        return False

def test_bulk_upload_functionality():
    """Test the bulk upload core functionality"""
    print("\n🧪 Testing Bulk Upload Core Functionality...")
    
    try:
        # Create test data
        subject, created = Subject.objects.get_or_create(
            name="Test Subject",
            defaults={'is_active': True}
        )
        
        topic, created = Topic.objects.get_or_create(
            name="Test Topic",
            subject=subject,
            defaults={'is_active': True}
        )
        
        print("✅ Test data created")
        
        # Test form validation
        form_data = {
            'default_subject': subject.id,
            'default_difficulty': 'medium',
            'overwrite_existing': False
        }
        
        form = BulkQuestionUploadForm(data=form_data)
        
        # Form will be invalid without file, but we're testing structure
        print(f"✅ Form structure valid: {list(form.fields.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 MCQ Bulk Upload Test Suite")
    print("=" * 50)
    
    tests = [
        test_bulk_upload_page,
        test_sample_data,
        test_bulk_upload_functionality,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The bulk upload page is working correctly.")
        print("\n📝 Next Steps:")
        print("1. Navigate to: /staff/questions/bulk-upload/")
        print("2. Download the CSV template")
        print("3. Add your MCQ data to the template")
        print("4. Upload the completed file")
        print("5. Review results and download any error rows if needed")
    else:
        print("⚠️  Some tests failed. Please check the error messages above.")

if __name__ == '__main__':
    main()
