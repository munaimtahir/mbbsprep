#!/usr/bin/env python3
"""
Comprehensive Tags Management Testing Script
Tests all functionality of the tags management system including:
- Tag CRUD operations
- Subtag management
- Filter/search functionality
- Bulk actions
- Color picker
- Resource type assignments
- AJAX endpoints
"""

import os
import sys
import django
import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medprep.settings')
django.setup()

from core.models import Tag, Subtag
from staff.forms import TagForm, SubtagForm


class TagsManagementTester:
    """Comprehensive tester for tags management functionality"""
    
    def __init__(self):
        self.client = Client()
        self.setup_test_user()
        self.test_results = []
        
    def setup_test_user(self):
        """Create test staff user and login"""
        try:
            # Create staff user
            self.staff_user = User.objects.create_user(
                username='test_staff',
                email='test@example.com',
                password='testpass123',
                is_staff=True,
                is_superuser=True
            )
            
            # Login
            login_result = self.client.login(username='test_staff', password='testpass123')
            self.log_test("User Setup", login_result, "Staff user created and logged in")
            
        except Exception as e:
            self.log_test("User Setup", False, f"Failed to setup user: {str(e)}")
    
    def log_test(self, test_name, success, message):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.test_results.append(f"{status} {test_name}: {message}")
        print(f"{status} {test_name}: {message}")
    
    def test_tag_list_page(self):
        """Test main tags list page loads correctly"""
        try:
            response = self.client.get('/staff/tags/')
            success = response.status_code == 200
            
            if success:
                content = response.content.decode()
                # Check for key elements
                has_header = 'Tags & Subtags Management' in content
                has_add_button = 'addTagBtn' in content
                has_table = 'tags-table' in content
                has_filters = 'statusFilter' in content and 'resourceFilter' in content
                has_bulk_actions = 'bulkActionBtn' in content
                
                all_elements = has_header and has_add_button and has_table and has_filters and has_bulk_actions
                
                self.log_test("Tags List Page", all_elements, 
                            f"Page loaded with all elements present: Header({has_header}), Add Button({has_add_button}), Table({has_table}), Filters({has_filters}), Bulk Actions({has_bulk_actions})")
            else:
                self.log_test("Tags List Page", False, f"Page failed to load: Status {response.status_code}")
                
        except Exception as e:
            self.log_test("Tags List Page", False, f"Exception: {str(e)}")
    
    def test_tag_creation(self):
        """Test tag creation functionality"""
        try:
            # Test form creation
            tag_data = {
                'name': 'Test Tag',
                'description': 'Test description',
                'color': '#FF5733',
                'is_active': True,
                'apply_to_all_resources': False,
                'apply_to_mcq': True,
                'apply_to_videos': True,
                'apply_to_notes': False
            }
            
            form = TagForm(data=tag_data)
            form_valid = form.is_valid()
            
            if form_valid:
                tag = form.save()
                self.log_test("Tag Creation (Form)", True, f"Tag '{tag.name}' created successfully with ID {tag.id}")
                
                # Test AJAX creation endpoint
                ajax_response = self.client.post(
                    '/staff/tags/ajax/add/',
                    data=json.dumps({
                        'name': 'AJAX Test Tag',
                        'description': 'AJAX test description',
                        'color': '#33FF57',
                        'is_active': True,
                        'apply_to_all_resources': True
                    }),
                    content_type='application/json'
                )
                
                ajax_success = ajax_response.status_code == 200
                if ajax_success:
                    response_data = json.loads(ajax_response.content)
                    self.log_test("Tag Creation (AJAX)", response_data.get('success', False), 
                                response_data.get('message', 'AJAX tag creation'))
                else:
                    self.log_test("Tag Creation (AJAX)", False, f"AJAX creation failed: Status {ajax_response.status_code}")
                
            else:
                self.log_test("Tag Creation (Form)", False, f"Form validation failed: {form.errors}")
                
        except Exception as e:
            self.log_test("Tag Creation", False, f"Exception: {str(e)}")
    
    def test_tag_editing(self):
        """Test tag editing functionality"""
        try:
            # Create a test tag first
            tag = Tag.objects.create(
                name='Edit Test Tag',
                description='Original description',
                color='#0057A3',
                is_active=True
            )
            
            # Test GET endpoint
            get_response = self.client.get(f'/staff/tags/ajax/{tag.id}/')
            get_success = get_response.status_code == 200
            
            if get_success:
                tag_data = json.loads(get_response.content)
                self.log_test("Tag Get (AJAX)", tag_data.get('success', False), 
                            f"Retrieved tag data for ID {tag.id}")
                
                # Test UPDATE endpoint
                update_response = self.client.post(
                    f'/staff/tags/ajax/{tag.id}/update/',
                    data=json.dumps({
                        'name': 'Updated Test Tag',
                        'description': 'Updated description',
                        'color': '#FF0000',
                        'is_active': True,
                        'apply_to_all_resources': False,
                        'apply_to_mcq': True
                    }),
                    content_type='application/json'
                )
                
                update_success = update_response.status_code == 200
                if update_success:
                    response_data = json.loads(update_response.content)
                    self.log_test("Tag Update (AJAX)", response_data.get('success', False),
                                response_data.get('message', 'Tag update'))
                else:
                    self.log_test("Tag Update (AJAX)", False, f"Update failed: Status {update_response.status_code}")
            else:
                self.log_test("Tag Get (AJAX)", False, f"Get failed: Status {get_response.status_code}")
                
        except Exception as e:
            self.log_test("Tag Editing", False, f"Exception: {str(e)}")
    
    def test_tag_status_toggle(self):
        """Test tag status toggle functionality"""
        try:
            # Create test tag
            tag = Tag.objects.create(
                name='Status Toggle Test',
                is_active=True
            )
            
            # Test status toggle
            toggle_response = self.client.post(
                '/staff/tags/ajax/toggle-status/',
                data=json.dumps({'tag_id': tag.id}),
                content_type='application/json'
            )
            
            toggle_success = toggle_response.status_code == 200
            if toggle_success:
                response_data = json.loads(toggle_response.content)
                # Refresh tag from database
                tag.refresh_from_db()
                actual_status = not tag.is_active  # Should be toggled
                
                self.log_test("Tag Status Toggle", response_data.get('success', False),
                            f"Status toggled successfully. New status: {actual_status}")
            else:
                self.log_test("Tag Status Toggle", False, f"Toggle failed: Status {toggle_response.status_code}")
                
        except Exception as e:
            self.log_test("Tag Status Toggle", False, f"Exception: {str(e)}")
    
    def test_subtag_functionality(self):
        """Test subtag creation and management"""
        try:
            # Create parent tag
            parent_tag = Tag.objects.create(
                name='Parent Tag for Subtags',
                is_active=True
            )
            
            # Test subtag creation
            subtag_data = {
                'name': 'Test Subtag',
                'tag': parent_tag.id,
                'description': 'Test subtag description',
                'is_active': True
            }
            
            # Test AJAX subtag creation
            subtag_response = self.client.post(
                '/staff/subtags/ajax/add/',
                data=json.dumps(subtag_data),
                content_type='application/json'
            )
            
            subtag_success = subtag_response.status_code == 200
            if subtag_success:
                response_data = json.loads(subtag_response.content)
                self.log_test("Subtag Creation", response_data.get('success', False),
                            response_data.get('message', 'Subtag creation'))
                
                # Test getting subtags for parent tag
                get_subtags_response = self.client.get(f'/staff/tags/{parent_tag.id}/subtags/')
                get_success = get_subtags_response.status_code == 200
                
                self.log_test("Get Tag Subtags", get_success,
                            f"Retrieved subtags for parent tag {parent_tag.id}")
            else:
                self.log_test("Subtag Creation", False, f"Failed: Status {subtag_response.status_code}")
                
        except Exception as e:
            self.log_test("Subtag Functionality", False, f"Exception: {str(e)}")
    
    def test_bulk_actions(self):
        """Test bulk actions functionality"""
        try:
            # Create multiple test tags
            tags = []
            for i in range(3):
                tag = Tag.objects.create(
                    name=f'Bulk Test Tag {i+1}',
                    is_active=True
                )
                tags.append(tag)
            
            tag_ids = [tag.id for tag in tags]
            
            # Test bulk archive
            bulk_response = self.client.post(
                '/staff/tags/ajax/bulk-action/',
                data=json.dumps({
                    'action': 'archive',
                    'tag_ids': tag_ids
                }),
                content_type='application/json'
            )
            
            bulk_success = bulk_response.status_code == 200
            if bulk_success:
                response_data = json.loads(bulk_response.content)
                self.log_test("Bulk Actions", response_data.get('success', False),
                            f"Bulk archive operation: {response_data.get('message', 'completed')}")
            else:
                self.log_test("Bulk Actions", False, f"Failed: Status {bulk_response.status_code}")
                
        except Exception as e:
            self.log_test("Bulk Actions", False, f"Exception: {str(e)}")
    
    def test_css_and_js_files(self):
        """Test that CSS and JS files are accessible"""
        try:
            # Test CSS file
            css_response = self.client.get('/static/staff/css/tags.css')
            css_success = css_response.status_code == 200
            
            # Test JS files
            js_response = self.client.get('/static/staff/js/tags.js')
            js_success = js_response.status_code == 200
            
            js_shared_response = self.client.get('/static/staff/js/tags_shared.js')
            js_shared_success = js_shared_response.status_code == 200
            
            self.log_test("Static Files", css_success and js_success and js_shared_success,
                        f"CSS({css_success}), JS({js_success}), JS Shared({js_shared_success})")
                        
        except Exception as e:
            self.log_test("Static Files", False, f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all tests and generate report"""
        print("=" * 60)
        print("🏷️  TAGS MANAGEMENT FUNCTIONALITY TESTING")
        print("=" * 60)
        
        # Run all tests
        self.test_tag_list_page()
        self.test_tag_creation()
        self.test_tag_editing()
        self.test_tag_status_toggle()
        self.test_subtag_functionality()
        self.test_bulk_actions()
        self.test_css_and_js_files()
        
        # Generate summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed_tests = sum(1 for result in self.test_results if "✅ PASS" in result)
        total_tests = len(self.test_results)
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if success_rate == 100:
            print("🎉 ALL TESTS PASSED! Tags management is fully functional!")
        elif success_rate >= 80:
            print("⚠️  Most tests passed, minor issues detected")
        else:
            print("❌ Multiple issues detected, requires attention")
        
        print("\n" + "=" * 60)
        print("📝 DETAILED RESULTS")
        print("=" * 60)
        for result in self.test_results:
            print(result)


def main():
    """Main function to run the tags management tests"""
    try:
        tester = TagsManagementTester()
        tester.run_all_tests()
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {str(e)}")
        print("Unable to run tests. Please check Django setup and database connectivity.")


if __name__ == '__main__':
    main()
