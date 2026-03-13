#!/usr/bin/env python3
"""
Simple system verification for MedPrep Admin
Tests basic imports and model access
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medprep.settings')
django.setup()

def test_models():
    """Test that all models can be imported and accessed"""
    try:
        from core.models.academic_models import Subject, Topic, Question, Option
        from core.models.user_models import UserProfile
        from core.models.tag_models import Tag, Subtag
        from core.models.resource_models import Note, VideoResource, Flashcard
        from core.models.subscription_models import SubscriptionPlan, PaymentProof
        
        print("✅ All models imported successfully")
        
        # Test model counts
        print(f"📊 Model Statistics:")
        print(f"   - Subjects: {Subject.objects.count()}")
        print(f"   - Topics: {Topic.objects.count()}")
        print(f"   - Questions: {Question.objects.count()}")
        print(f"   - Tags: {Tag.objects.count()}")
        print(f"   - Users: {UserProfile.objects.count()}")
        print(f"   - Notes: {Note.objects.count()}")
        print(f"   - Videos: {VideoResource.objects.count()}")
        print(f"   - Flashcards: {Flashcard.objects.count()}")
        
        return True
    except Exception as e:
        print(f"❌ Model import error: {e}")
        return False

def test_forms():
    """Test that all forms can be imported"""
    try:
        from staff.forms import (
            TopicBulkUploadForm, StaffLoginForm, UserSearchForm,
            UserCreateForm, UserEditForm, BulkUserUploadForm,
            QuestionForm, OptionFormSet, BulkQuestionUploadForm,
            TagForm, SubtagForm, NoteForm, VideoResourceForm,
            FlashcardForm, PaymentReviewForm, SubscriptionPlanForm
        )
        
        print("✅ All forms imported successfully")
        return True
    except Exception as e:
        print(f"❌ Form import error: {e}")
        return False

def test_urls():
    """Test that URL patterns work"""
    try:
        from django.urls import reverse
        from django.test import Client
        
        # Test some basic URL reversals
        urls_to_test = [
            'staff:login',
            'staff:dashboard',
            'staff:user_list',
            'staff:topic_list',
            'staff:tag_list',
        ]
        
        for url_name in urls_to_test:
            try:
                reverse(url_name)
                print(f"✅ URL {url_name} resolved successfully")
            except Exception as e:
                print(f"❌ URL {url_name} error: {e}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ URL test error: {e}")
        return False

def main():
    """Run all verification tests"""
    print("🚀 Starting MedPrep Admin System Verification")
    print("=" * 50)
    
    tests = [
        ("Model Import Test", test_models),
        ("Form Import Test", test_forms),
        ("URL Pattern Test", test_urls),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"🎯 VERIFICATION RESULTS: {passed}/{total} ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! System is ready for use.")
        print("\nTo start the server:")
        print("  python manage.py runserver")
        print("\nAccess the admin at:")
        print("  http://127.0.0.1:8000/staff/login/")
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()
