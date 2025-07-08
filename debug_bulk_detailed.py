#!/usr/bin/env python
import os
import sys

# Setup Django
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = current_dir
sys.path.insert(0, project_dir)

# Clean environment
if 'DJANGO_SETTINGS_MODULE' in os.environ:
    del os.environ['DJANGO_SETTINGS_MODULE']
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medprep.settings')

import django
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

User = get_user_model()

def debug_bulk_upload():
    """Debug bulk upload exactly like verification"""
    client = Client()
    
    # Login first
    staff_user = User.objects.filter(is_staff=True).first()
    staff_user.set_password('testpass123')
    staff_user.save()
    client.force_login(staff_user)
    
    print("✅ Logged in successfully")
    
    # Test GET first
    get_response = client.get(reverse('staff:topic_bulk_upload'))
    print(f"GET response: {get_response.status_code}")
    
    # Create test CSV with exact same format as verification
    csv_content = """LOs,Sub-Topic,Topic,Subject,Type,Module,Assessment
Test Learning Objective,Test Sub Topic,Test Topic,Test Subject,Test Type,Test Module,Test Assessment"""
    
    csv_file = SimpleUploadedFile(
        "test_topics.csv",
        csv_content.encode('utf-8'),
        content_type="text/csv"
    )
    
    upload_data = {
        'create_subjects': True,
        'create_tags': True
    }
    upload_files = {'csv_file': csv_file}
    
    print("Submitting POST request...")
    response = client.post(reverse('staff:topic_bulk_upload'), data=upload_data, files=upload_files)
    
    print(f"POST response status: {response.status_code}")
    
    if response.status_code == 200:
        print("❌ Form validation failed or processing error")
        if hasattr(response, 'context') and response.context:
            if 'form' in response.context:
                form = response.context['form']
                print(f"Form errors: {form.errors}")
                print(f"Form non-field errors: {form.non_field_errors()}")
                    
                # Check if form is bound and valid
                print(f"Form is bound: {form.is_bound}")
                if form.is_bound:
                    print(f"Form is valid: {form.is_valid()}")
                    print(f"Form cleaned_data: {getattr(form, 'cleaned_data', 'Not available')}")
            else:
                print("No form in context")
            
            if 'messages' in response.context:
                messages = list(response.context['messages'])
                if messages:
                    for msg in messages:
                        print(f"Message: {msg.message} (level: {msg.level_tag})")
                else:
                    print("No messages")
            else:
                print("No messages in context")
        else:
            print("No context in response")
        
        # Check response content for any exceptions
        content = response.content.decode('utf-8')
        if 'exception' in content.lower() or 'error' in content.lower()[:1000]:
            print("Response contains error indicators")
    elif response.status_code == 302:
        print(f"✅ Redirected to: {response.url}")
        return True
    else:
        print(f"❌ Unexpected status: {response.status_code}")
    
    return False

if __name__ == '__main__':
    print("🔍 Debugging bulk upload...")
    success = debug_bulk_upload()
    print(f"Result: {'✅ SUCCESS' if success else '❌ FAILED'}")
