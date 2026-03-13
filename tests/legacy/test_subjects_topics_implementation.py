#!/usr/bin/env python
"""
Django Test Script for New Subjects & Topics Management Pages
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to the path
PROJECT_DIR = Path(__file__).parent
sys.path.insert(0, str(PROJECT_DIR))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medprep.settings')

try:
    django.setup()
except Exception as e:
    print(f"Error setting up Django: {e}")
    sys.exit(1)

def test_views_import():
    """Test if all new views can be imported"""
    print("🔍 Testing view imports...")
    
    try:
        from staff.views.subject_views import (
            SubjectListView, 
            TopicListEnhancedView,
            TopicCreateAjaxEnhancedView,
            TopicEditAjaxEnhancedView,
            TopicToggleStatusView,
            TopicDeleteView
        )
        print("✅ All new views imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_templates():
    """Test if all templates exist"""
    print("\n🔍 Testing template files...")
    
    templates = [
        'templates/staff/subjects/subject_form.html',
        'templates/staff/topics/topic_list_new.html', 
        'templates/staff/topics/topic_form.html'
    ]
    
    all_exist = True
    for template in templates:
        path = PROJECT_DIR / template
        if path.exists():
            print(f"✅ {template}")
        else:
            print(f"❌ {template} - MISSING")
            all_exist = False
    
    return all_exist

def test_static_files():
    """Test if all static files exist"""
    print("\n🔍 Testing static files...")
    
    static_files = [
        'static/staff/css/subjects.css',
        'static/staff/css/subject_form.css',
        'static/staff/css/topics.css',
        'static/staff/js/subjects.js',
        'static/staff/js/subject_form.js', 
        'static/staff/js/topics.js',
        'static/staff/js/topic_form.js',
        'static/staff/js/subjects_shared.js',
        'static/staff/js/topics_shared.js'
    ]
    
    all_exist = True
    for static_file in static_files:
        path = PROJECT_DIR / static_file
        if path.exists():
            print(f"✅ {static_file}")
        else:
            print(f"❌ {static_file} - MISSING")
            all_exist = False
    
    return all_exist

def test_models():
    """Test if required models exist"""
    print("\n🔍 Testing model access...")
    
    try:
        from core.models import Subject, Topic
        
        # Test basic model operations
        subjects_count = Subject.objects.count()
        topics_count = Topic.objects.count()
        
        print(f"✅ Subjects model: {subjects_count} records")
        print(f"✅ Topics model: {topics_count} records")
        return True
    except Exception as e:
        print(f"❌ Model error: {e}")
        return False

def test_urls():
    """Test if URL patterns are correctly configured"""
    print("\n🔍 Testing URL configuration...")
    
    try:
        from django.urls import reverse
        
        # Test basic URL reversal
        urls_to_test = [
            'staff:subject_list',
            'staff:topic_list',
            'staff:subject_add',
            'staff:topic_add'
        ]
        
        for url_name in urls_to_test:
            try:
                url = reverse(url_name)
                print(f"✅ {url_name} -> {url}")
            except Exception as e:
                print(f"❌ {url_name} - Error: {e}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ URL configuration error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing New Subjects & Topics Management Implementation")
    print("=" * 60)
    
    tests = [
        ("Views Import", test_views_import),
        ("Templates", test_templates), 
        ("Static Files", test_static_files),
        ("Models", test_models),
        ("URLs", test_urls)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! The implementation looks good.")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
