#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medprep.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

User = get_user_model()

def test_bulk_upload_detailed():
    """Test bulk upload with detailed error reporting"""
    client = Client()
    
    # Login first
    staff_user = User.objects.filter(is_staff=True).first()
    staff_user.set_password('testpass123')
    staff_user.save()
    client.force_login(staff_user)
    
    print("✅ Logged in successfully")
    
    # Get the form first
    response = client.get(reverse('staff:topic_bulk_upload'))
    print(f"GET bulk upload page: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ Could not access bulk upload page")
        return
    
    # Create test CSV with correct format based on form help text
    csv_content = """LOs,Sub-Topic,Topic,Subject,Type,Module,Assessment
Test Learning Objective,Test Sub Topic,Test Topic,Test Subject,Test Type,Test Module,Test Assessment"""
    
    csv_file = SimpleUploadedFile(
        "test_topics.csv",
        csv_content.encode('utf-8'),
        content_type="text/csv"
    )
    
    upload_data = {
        'csv_file': csv_file,
        'create_subjects': True,
        'create_tags': True
    }
    
    print("Submitting bulk upload...")
    response = client.post(reverse('staff:topic_bulk_upload'), data=upload_data)
    
    print(f"POST response status: {response.status_code}")
    
    if response.status_code == 200:
        print("❌ Form submission failed - check for errors")
        if hasattr(response, 'context') and response.context:
            if 'form' in response.context:
                form = response.context['form']
                if form.errors:
                    print(f"Form errors: {form.errors}")
                else:
                    print("No form errors found")
            
            # Check for messages
            if 'messages' in response.context:
                messages = list(response.context['messages'])
                if messages:
                    for msg in messages:
                        print(f"Message: {msg}")
        
        # Print first part of response content to see what's happening
        content = response.content.decode('utf-8')
        if 'error' in content.lower() or 'traceback' in content.lower():
            print("Response contains errors:")
            print(content[:1000])
    elif response.status_code == 302:
        print(f"✅ Success! Redirected to: {response.url}")
    else:
        print(f"❌ Unexpected status: {response.status_code}")

if __name__ == '__main__':
    print("🔍 Testing bulk upload in detail...")
    test_bulk_upload_detailed()
