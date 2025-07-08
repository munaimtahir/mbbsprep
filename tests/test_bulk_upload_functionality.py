#!/usr/bin/env python3
"""
Test bulk upload functionality
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medprep.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Subject, Topic, Tag


def test_bulk_upload():
    """Test the bulk upload functionality"""
    print("🧪 Testing Bulk Upload Functionality...")
    
    # Create admin user and login
    client = Client()
    admin_user, created = User.objects.get_or_create(
        username='test_admin_bulk',
        defaults={
            'email': 'admin@test.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('testpass123')
        admin_user.save()
    
    client.login(username='test_admin_bulk', password='testpass123')
    
    # Test CSV upload
    print("📤 Testing CSV file upload...")
    
    with open('test_topics_upload.csv', 'rb') as csv_file:
        response = client.post(reverse('staff:topic_bulk_upload'), {
            'csv_file': csv_file,
            'create_subjects': True,
            'create_tags': True
        })
    
    print(f"Upload response status: {response.status_code}")
    
    if response.status_code == 302:  # Redirect after successful upload
        print("✅ Upload successful (redirected)")
        
        # Check if data was created
        biochemistry_subject = Subject.objects.filter(name='Biochemistry').first()
        physiology_subject = Subject.objects.filter(name='Physiology').first()
        
        if biochemistry_subject:
            print(f"✅ Biochemistry subject created: {biochemistry_subject}")
        else:
            print("❌ Biochemistry subject not found")
        
        if physiology_subject:
            print(f"✅ Physiology subject created: {physiology_subject}")
        else:
            print("❌ Physiology subject not found")
        
        # Check topics
        topics = Topic.objects.filter(subject__in=[biochemistry_subject, physiology_subject])
        print(f"✅ Created {topics.count()} topics")
        
        for topic in topics:
            print(f"  - {topic.name} ({topic.subject.name})")
        
        # Check tags
        tags = Tag.objects.filter(name__contains='Topic:')
        print(f"✅ Created {tags.count()} topic tags")
        
        for tag in tags:
            print(f"  - {tag.name}")
        
    else:
        print(f"❌ Upload failed with status {response.status_code}")
        print(response.content.decode())


if __name__ == "__main__":
    test_bulk_upload()
