#!/usr/bin/env python
import os
import sys

# Setup Django
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'medprep.settings'

import django
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

User = get_user_model()

def test_bulk_upload():
    """Test bulk upload exactly like the verification script"""
    client = Client()
    
    # Login first
    staff_user = User.objects.filter(is_staff=True).first()
    staff_user.set_password('testpass123')
    staff_user.save()
    client.force_login(staff_user)
    
    # Create test CSV with correct format
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
    
    print("Submitting bulk upload...")
    response = client.post(reverse('staff:topic_bulk_upload'), data=upload_data, files=upload_files)
    
    print(f"Response status: {response.status_code}")
    
    if response.status_code == 200:
        print("❌ Form returned 200 - checking for errors")
        if hasattr(response, 'context') and response.context:
            if 'form' in response.context:
                form = response.context['form']
                if form.errors:
                    print(f"Form errors: {form.errors}")
                else:
                    print("No form errors")
            
            if 'messages' in response.context:
                messages = list(response.context['messages'])
                for msg in messages:
                    print(f"Message: {msg}")
    elif response.status_code == 302:
        print(f"✅ Redirected to: {response.url}")
    
    return response.status_code == 302

if __name__ == '__main__':
    print("🔍 Testing bulk upload...")
    success = test_bulk_upload()
    print(f"Result: {'✅ SUCCESS' if success else '❌ FAILED'}")
