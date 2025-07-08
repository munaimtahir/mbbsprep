#!/usr/bin/env python
"""
Test script to verify the fixes for:
1. Topic buttons functionality
2. Subject button state updates
3. Search icon positioning
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
PROJECT_DIR = Path(__file__).parent
sys.path.insert(0, str(PROJECT_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medprep.settings')
django.setup()

def test_topics_js_fixes():
    """Test if topics.js has the correct event delegation"""
    print("🔍 Testing topics.js fixes...")
    
    topics_js_path = PROJECT_DIR / 'static/staff/js/topics.js'
    
    if not topics_js_path.exists():
        print("❌ topics.js not found")
        return False
    
    content = topics_js_path.read_text()
    
    # Check for event delegation
    if 'document.addEventListener(\'click\'' in content:
        print("✅ Event delegation implemented in topics.js")
    else:
        print("❌ Event delegation missing in topics.js")
        return False
    
    # Check for console logging
    if 'console.log(\'Topics page loaded' in content:
        print("✅ Debug logging added to topics.js")
    else:
        print("❌ Debug logging missing in topics.js")
        return False
    
    return True

def test_subjects_js_fixes():
    """Test if subjects.js has the correct button update logic"""
    print("\n🔍 Testing subjects.js fixes...")
    
    subjects_js_path = PROJECT_DIR / 'static/staff/js/subjects.js'
    
    if not subjects_js_path.exists():
        print("❌ subjects.js not found")
        return False
    
    content = subjects_js_path.read_text()
    
    # Check for bindActionButtons function
    if 'function bindActionButtons()' in content:
        print("✅ bindActionButtons function exists in subjects.js")
    else:
        print("❌ bindActionButtons function missing in subjects.js")
        return False
    
    # Check for event delegation
    if 'document.addEventListener(\'click\'' in content:
        print("✅ Event delegation implemented in subjects.js")
    else:
        print("❌ Event delegation missing in subjects.js")
        return False
    
    return True

def test_css_search_fixes():
    """Test if CSS search icon fixes are applied"""
    print("\n🔍 Testing CSS search icon fixes...")
    
    css_files = [
        'static/staff/css/subjects.css',
        'static/staff/css/topics.css'
    ]
    
    all_fixed = True
    
    for css_file in css_files:
        css_path = PROJECT_DIR / css_file
        
        if not css_path.exists():
            print(f"❌ {css_file} not found")
            all_fixed = False
            continue
        
        content = css_path.read_text()
        
        # Check for increased padding
        if 'padding-left: 2.75rem !important' in content:
            print(f"✅ Search input padding fixed in {css_file}")
        else:
            print(f"❌ Search input padding not fixed in {css_file}")
            all_fixed = False
        
        # Check for pointer-events: none
        if 'pointer-events: none' in content:
            print(f"✅ Search icon pointer-events fixed in {css_file}")
        else:
            print(f"❌ Search icon pointer-events not fixed in {css_file}")
            all_fixed = False
    
    return all_fixed

def test_url_configuration():
    """Test if all required URLs are configured"""
    print("\n🔍 Testing URL configuration...")
    
    try:
        from django.urls import reverse
        
        urls_to_test = [
            'staff:topic_list',
            'staff:topic_ajax_add',
            'staff:topic_toggle_status',
            'staff:subject_toggle_status'
        ]
        
        for url_name in urls_to_test:
            try:
                if 'ajax' in url_name or 'toggle' in url_name:
                    # These are AJAX endpoints
                    if 'edit' in url_name:
                        url = reverse(url_name, args=[1])  # Dummy ID for testing
                    else:
                        url = reverse(url_name)
                else:
                    url = reverse(url_name)
                print(f"✅ {url_name} -> {url}")
            except Exception as e:
                print(f"❌ {url_name} - Error: {e}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ URL configuration error: {e}")
        return False

def test_template_integrity():
    """Test if templates have required elements"""
    print("\n🔍 Testing template integrity...")
    
    topic_template = PROJECT_DIR / 'templates/staff/topics/topic_list_new.html'
    
    if not topic_template.exists():
        print("❌ topic_list_new.html not found")
        return False
    
    content = topic_template.read_text()
    
    # Check for required JavaScript URL setup
    if 'window.staffUrls.topicToggleStatus' in content:
        print("✅ Topic toggle status URL configured in template")
    else:
        print("❌ Topic toggle status URL missing in template")
        return False
    
    # Check for button classes
    if 'btn-edit' in content and 'btn-archive' in content and 'btn-restore' in content:
        print("✅ Action buttons present in template")
    else:
        print("❌ Action buttons missing in template")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 Testing Subjects & Topics Management Fixes")
    print("=" * 50)
    
    tests = [
        ("Topics.js Event Handling", test_topics_js_fixes),
        ("Subjects.js Button Updates", test_subjects_js_fixes),
        ("CSS Search Icon Fixes", test_css_search_fixes),
        ("URL Configuration", test_url_configuration),
        ("Template Integrity", test_template_integrity)
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 FIX VERIFICATION SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ FIXED" if result else "❌ ISSUE"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} fixes verified")
    
    if passed == len(results):
        print("\n🎉 All fixes verified! The issues should be resolved.")
        print("\n🚀 Ready to test:")
        print("1. Start server: python manage.py runserver")
        print("2. Test subjects page: /staff/subjects/")
        print("3. Test topics page: /staff/topics/")
        print("4. Try edit/archive/restore buttons")
        print("5. Check search icon positioning")
    else:
        print("\n⚠️  Some fixes may need attention. Please check the issues above.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
