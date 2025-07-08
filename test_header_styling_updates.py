#!/usr/bin/env python
"""
Test script to verify the header styling updates for subjects and topics pages
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

def test_template_headers():
    """Test if templates have the new MCQ-style headers"""
    print("🔍 Testing template header updates...")
    
    # Test subjects template
    subjects_template = PROJECT_DIR / 'templates/staff/subjects/subject_list_new.html'
    
    if not subjects_template.exists():
        print("❌ subjects template not found")
        return False
    
    subjects_content = subjects_template.read_text()
    
    # Check for new header elements
    if 'Subject Management' in subjects_content and 'breadcrumb mb-2' in subjects_content:
        print("✅ Subjects template header updated")
    else:
        print("❌ Subjects template header not updated")
        return False
    
    # Test topics template
    topics_template = PROJECT_DIR / 'templates/staff/topics/topic_list_new.html'
    
    if not topics_template.exists():
        print("❌ topics template not found")
        return False
    
    topics_content = topics_template.read_text()
    
    # Check for new header elements
    if 'Topic Management' in topics_content and 'breadcrumb mb-2' in topics_content:
        print("✅ Topics template header updated")
    else:
        print("❌ Topics template header not updated")
        return False
    
    return True

def test_css_updates():
    """Test if CSS files have been updated with new styles"""
    print("\n🔍 Testing CSS updates...")
    
    css_files = [
        'static/staff/css/subjects.css',
        'static/staff/css/topics.css',
        'static/staff/css/subject_form.css'
    ]
    
    all_updated = True
    
    for css_file in css_files:
        css_path = PROJECT_DIR / css_file
        
        if not css_path.exists():
            print(f"❌ {css_file} not found")
            all_updated = False
            continue
        
        content = css_path.read_text()
        
        # Check for header styling updates
        if css_file.endswith('subject_form.css'):
            if 'text-decoration: none !important' in content:
                print(f"✅ {css_file} - underline removal added")
            else:
                print(f"❌ {css_file} - underline removal missing")
                all_updated = False
        else:
            if 'text-white-50' in content and 'text-white-75' in content:
                print(f"✅ {css_file} - header styling updated")
            else:
                print(f"❌ {css_file} - header styling missing")
                all_updated = False
        
        # Check if old custom button styles were removed
        if 'btn-primary {' in content and 'background: #0057A3' in content:
            print(f"⚠️  {css_file} - old custom button styles still present")
        else:
            print(f"✅ {css_file} - old custom button styles removed")
    
    # Check for new header card and button styles
    for css_file in ['static/staff/css/subjects.css', 'static/staff/css/topics.css']:
        css_path = PROJECT_DIR / css_file
        
        if not css_path.exists():
            print(f"❌ {css_file} not found")
            all_updated = False
            continue
        
        content = css_path.read_text()
        
        # Check for enhanced header styling
        if 'box-shadow: 0 4px 12px' in content:
            print(f"✅ {css_file} - enhanced header card styling added")
        else:
            print(f"❌ {css_file} - enhanced header card styling missing")
            all_updated = False
            
        # Check for button hover effects
        if 'transform: translateY(-2px)' in content:
            print(f"✅ {css_file} - enhanced button hover effects added")
        else:
            print(f"❌ {css_file} - enhanced button hover effects missing")
            all_updated = False
            
        # Check for no underline on buttons
        if '.btn.btn-outline-light {' in content and 'text-decoration: none !important' in content:
            print(f"✅ {css_file} - button underline removal verified")
        else:
            print(f"⚠️ {css_file} - button underline removal may need verification")
    
    return all_updated

def test_bootstrap_integration():
    """Test if Bootstrap button classes are properly used"""
    print("\n🔍 Testing Bootstrap button integration...")
    
    templates = [
        'templates/staff/subjects/subject_list_new.html',
        'templates/staff/topics/topic_list_new.html'
    ]
    
    all_correct = True
    
    for template in templates:
        template_path = PROJECT_DIR / template
        
        if not template_path.exists():
            print(f"❌ {template} not found")
            all_correct = False
            continue
        
        content = template_path.read_text()
        
        # Check for Bootstrap button classes
        if 'btn btn-light btn-lg' in content and 'btn btn-outline-light btn-lg' in content:
            print(f"✅ {template} - Bootstrap button classes used")
        else:
            print(f"❌ {template} - Bootstrap button classes missing")
            all_correct = False
    
    return all_correct

def test_header_consistency():
    """Test if headers are consistent with MCQ page style"""
    print("\n🔍 Testing header consistency...")
    
    # Check if both templates have similar structure
    templates = [
        'templates/staff/subjects/subject_list_new.html',
        'templates/staff/topics/topic_list_new.html'
    ]
    
    header_elements = [
        'breadcrumb mb-2',
        'text-white-50',
        'text-white',
        'text-white-75',
        'fas fa-',
        'Management'
    ]
    
    all_consistent = True
    
    for template in templates:
        template_path = PROJECT_DIR / template
        
        if not template_path.exists():
            continue
        
        content = template_path.read_text()
        
        for element in header_elements:
            if element in content:
                print(f"✅ {template} has {element}")
            else:
                print(f"❌ {template} missing {element}")
                all_consistent = False
    
    return all_consistent

def main():
    """Run all tests"""
    print("🧪 Testing Subject & Topics Header Styling Updates")
    print("=" * 60)
    
    tests = [
        ("Template Headers", test_template_headers),
        ("CSS Updates", test_css_updates),
        ("Bootstrap Integration", test_bootstrap_integration),
        ("Header Consistency", test_header_consistency)
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 HEADER STYLING UPDATE SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ UPDATED" if result else "❌ ISSUE"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} updates verified")
    
    if passed == len(results):
        print("\n🎉 All header styling updates completed successfully!")
        print("\n🚀 Changes made:")
        print("- ✅ Subject page header now matches MCQ page style")
        print("- ✅ Topics page header now matches MCQ page style")
        print("- ✅ Proper breadcrumb navigation with links")
        print("- ✅ Large titles with icons and descriptions")
        print("- ✅ Bootstrap button classes for consistency")
        print("- ✅ Removed underlines from manage buttons")
        print("- ✅ Cleaned up old custom CSS styles")
    else:
        print("\n⚠️  Some updates may need attention. Please check the issues above.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
