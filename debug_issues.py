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

def test_login_form():
    """Test login form submission"""
    client = Client()
    
    # Get staff user
    try:
        staff_user = User.objects.filter(is_staff=True).first()
        if not staff_user:
            print("❌ No staff user found")
            return
        
        print(f"✅ Testing with staff user: {staff_user.username}")
        
        # Test login form
        login_data = {'username': staff_user.username, 'password': 'testpass123'}
        response = client.post(reverse('staff:login'), data=login_data)
        
        print(f"Login response status: {response.status_code}")
        if response.status_code == 200:
            print("❌ Login failed - form returned 200 instead of redirect")
            if hasattr(response, 'context') and response.context and 'form' in response.context:
                form = response.context['form']
                if form.errors:
                    print(f"Form errors: {form.errors}")
        elif response.status_code == 302:
            print(f"✅ Login successful - redirected to: {response.url}")
    
    except Exception as e:
        print(f"❌ Error testing login: {e}")

def test_ajax_tag_create():
    """Test AJAX tag creation"""
    client = Client()
    
    # Login first
    staff_user = User.objects.filter(is_staff=True).first()
    client.force_login(staff_user)
    
    # Test AJAX tag create
    tag_data = {'name': 'Test Tag', 'color': '#FF0000'}
    response = client.post(reverse('staff:ajax_tag_create'), data=tag_data)
    
    print(f"AJAX Tag Create response status: {response.status_code}")
    if response.status_code != 200:
        print(f"❌ AJAX Tag Create failed with status {response.status_code}")
        print(f"Response content: {response.content.decode()}")

def test_bulk_upload():
    """Test topic bulk upload"""
    client = Client()
    
    # Login first
    staff_user = User.objects.filter(is_staff=True).first()
    client.force_login(staff_user)
    
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
    response = client.post(reverse('staff:topic_bulk_upload'), data=upload_data)
    
    print(f"Bulk Upload response status: {response.status_code}")
    if response.status_code == 200:
        print("❌ Bulk upload failed - form returned 200 instead of redirect")
        if hasattr(response, 'context') and response.context and 'form' in response.context:
            form = response.context['form']
            if form.errors:
                print(f"Form errors: {form.errors}")
            else:
                print("No form errors found")
        print("Response content (first 500 chars):", response.content.decode()[:500])

if __name__ == '__main__':
    print("🔍 Debugging specific issues...")
    test_login_form()
    test_ajax_tag_create()
    test_bulk_upload()
