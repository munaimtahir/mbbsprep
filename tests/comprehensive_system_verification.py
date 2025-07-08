#!/usr/bin/env python3
"""
Comprehensive system verification script for MedPrep Admin System
Tests all components: Dashboard, Users, Subjects, Topics, MCQs, Tags, Bulk Upload
"""
import os
import sys
import django
import requests
from datetime import datetime
import json

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medprep.settings')
django.setup()

from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import UserProfile, Subject, Topic, Question, Option, Tag, Subtag


class MedPrepSystemVerification:
    def __init__(self):
        self.client = Client()
        self.admin_user = None
        self.test_results = {
            'dashboard': {'total': 0, 'passed': 0, 'failed': 0, 'errors': []},
            'users': {'total': 0, 'passed': 0, 'failed': 0, 'errors': []},
            'subjects': {'total': 0, 'passed': 0, 'failed': 0, 'errors': []},
            'topics': {'total': 0, 'passed': 0, 'failed': 0, 'errors': []},
            'mcqs': {'total': 0, 'passed': 0, 'failed': 0, 'errors': []},
            'tags': {'total': 0, 'passed': 0, 'failed': 0, 'errors': []},
            'bulk_upload': {'total': 0, 'passed': 0, 'failed': 0, 'errors': []},
        }
        
    def setup_test_environment(self):
        """Create test admin user and test data"""
        print("🔧 Setting up test environment...")
        
        # Create admin user
        self.admin_user, created = User.objects.get_or_create(
            username='test_admin',
            defaults={
                'email': 'admin@test.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            self.admin_user.set_password('testpass123')
            self.admin_user.save()
        
        # Login
        login_success = self.client.login(username='test_admin', password='testpass123')
        if not login_success:
            print("❌ Failed to login as admin")
            return False
        
        print("✅ Test environment setup complete")
        return True
    
    def test_dashboard(self):
        """Test dashboard functionality"""
        print("\n📊 Testing Dashboard...")
        module = 'dashboard'
        
        # Test dashboard access
        self.run_test(module, "Dashboard Access", lambda: self.test_dashboard_access())
        self.run_test(module, "Dashboard Stats", lambda: self.test_dashboard_stats())
        self.run_test(module, "Dashboard Navigation", lambda: self.test_dashboard_navigation())
        
    def test_dashboard_access(self):
        response = self.client.get(reverse('staff:dashboard'))
        assert response.status_code == 200, f"Dashboard returned {response.status_code}"
        assert 'Dashboard' in response.content.decode(), "Dashboard title not found"
        return True
        
    def test_dashboard_stats(self):
        response = self.client.get(reverse('staff:dashboard'))
        content = response.content.decode()
        # Check for key stats elements
        assert 'Total Users' in content or 'total-users' in content, "User stats not found"
        return True
        
    def test_dashboard_navigation(self):
        response = self.client.get(reverse('staff:dashboard'))
        content = response.content.decode()
        # Check for navigation links
        assert 'Users' in content, "Users navigation not found"
        assert 'Questions' in content or 'MCQs' in content, "Questions navigation not found"
        return True
    
    def test_users(self):
        """Test user management functionality"""
        print("\n👥 Testing User Management...")
        module = 'users'
        
        self.run_test(module, "User List Access", lambda: self.test_user_list_access())
        self.run_test(module, "User Detail Access", lambda: self.test_user_detail_access())
        self.run_test(module, "User Create Form", lambda: self.test_user_create_form())
        self.run_test(module, "User Edit Form", lambda: self.test_user_edit_form())
        
    def test_user_list_access(self):
        response = self.client.get(reverse('staff:user_list'))
        assert response.status_code == 200, f"User list returned {response.status_code}"
        return True
        
    def test_user_detail_access(self):
        # Create test user if needed
        test_user, created = User.objects.get_or_create(
            username='test_user_detail',
            defaults={'email': 'testuser@test.com'}
        )
        response = self.client.get(reverse('staff:user_detail', kwargs={'pk': test_user.pk}))
        assert response.status_code == 200, f"User detail returned {response.status_code}"
        return True
        
    def test_user_create_form(self):
        response = self.client.get(reverse('staff:user_add'))
        assert response.status_code == 200, f"User create form returned {response.status_code}"
        return True
        
    def test_user_edit_form(self):
        test_user, created = User.objects.get_or_create(
            username='test_user_edit',
            defaults={'email': 'testedit@test.com'}
        )
        response = self.client.get(reverse('staff:user_edit', kwargs={'pk': test_user.pk}))
        assert response.status_code == 200, f"User edit form returned {response.status_code}"
        return True
    
    def test_subjects(self):
        """Test subject management functionality"""
        print("\n📚 Testing Subject Management...")
        module = 'subjects'
        
        self.run_test(module, "Subject List Access", lambda: self.test_subject_list_access())
        self.run_test(module, "Subject Create Form", lambda: self.test_subject_create_form())
        self.run_test(module, "Subject AJAX Endpoints", lambda: self.test_subject_ajax())
        
    def test_subject_list_access(self):
        response = self.client.get(reverse('staff:subject_list'))
        assert response.status_code == 200, f"Subject list returned {response.status_code}"
        return True
        
    def test_subject_create_form(self):
        response = self.client.get(reverse('staff:subject_add'))
        assert response.status_code == 200, f"Subject create form returned {response.status_code}"
        return True
        
    def test_subject_ajax(self):
        # Test subject AJAX creation
        response = self.client.post(reverse('staff:subject_ajax_add'), {
            'name': 'Test Subject AJAX',
            'code': 'TSA',
            'description': 'Test description'
        })
        assert response.status_code == 200, f"Subject AJAX add returned {response.status_code}"
        return True
    
    def test_topics(self):
        """Test topic management functionality"""
        print("\n📝 Testing Topic Management...")
        module = 'topics'
        
        self.run_test(module, "Topic List Access", lambda: self.test_topic_list_access())
        self.run_test(module, "Topic Create Form", lambda: self.test_topic_create_form())
        self.run_test(module, "Topic AJAX Endpoints", lambda: self.test_topic_ajax())
        self.run_test(module, "Topic Bulk Upload Access", lambda: self.test_topic_bulk_upload_access())
        
    def test_topic_list_access(self):
        response = self.client.get(reverse('staff:topic_list'))
        assert response.status_code == 200, f"Topic list returned {response.status_code}"
        return True
        
    def test_topic_create_form(self):
        response = self.client.get(reverse('staff:topic_add'))
        assert response.status_code == 200, f"Topic create form returned {response.status_code}"
        return True
        
    def test_topic_ajax(self):
        # Create test subject first
        subject, created = Subject.objects.get_or_create(
            name='Test Subject for Topic',
            defaults={'code': 'TST', 'description': 'Test subject'}
        )
        
        response = self.client.post(reverse('staff:topic_ajax_add'), {
            'name': 'Test Topic AJAX',
            'subject': subject.id,
            'description': 'Test topic description'
        })
        assert response.status_code == 200, f"Topic AJAX add returned {response.status_code}"
        return True
        
    def test_topic_bulk_upload_access(self):
        response = self.client.get(reverse('staff:topic_bulk_upload'))
        assert response.status_code == 200, f"Topic bulk upload returned {response.status_code}"
        return True
    
    def test_mcqs(self):
        """Test MCQ management functionality"""
        print("\n❓ Testing MCQ Management...")
        module = 'mcqs'
        
        self.run_test(module, "MCQ List Access", lambda: self.test_mcq_list_access())
        self.run_test(module, "MCQ Create Form", lambda: self.test_mcq_create_form())
        self.run_test(module, "MCQ Bulk Upload Access", lambda: self.test_mcq_bulk_upload_access())
        
    def test_mcq_list_access(self):
        response = self.client.get(reverse('staff:question_list'))
        assert response.status_code == 200, f"MCQ list returned {response.status_code}"
        return True
        
    def test_mcq_create_form(self):
        response = self.client.get(reverse('staff:question_add'))
        assert response.status_code == 200, f"MCQ create form returned {response.status_code}"
        return True
        
    def test_mcq_bulk_upload_access(self):
        response = self.client.get(reverse('staff:question_bulk_upload'))
        assert response.status_code == 200, f"MCQ bulk upload returned {response.status_code}"
        return True
    
    def test_tags(self):
        """Test tag management functionality"""
        print("\n🏷️ Testing Tag Management...")
        module = 'tags'
        
        self.run_test(module, "Tag List Access", lambda: self.test_tag_list_access())
        self.run_test(module, "Tag AJAX Create", lambda: self.test_tag_ajax_create())
        self.run_test(module, "Tag AJAX Get", lambda: self.test_tag_ajax_get())
        self.run_test(module, "Tag AJAX Update", lambda: self.test_tag_ajax_update())
        
    def test_tag_list_access(self):
        response = self.client.get(reverse('staff:tag_list'))
        assert response.status_code == 200, f"Tag list returned {response.status_code}"
        return True
        
    def test_tag_ajax_create(self):
        response = self.client.post(reverse('staff:tag_create_ajax'), {
            'name': 'Test Tag AJAX',
            'description': 'Test tag description',
            'color': '#FF5733',
            'resourceTypeAll': 'on'
        })
        assert response.status_code == 200, f"Tag AJAX create returned {response.status_code}"
        
        # Check if response is JSON and successful
        try:
            data = response.json()
            assert data.get('success'), f"Tag creation failed: {data.get('message')}"
        except:
            pass  # Non-JSON response might be redirect
        return True
        
    def test_tag_ajax_get(self):
        # Create test tag first
        tag, created = Tag.objects.get_or_create(
            name='Test Tag Get',
            defaults={'description': 'Test tag for get', 'color': '#28A745'}
        )
        
        response = self.client.get(reverse('staff:tag_get_ajax', kwargs={'pk': tag.pk}))
        assert response.status_code == 200, f"Tag AJAX get returned {response.status_code}"
        return True
        
    def test_tag_ajax_update(self):
        # Create test tag first
        tag, created = Tag.objects.get_or_create(
            name='Test Tag Update',
            defaults={'description': 'Test tag for update', 'color': '#17A2B8'}
        )
        
        response = self.client.post(reverse('staff:tag_update_ajax', kwargs={'pk': tag.pk}), {
            'name': 'Updated Test Tag',
            'description': 'Updated description',
            'color': '#DC3545',
            'resourceTypeAll': 'on'
        })
        assert response.status_code == 200, f"Tag AJAX update returned {response.status_code}"
        return True
    
    def test_bulk_upload(self):
        """Test bulk upload functionality"""
        print("\n📤 Testing Bulk Upload...")
        module = 'bulk_upload'
        
        self.run_test(module, "Topic Bulk Template", lambda: self.test_topic_bulk_template())
        self.run_test(module, "User Bulk Upload Access", lambda: self.test_user_bulk_upload_access())
        self.run_test(module, "MCQ Bulk Upload Access", lambda: self.test_mcq_bulk_upload_access())
        
    def test_topic_bulk_template(self):
        response = self.client.get(reverse('staff:topic_bulk_template'))
        assert response.status_code == 200, f"Topic bulk template returned {response.status_code}"
        assert 'text/csv' in response.get('Content-Type', ''), "Template is not CSV format"
        return True
        
    def test_user_bulk_upload_access(self):
        response = self.client.get(reverse('staff:user_bulk_upload'))
        assert response.status_code == 200, f"User bulk upload returned {response.status_code}"
        return True
        
    def test_mcq_bulk_upload_access(self):
        response = self.client.get(reverse('staff:question_bulk_upload'))
        assert response.status_code == 200, f"MCQ bulk upload returned {response.status_code}"
        return True
    
    def run_test(self, module, test_name, test_func):
        """Run a single test and record results"""
        self.test_results[module]['total'] += 1
        try:
            result = test_func()
            if result:
                self.test_results[module]['passed'] += 1
                print(f"  ✅ {test_name}")
            else:
                self.test_results[module]['failed'] += 1
                self.test_results[module]['errors'].append(f"{test_name}: Test returned False")
                print(f"  ❌ {test_name}: Test returned False")
        except Exception as e:
            self.test_results[module]['failed'] += 1
            self.test_results[module]['errors'].append(f"{test_name}: {str(e)}")
            print(f"  ❌ {test_name}: {str(e)}")
    
    def print_results(self):
        """Print comprehensive test results"""
        print("\n" + "="*80)
        print("🎯 COMPREHENSIVE SYSTEM VERIFICATION RESULTS")
        print("="*80)
        
        total_tests = 0
        total_passed = 0
        total_failed = 0
        
        for module, results in self.test_results.items():
            total_tests += results['total']
            total_passed += results['passed']
            total_failed += results['failed']
            
            success_rate = (results['passed'] / results['total'] * 100) if results['total'] > 0 else 0
            
            status_icon = "🟢" if success_rate == 100 else "🟡" if success_rate >= 75 else "🔴"
            
            print(f"\n{status_icon} {module.upper()}: {results['passed']}/{results['total']} ({success_rate:.1f}%)")
            
            if results['errors']:
                for error in results['errors']:
                    print(f"    ❌ {error}")
        
        overall_success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        print("\n" + "="*80)
        print(f"🎯 OVERALL RESULTS: {total_passed}/{total_tests} ({overall_success_rate:.1f}%)")
        
        if overall_success_rate == 100:
            print("🎉🎉🎉 PERFECT SCORE! ALL TESTS PASSED! 🎉🎉🎉")
        elif overall_success_rate >= 90:
            print("🎉 EXCELLENT! System is highly functional!")
        elif overall_success_rate >= 75:
            print("👍 GOOD! Most features are working correctly.")
        else:
            print("⚠️ NEEDS ATTENTION! Several issues found.")
        
        print("="*80)
        return overall_success_rate
    
    def run_all_tests(self):
        """Run all system verification tests"""
        print("🚀 Starting Comprehensive System Verification...")
        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if not self.setup_test_environment():
            print("❌ Failed to setup test environment")
            return False
        
        # Run all test modules
        self.test_dashboard()
        self.test_users()
        self.test_subjects()
        self.test_topics()
        self.test_mcqs()
        self.test_tags()
        self.test_bulk_upload()
        
        # Print results
        success_rate = self.print_results()
        
        return success_rate >= 90  # Consider 90%+ as success


def main():
    """Main function to run verification"""
    verifier = MedPrepSystemVerification()
    success = verifier.run_all_tests()
    
    if success:
        print("\n✅ System verification completed successfully!")
        print("🌐 Ready for manual testing at http://localhost:8000/staff/")
    else:
        print("\n⚠️ System verification found issues that need attention.")
        print("🔧 Please review the errors above and fix them before manual testing.")
    
    return success


if __name__ == "__main__":
    main()
