#!/usr/bin/env python3
"""
Test script for MCQ Edit functionality
Tests all edit operations including form validation, option management, and delete/reset actions
"""

import os
import sys
import django
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medprep.settings')
django.setup()

from core.models import Question, Option, Subject, Topic, Tag
from django.contrib.auth.models import User

def test_edit_mcq_functionality():
    """Test complete MCQ edit functionality"""
    print("🔧 Testing MCQ Edit Functionality")
    print("=" * 50)
    
    # Setup test client
    client = Client()
    
    # Create test admin user
    User = get_user_model()
    admin_user, created = User.objects.get_or_create(
        username='testadmin',
        defaults={
            'first_name': 'Test',
            'last_name': 'Admin',
            'email': 'testadmin@example.com',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created:
        admin_user.set_password('testpass123')
        admin_user.save()
        print(f"✅ Created test admin user: {admin_user.username}")
    
    # Login as admin
    login_success = client.login(username='testadmin', password='testpass123')
    if not login_success:
        print("❌ Failed to login as admin")
        return False
    print("✅ Logged in as admin")
    
    # Ensure we have test data
    setup_test_data()
    
    # Get a test question
    question = Question.objects.first()
    if not question:
        print("❌ No test questions found")
        return False
    
    print(f"📝 Testing with question: {question.question_text[:50]}...")
    
    # Test 1: Access edit page
    print("\n1. Testing edit page access...")
    edit_url = reverse('staff:question_edit', kwargs={'pk': question.pk})
    response = client.get(edit_url)
    
    if response.status_code == 200:
        print("✅ Edit page accessible")
        print(f"   URL: {edit_url}")
    else:
        print(f"❌ Edit page access failed: {response.status_code}")
        return False
    
    # Test 2: Check form pre-population
    print("\n2. Testing form pre-population...")
    content = response.content.decode()
    
    checks = [
        (question.question_text in content, "Question text pre-filled"),
        (question.topic.name in content, "Topic pre-selected"),
        (str(question.difficulty) in content, "Difficulty pre-selected"),
        (question.explanation in content, "Explanation pre-filled")
    ]
    
    for check, description in checks:
        if check:
            print(f"✅ {description}")
        else:
            print(f"❌ {description}")
    
    # Test 3: Test option editing
    print("\n3. Testing option editing...")
    
    # Get CSRF token from the form
    csrf_token = None
    content = response.content.decode()
    import re
    csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', content)
    if csrf_match:
        csrf_token = csrf_match.group(1)
    
    # Prepare updated data
    options = list(question.options.all().order_by('order'))
    updated_data = {
        'csrfmiddlewaretoken': csrf_token,
        'subject': question.topic.subject.id,  # Add subject field
        'question_text': 'Updated test question for cardiovascular system?',
        'topic': question.topic.id,
        'difficulty': 'medium',
        'explanation': 'Updated explanation for this question.',
        'reference': 'Updated Reference Book, Page 123',
        'tags': [tag.id for tag in question.tags.all()],
        'is_active': True,
        'correct_answer': '1',  # Second option
        'option_0_text': 'Updated Option A',
        'option_1_text': 'Updated Option B (Correct)',
        'option_2_text': 'Updated Option C',
        'option_3_text': 'Updated Option D',
    }
    
    response = client.post(edit_url, updated_data)
    
    if response.status_code == 302:  # Redirect on success
        print("✅ MCQ update successful")
        
        # Verify the update
        updated_question = Question.objects.get(pk=question.pk)
        print(f"   Updated question text: {updated_question.question_text[:50]}...")
        print(f"   Updated difficulty: {updated_question.difficulty}")
        
        # Check options
        updated_options = list(updated_question.options.all().order_by('order'))
        print(f"   Options count: {len(updated_options)}")
        
        correct_option = updated_question.options.filter(is_correct=True).first()
        if correct_option:
            print(f"   Correct option: {correct_option.option_text}")
        
    else:
        print(f"❌ MCQ update failed: {response.status_code}")
        content = response.content.decode()
        print(f"   Response content length: {len(content)} chars")
        
        # Check for form errors in the response
        if 'error' in content.lower():
            print("   Form contains errors")
        if 'required' in content.lower():
            print("   Form has required field errors")
            
        # Try to extract any visible error messages
        if 'class="alert' in content:
            print("   Alert messages found in response")
            
        if hasattr(response, 'context') and response.context and 'form' in response.context:
            form = response.context['form']
            if form.errors:
                print(f"   Form errors: {form.errors}")
        
        # Save response for debugging
        with open('debug_edit_response.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("   Response saved to debug_edit_response.html")
    
    # Test 4: Test reset functionality
    print("\n4. Testing reset functionality...")
    reset_data = {
        'reset_form': 'true'
    }
    
    response = client.post(edit_url, reset_data)
    if response.status_code == 302:
        print("✅ Reset functionality working")
    else:
        print(f"❌ Reset failed: {response.status_code}")
    
    # Test 5: Test validation errors
    print("\n5. Testing validation errors...")
    
    # Test with invalid data (no options)
    invalid_data = {
        'question_text': 'Invalid question?',
        'topic': question.topic.id,
        'difficulty': 'easy',
        'explanation': 'Test explanation',
        'correct_answer': '0',
    }
    
    response = client.post(edit_url, invalid_data)
    if response.status_code == 200:  # Should stay on page with errors
        print("✅ Validation errors handled correctly")
    else:
        print(f"❌ Validation error handling failed: {response.status_code}")
    
    # Test 6: Test delete functionality
    print("\n6. Testing delete functionality...")
    
    # Create a test question to delete
    test_subject = Subject.objects.first()
    test_topic = Topic.objects.filter(subject=test_subject).first()
    
    delete_question = Question.objects.create(
        question_text="Test question for deletion?",
        topic=test_topic,
        difficulty='easy',
        explanation='Test explanation for deletion.',
        reference='Test reference'
    )
    
    # Add options
    Option.objects.create(question=delete_question, option_text='Option A', is_correct=True, order=1)
    Option.objects.create(question=delete_question, option_text='Option B', is_correct=False, order=2)
    
    delete_url = reverse('staff:question_edit', kwargs={'pk': delete_question.pk})
    delete_data = {
        'delete_mcq': 'true'
    }
    
    response = client.post(delete_url, delete_data)
    if response.status_code == 302:  # Redirect on success
        # Check if question was deleted
        if not Question.objects.filter(pk=delete_question.pk).exists():
            print("✅ Delete functionality working")
        else:
            print("❌ Question not deleted")
    else:
        print(f"❌ Delete failed: {response.status_code}")
    
    print("\n" + "=" * 50)
    print("🎉 MCQ Edit functionality test completed!")
    return True

def setup_test_data():
    """Setup test data for MCQ testing"""
    # Create test subject if not exists
    subject, created = Subject.objects.get_or_create(
        name='Test Subject',
        defaults={'description': 'Test subject for MCQ testing'}
    )
    
    # Create test topic if not exists
    topic, created = Topic.objects.get_or_create(
        name='Test Topic',
        subject=subject,
        defaults={'description': 'Test topic for MCQ testing'}
    )
    
    # Create test tags
    tag1, created = Tag.objects.get_or_create(name='test-tag-1')
    tag2, created = Tag.objects.get_or_create(name='test-tag-2')
    
    # Create test question if not exists
    if not Question.objects.filter(question_text__contains='Test question for editing').exists():
        question = Question.objects.create(
            question_text='Test question for editing - What is the cardiovascular system?',
            topic=topic,
            difficulty='easy',
            explanation='Test explanation for editing.',
            reference='Test Reference Book, Page 100'
        )
        
        # Add tags
        question.tags.add(tag1, tag2)
        
        # Add options
        Option.objects.create(question=question, option_text='Heart and blood vessels', is_correct=True, order=1)
        Option.objects.create(question=question, option_text='Lungs and airways', is_correct=False, order=2)
        Option.objects.create(question=question, option_text='Brain and nerves', is_correct=False, order=3)
        Option.objects.create(question=question, option_text='Bones and muscles', is_correct=False, order=4)
        
        print(f"✅ Created test question: {question.question_text[:50]}...")

if __name__ == '__main__':
    test_edit_mcq_functionality()
