#!/usr/bin/env python3
"""
Test script to verify the edit button functionality for tags
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medprep.settings')
django.setup()

from core.models import Tag
from django.urls import reverse
from django.test import Client


def test_edit_button_setup():
    """Test if edit button setup is correct"""
    print("🔍 Testing Edit Button Setup...")
    
    # Check if we have tags to test with
    tags = Tag.objects.all()[:3]
    if not tags:
        print("❌ No tags found to test with. Creating test tag...")
        tag = Tag.objects.create(
            name="Test Tag",
            description="Test description",
            color="#FF5733",
            apply_to_mcq=True
        )
        tags = [tag]
    
    print(f"✅ Found {len(tags)} tag(s) to test with")
    
    # Test URL patterns
    try:
        url = reverse('staff:tag_get_ajax', kwargs={'pk': tags[0].id})
        print(f"✅ Tag get AJAX URL: {url}")
    except Exception as e:
        print(f"❌ Tag get AJAX URL error: {e}")
        return False
    
    try:
        url = reverse('staff:tag_update_ajax', kwargs={'pk': tags[0].id})
        print(f"✅ Tag update AJAX URL: {url}")
    except Exception as e:
        print(f"❌ Tag update AJAX URL error: {e}")
        return False
    
    # Test AJAX view responses
    client = Client()
    
    try:
        response = client.get(reverse('staff:tag_get_ajax', kwargs={'pk': tags[0].id}))
        if response.status_code == 200:
            import json
            data = json.loads(response.content)
            if data.get('success'):
                print(f"✅ Tag get AJAX view working - tag: {data['tag']['name']}")
            else:
                print(f"❌ Tag get AJAX view failed: {data.get('message')}")
                return False
        else:
            print(f"❌ Tag get AJAX view returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Tag get AJAX view error: {e}")
        return False
    
    print("✅ All edit button setup tests passed!")
    return True


def test_template_files():
    """Test if template files are correct"""
    print("\n🔍 Testing Template Files...")
    
    template_path = "templates/staff/tags/tag_list.html"
    if not os.path.exists(template_path):
        print(f"❌ Template file not found: {template_path}")
        return False
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for edit button
    if 'btn-edit-tag' in content:
        print("✅ Edit button class found in template")
    else:
        print("❌ Edit button class not found in template")
        return False
    
    # Check for tag modal
    if 'id="tagModal"' in content:
        print("✅ Tag modal found in template")
    else:
        print("❌ Tag modal not found in template")
        return False
    
    # Check for form fields
    required_fields = ['tagId', 'tagName', 'tagDescription', 'tagColor']
    for field in required_fields:
        if f'id="{field}"' in content:
            print(f"✅ Form field {field} found")
        else:
            print(f"❌ Form field {field} not found")
            return False
    
    # Check for staffUrls
    if 'window.staffUrls' in content:
        print("✅ staffUrls object found")
    else:
        print("❌ staffUrls object not found")
        return False
    
    print("✅ All template tests passed!")
    return True


def test_static_files():
    """Test if static files are correct"""
    print("\n🔍 Testing Static Files...")
    
    js_path = "static/staff/js/tags.js"
    if not os.path.exists(js_path):
        print(f"❌ JavaScript file not found: {js_path}")
        return False
    
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for edit functions
    if 'handleEditTag' in content:
        print("✅ handleEditTag function found")
    else:
        print("❌ handleEditTag function not found")
        return False
    
    if 'loadTagForEdit' in content:
        print("✅ loadTagForEdit function found")
    else:
        print("❌ loadTagForEdit function not found")
        return False
    
    if 'populateTagForm' in content:
        print("✅ populateTagForm function found")
    else:
        print("❌ populateTagForm function not found")
        return False
    
    # Check for event binding
    if 'btn-edit-tag' in content:
        print("✅ Edit button event binding found")
    else:
        print("❌ Edit button event binding not found")
        return False
    
    print("✅ All static file tests passed!")
    return True


def main():
    """Run all tests"""
    print("🚀 Starting Edit Button Tests...\n")
    
    success = True
    success &= test_template_files()
    success &= test_static_files()
    success &= test_edit_button_setup()
    
    print("\n" + "="*50)
    if success:
        print("🎉 ALL TESTS PASSED! Edit button should be working correctly.")
        print("🔧 If the edit button still doesn't work, check browser console for JavaScript errors.")
        print("🌐 Navigate to http://localhost:8000/staff/tags/ and try clicking an edit button.")
        print("🐛 Check the browser's Developer Tools (F12) -> Console for any errors.")
    else:
        print("❌ SOME TESTS FAILED! Please fix the issues above.")
    print("="*50)


if __name__ == "__main__":
    main()
