#!/usr/bin/env python
"""
Test script for the subjects management page functionality
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medprep.settings')
django.setup()

from core.models import Subject, Topic
from django.contrib.auth import get_user_model
from django.test import Client, RequestFactory
from staff.views.subject_views import SubjectListView

def test_subjects_page():
    """Test the subjects management functionality"""
    print("🧪 Testing Subjects Management Page")
    print("=" * 50)
    
    # Create test data if needed
    print("📚 Creating test subjects...")
    
    # Create some test subjects if they don't exist
    subjects_data = [
        {'name': 'Anatomy', 'code': 'ANAT', 'description': 'Human Anatomy', 'is_active': True},
        {'name': 'Pathology', 'code': 'PATH', 'description': 'General Pathology', 'is_active': True},
        {'name': 'Forensics', 'code': 'FMED', 'description': 'Forensic Medicine', 'is_active': False},
        {'name': 'Pharmacology', 'code': 'PHAR', 'description': 'Medical Pharmacology', 'is_active': True},
    ]
    
    created_subjects = []
    for data in subjects_data:
        subject, created = Subject.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        created_subjects.append(subject)
        print(f"{'✓ Created' if created else '✓ Found'} {subject.name} ({subject.code})")
    
    # Create some topics for subjects
    print("\n📝 Creating test topics...")
    topics_data = [
        {'subject': 'Anatomy', 'topics': ['Head and Neck', 'Thorax', 'Abdomen', 'Pelvis', 'Limbs']},
        {'subject': 'Pathology', 'topics': ['Cell Injury', 'Inflammation', 'Neoplasia', 'Hemodynamics']},
        {'subject': 'Pharmacology', 'topics': ['Pharmacokinetics', 'Pharmacodynamics', 'Autonomic Drugs']},
    ]
    
    for topic_group in topics_data:
        try:
            subject = Subject.objects.get(name=topic_group['subject'])
            for i, topic_name in enumerate(topic_group['topics']):
                topic, created = Topic.objects.get_or_create(
                    subject=subject,
                    name=topic_name,
                    defaults={'order': i + 1, 'is_active': True}
                )
                print(f"  {'✓ Created' if created else '✓ Found'} {topic.name} in {subject.name}")
        except Subject.DoesNotExist:
            print(f"  ❌ Subject {topic_group['subject']} not found")
    
    # Test the view
    print("\n🔍 Testing SubjectListView...")
    factory = RequestFactory()
    request = factory.get('/staff/subjects/')
    
    # Create a staff user for testing
    User = get_user_model()
    try:
        staff_user = User.objects.filter(is_staff=True).first()
        if not staff_user:
            staff_user = User.objects.create_user(
                username='testadmin',
                email='testadmin@test.com',
                password='testpass123',
                first_name='Test',
                last_name='Admin',
                is_staff=True,
                is_superuser=True,
            )
            print("✓ Created test admin user")
        else:
            print(f"✓ Using existing staff user: {staff_user.username}")
    except Exception as e:
        print(f"❌ Error creating/finding staff user: {e}")
        return False
    request.user = staff_user
    
    view = SubjectListView()
    view.setup(request)
    
    # Test queryset
    queryset = view.get_queryset()
    print(f"✓ Found {queryset.count()} subjects in queryset")
    
    # Test context data
    view.object_list = queryset
    context = view.get_context_data(object_list=queryset)
    print(f"✓ Active subjects: {context.get('active_subjects', 0)}")
    print(f"✓ Total topics: {context.get('total_topics', 0)}")
    
    # Test template existence
    print(f"\n📄 Template: {view.template_name}")
    template_path = os.path.join('templates', 'staff', 'subjects', 'subject_list_new.html')
    if os.path.exists(template_path):
        print("✓ Template file exists")
    else:
        print("❌ Template file not found")
    
    # Test static files
    print(f"\n🎨 Static Files:")
    css_path = os.path.join('static', 'staff', 'css', 'subjects.css')
    js_path = os.path.join('static', 'staff', 'js', 'subjects.js')
    shared_js_path = os.path.join('static', 'staff', 'js', 'subjects_shared.js')
    
    for file_path, name in [(css_path, 'CSS'), (js_path, 'JavaScript'), (shared_js_path, 'Shared JS')]:
        if os.path.exists(file_path):
            print(f"✓ {name} file exists: {file_path}")
        else:
            print(f"❌ {name} file not found: {file_path}")
    
    # Summary
    print(f"\n📊 Summary:")
    print(f"✓ Total subjects: {Subject.objects.count()}")
    print(f"✓ Active subjects: {Subject.objects.filter(is_active=True).count()}")
    print(f"✓ Archived subjects: {Subject.objects.filter(is_active=False).count()}")
    print(f"✓ Total topics: {Topic.objects.count()}")
    
    print(f"\n🌐 URL Testing:")
    print(f"Main page: http://localhost:8000/staff/subjects/")
    print(f"Template used: {view.template_name}")
    
    print(f"\n✅ Subjects management page test completed!")
    print(f"You can now visit: http://localhost:8000/staff/subjects/")
    return True

if __name__ == '__main__':
    try:
        test_subjects_page()
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
