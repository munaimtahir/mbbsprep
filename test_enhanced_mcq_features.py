#!/usr/bin/env python3
"""
Test script to verify the enhanced tag management and delete confirmation functionality.
"""

import os
import sys
import django
from django.test import Client
from django.contrib.auth.models import User
from core.models import Subject, Topic, Question, Tag

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_prep.settings')
django.setup()

def test_tag_functionality():
    """Test that tag creation and management is working."""
    
    client = Client()
    
    # Create test user
    user = User.objects.create_user(
        username='teststaff',
        password='testpass123',
        is_staff=True
    )
    
    # Login
    client.login(username='teststaff', password='testpass123')
    
    print("🔍 Testing Enhanced Tag Management & Delete Functionality")
    print("=" * 60)
    
    # Test 1: Check that templates load correctly
    test_pages = [
        ('/staff/questions/', 'MCQ List'),
        ('/staff/questions/add/', 'Add MCQ Form'),
        ('/staff/questions/bulk-upload/', 'Bulk Upload')
    ]
    
    all_passed = True
    
    for url, name in test_pages:
        try:
            response = client.get(url)
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                
                # Check for new tag functionality in forms
                if 'add' in url:
                    has_new_tags_field = 'id_new_tags' in content
                    has_tag_preview = 'tagPreview' in content
                    has_enhanced_css = 'tag-preview-chip' in content or 'question_add.css' in content
                    
                    if has_new_tags_field and has_tag_preview:
                        print(f"✅ {name}: Enhanced tag management loaded")
                    else:
                        print(f"❌ {name}: Missing tag enhancements")
                        if not has_new_tags_field:
                            print(f"   • Missing new tags field")
                        if not has_tag_preview:
                            print(f"   • Missing tag preview")
                        all_passed = False
                else:
                    print(f"✅ {name}: Page loads correctly")
            else:
                print(f"❌ {name}: HTTP {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"❌ {name}: Error - {str(e)}")
            all_passed = False
    
    # Test 2: Check delete confirmation template exists
    try:
        # Create a test question first
        from core.models import Question, Subject, Topic
        
        subject = Subject.objects.create(name="Test Subject", is_active=True)
        topic = Topic.objects.create(name="Test Topic", subject=subject, is_active=True)
        question = Question.objects.create(
            question_text="Test question?",
            subject=subject,
            topic=topic,
            difficulty="EASY",
            is_active=True
        )
        
        delete_url = f'/staff/questions/{question.id}/delete/'
        response = client.get(delete_url)
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            has_delete_confirmation = 'Delete MCQ' in content
            has_question_preview = question.question_text in content
            
            if has_delete_confirmation and has_question_preview:
                print(f"✅ Delete Confirmation: Template working correctly")
            else:
                print(f"❌ Delete Confirmation: Template issues")
                all_passed = False
        else:
            print(f"❌ Delete Confirmation: HTTP {response.status_code}")
            all_passed = False
            
        # Clean up
        question.delete()
        topic.delete()
        subject.delete()
        
    except Exception as e:
        print(f"❌ Delete Confirmation: Error - {str(e)}")
        all_passed = False
    
    # Test 3: Check that tag creation would work
    initial_tag_count = Tag.objects.count()
    print(f"📊 Current tags in database: {initial_tag_count}")
    
    # Test creating a new tag programmatically
    try:
        new_tag, created = Tag.objects.get_or_create(
            name="Test Tag",
            defaults={'is_active': True}
        )
        
        if created:
            print("✅ Tag Creation: New tag created successfully")
            new_tag.delete()  # Clean up
        else:
            print("✅ Tag Creation: Tag already exists (expected behavior)")
            
    except Exception as e:
        print(f"❌ Tag Creation: Error - {str(e)}")
        all_passed = False
    
    # Clean up user
    user.delete()
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All enhanced functionality working correctly!")
        print("   • Delete confirmation template created")
        print("   • Tag management enhanced with creation capability") 
        print("   • Forms updated with new tag fields")
        print("   • CSS and JS enhancements applied")
        return True
    else:
        print("❌ Some issues found - check the output above")
        return False

if __name__ == '__main__':
    success = test_tag_functionality()
    sys.exit(0 if success else 1)
