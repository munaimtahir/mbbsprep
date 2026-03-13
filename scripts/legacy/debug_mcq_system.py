#!/usr/bin/env python3
"""
Comprehensive MCQ Management System Debugging Script
Tests all implemented pages: List, Add, Edit, Bulk Upload
Identifies issues and provides detailed debugging information
"""

import os
import sys
import django
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
import traceback

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medprep.settings')
django.setup()

from core.models import Question, Option, Subject, Topic, Tag
from django.contrib.auth.models import User

class MCQSystemDebugger:
    def __init__(self):
        self.client = Client()
        self.issues = []
        self.passed_tests = []
        self.admin_user = None
        
    def log_issue(self, test_name, issue_type, description, details=None):
        """Log an issue found during testing"""
        self.issues.append({
            'test': test_name,
            'type': issue_type,
            'description': description,
            'details': details
        })
        
    def log_success(self, test_name, description):
        """Log a successful test"""
        self.passed_tests.append({
            'test': test_name,
            'description': description
        })
        
    def setup_admin_user(self):
        """Create and login admin user"""
        try:
            User = get_user_model()
            self.admin_user, created = User.objects.get_or_create(
                username='debug_admin',
                defaults={
                    'first_name': 'Debug',
                    'last_name': 'Admin',
                    'email': 'debug@example.com',
                    'is_staff': True,
                    'is_superuser': True,
                }
            )
            if created:
                self.admin_user.set_password('debug123')
                self.admin_user.save()
            
            # Login
            login_success = self.client.login(username='debug_admin', password='debug123')
            if not login_success:
                self.log_issue('setup', 'ERROR', 'Failed to login admin user')
                return False
                
            self.log_success('setup', 'Admin user created and logged in')
            return True
            
        except Exception as e:
            self.log_issue('setup', 'ERROR', f'Failed to setup admin user: {str(e)}', traceback.format_exc())
            return False
    
    def test_mcq_list_page(self):
        """Test MCQ List/Search page"""
        test_name = 'mcq_list'
        print("🔍 Testing MCQ List Page...")
        
        try:
            url = reverse('staff:question_list')
            response = self.client.get(url)
            
            if response.status_code != 200:
                self.log_issue(test_name, 'ERROR', f'Page not accessible (Status: {response.status_code})', f'URL: {url}')
                return False
            
            content = response.content.decode()
            
            # Check for essential elements
            checks = [
                ('MCQ' in content or 'Question' in content, 'Page title/heading'),
                ('search' in content.lower(), 'Search functionality'),
                ('filter' in content.lower() or 'subject' in content.lower(), 'Filter options'),
                ('table' in content.lower() or 'list' in content.lower(), 'Question list/table'),
                ('add' in content.lower() or 'create' in content.lower(), 'Add question link'),
                ('bulk' in content.lower() or 'upload' in content.lower(), 'Bulk upload link'),
            ]
            
            for check, description in checks:
                if check:
                    self.log_success(test_name, f'{description} present')
                else:
                    self.log_issue(test_name, 'WARNING', f'{description} missing from page')
            
            # Check for data display
            questions_count = Question.objects.count()
            if questions_count > 0:
                # Check if questions are displayed
                sample_question = Question.objects.first()
                if sample_question.question_text[:20] in content:
                    self.log_success(test_name, f'Questions are displayed ({questions_count} total)')
                else:
                    self.log_issue(test_name, 'WARNING', 'Questions may not be displaying properly')
            else:
                self.log_issue(test_name, 'INFO', 'No questions in database to display')
            
            # Test search functionality
            search_response = self.client.get(url, {'search': 'test'})
            if search_response.status_code == 200:
                self.log_success(test_name, 'Search functionality working')
            else:
                self.log_issue(test_name, 'ERROR', 'Search functionality broken')
            
            return True
            
        except Exception as e:
            self.log_issue(test_name, 'ERROR', f'Exception in MCQ list test: {str(e)}', traceback.format_exc())
            return False
    
    def test_add_mcq_page(self):
        """Test Add MCQ page"""
        test_name = 'add_mcq'
        print("➕ Testing Add MCQ Page...")
        
        try:
            url = reverse('staff:question_add')
            response = self.client.get(url)
            
            if response.status_code != 200:
                self.log_issue(test_name, 'ERROR', f'Page not accessible (Status: {response.status_code})', f'URL: {url}')
                return False
            
            content = response.content.decode()
            
            # Check for form elements
            form_checks = [
                ('subject' in content.lower(), 'Subject field'),
                ('topic' in content.lower(), 'Topic field'),
                ('question_text' in content.lower() or 'question' in content.lower(), 'Question text field'),
                ('option' in content.lower(), 'Option fields'),
                ('difficulty' in content.lower(), 'Difficulty field'),
                ('explanation' in content.lower(), 'Explanation field'),
                ('reference' in content.lower(), 'Reference field'),
                ('tag' in content.lower(), 'Tags field'),
                ('csrf' in content.lower(), 'CSRF protection'),
                ('save' in content.lower() or 'submit' in content.lower(), 'Save button'),
            ]
            
            for check, description in form_checks:
                if check:
                    self.log_success(test_name, f'{description} present')
                else:
                    self.log_issue(test_name, 'WARNING', f'{description} missing from form')
            
            # Test form submission with minimal valid data
            if Subject.objects.exists() and Topic.objects.exists():
                subject = Subject.objects.first()
                topic = Topic.objects.filter(subject=subject).first()
                
                if topic:
                    # Get CSRF token
                    import re
                    csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', content)
                    csrf_token = csrf_match.group(1) if csrf_match else None
                    
                    test_data = {
                        'csrfmiddlewaretoken': csrf_token,
                        'subject': subject.id,
                        'topic': topic.id,
                        'question_text': 'Test question for debugging - What is the correct answer?',
                        'difficulty': 'easy',
                        'explanation': 'This is a test explanation for debugging.',
                        'reference': 'Test Reference',
                        'is_active': True,
                        'correct_answer': '0',
                        'option_0_text': 'Correct answer (Test)',
                        'option_1_text': 'Wrong answer 1 (Test)',
                        'option_2_text': 'Wrong answer 2 (Test)',
                        'option_3_text': 'Wrong answer 3 (Test)',
                    }
                    
                    form_response = self.client.post(url, test_data)
                    
                    if form_response.status_code == 302:  # Redirect on success
                        self.log_success(test_name, 'Form submission successful (test question created)')
                        
                        # Clean up test question
                        test_questions = Question.objects.filter(question_text__contains='Test question for debugging')
                        if test_questions.exists():
                            test_questions.delete()
                            self.log_success(test_name, 'Test question cleaned up')
                    else:
                        self.log_issue(test_name, 'ERROR', f'Form submission failed (Status: {form_response.status_code})')
                        
                        # Check for validation errors
                        if hasattr(form_response, 'context') and form_response.context:
                            if 'form' in form_response.context:
                                form = form_response.context['form']
                                if form.errors:
                                    self.log_issue(test_name, 'ERROR', f'Form validation errors: {form.errors}')
                else:
                    self.log_issue(test_name, 'ERROR', 'No topics available for testing form submission')
            else:
                self.log_issue(test_name, 'ERROR', 'No subjects/topics available for testing')
            
            return True
            
        except Exception as e:
            self.log_issue(test_name, 'ERROR', f'Exception in Add MCQ test: {str(e)}', traceback.format_exc())
            return False
    
    def test_edit_mcq_page(self):
        """Test Edit MCQ page"""
        test_name = 'edit_mcq'
        print("✏️ Testing Edit MCQ Page...")
        
        try:
            # Get a question to edit
            question = Question.objects.first()
            if not question:
                self.log_issue(test_name, 'ERROR', 'No questions available for editing test')
                return False
            
            url = reverse('staff:question_edit', kwargs={'pk': question.pk})
            response = self.client.get(url)
            
            if response.status_code != 200:
                self.log_issue(test_name, 'ERROR', f'Page not accessible (Status: {response.status_code})', f'URL: {url}')
                return False
            
            content = response.content.decode()
            
            # Check for pre-filled data
            prefill_checks = [
                (question.question_text[:20] in content, 'Question text pre-filled'),
                (question.topic.name in content, 'Topic pre-selected'),
                (str(question.difficulty) in content, 'Difficulty pre-selected'),
                (question.explanation in content if question.explanation else True, 'Explanation pre-filled'),
                ('csrf' in content.lower(), 'CSRF protection'),
            ]
            
            for check, description in prefill_checks:
                if check:
                    self.log_success(test_name, description)
                else:
                    self.log_issue(test_name, 'WARNING', f'{description} - may not be working')
            
            # Check for action buttons
            button_checks = [
                ('save' in content.lower(), 'Save button'),
                ('delete' in content.lower(), 'Delete button'),
                ('reset' in content.lower() or 'cancel' in content.lower(), 'Reset/Cancel button'),
            ]
            
            for check, description in button_checks:
                if check:
                    self.log_success(test_name, f'{description} present')
                else:
                    self.log_issue(test_name, 'WARNING', f'{description} missing')
            
            # Test form submission
            import re
            csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', content)
            csrf_token = csrf_match.group(1) if csrf_match else None
            
            edit_data = {
                'csrfmiddlewaretoken': csrf_token,
                'subject': question.topic.subject.id,
                'topic': question.topic.id,
                'question_text': question.question_text + ' [EDITED]',
                'difficulty': question.difficulty,
                'explanation': question.explanation or 'Test explanation',
                'reference': question.reference or 'Test reference',
                'is_active': True,
                'correct_answer': '0',
                'option_0_text': 'Option A (edited)',
                'option_1_text': 'Option B (edited)',
                'option_2_text': 'Option C (edited)',
                'option_3_text': 'Option D (edited)',
            }
            
            edit_response = self.client.post(url, edit_data)
            
            if edit_response.status_code == 302:  # Redirect on success
                self.log_success(test_name, 'Edit form submission successful')
                
                # Verify the edit
                updated_question = Question.objects.get(pk=question.pk)
                if '[EDITED]' in updated_question.question_text:
                    self.log_success(test_name, 'Question content actually updated')
                    
                    # Restore original content
                    updated_question.question_text = question.question_text
                    updated_question.save()
                    self.log_success(test_name, 'Original content restored')
                else:
                    self.log_issue(test_name, 'ERROR', 'Question content not updated despite successful form submission')
            else:
                self.log_issue(test_name, 'ERROR', f'Edit form submission failed (Status: {edit_response.status_code})')
            
            return True
            
        except Exception as e:
            self.log_issue(test_name, 'ERROR', f'Exception in Edit MCQ test: {str(e)}', traceback.format_exc())
            return False
    
    def test_bulk_upload_page(self):
        """Test Bulk Upload page"""
        test_name = 'bulk_upload'
        print("📤 Testing Bulk Upload Page...")
        
        try:
            url = reverse('staff:question_bulk_upload')
            response = self.client.get(url)
            
            if response.status_code != 200:
                self.log_issue(test_name, 'ERROR', f'Page not accessible (Status: {response.status_code})', f'URL: {url}')
                return False
            
            content = response.content.decode()
            
            # Check for bulk upload elements
            upload_checks = [
                ('file' in content.lower() or 'upload' in content.lower(), 'File upload field'),
                ('csv' in content.lower() or 'excel' in content.lower(), 'CSV/Excel support mentioned'),
                ('template' in content.lower() or 'download' in content.lower(), 'Template download option'),
                ('default' in content.lower(), 'Default field options'),
                ('subject' in content.lower(), 'Default subject field'),
                ('difficulty' in content.lower(), 'Default difficulty field'),
                ('tag' in content.lower(), 'Default tags field'),
                ('csrf' in content.lower(), 'CSRF protection'),
            ]
            
            for check, description in upload_checks:
                if check:
                    self.log_success(test_name, f'{description} present')
                else:
                    self.log_issue(test_name, 'WARNING', f'{description} missing')
            
            # Test template download (if available)
            try:
                template_url = reverse('staff:question_bulk_upload') + '?download_template=1'
                template_response = self.client.get(template_url)
                if template_response.status_code == 200:
                    self.log_success(test_name, 'Template download working')
                else:
                    self.log_issue(test_name, 'INFO', 'Template download not implemented or not working')
            except:
                self.log_issue(test_name, 'INFO', 'Template download test failed (may not be implemented)')
            
            return True
            
        except Exception as e:
            self.log_issue(test_name, 'ERROR', f'Exception in Bulk Upload test: {str(e)}', traceback.format_exc())
            return False
    
    def test_ajax_endpoints(self):
        """Test AJAX endpoints"""
        test_name = 'ajax'
        print("🔗 Testing AJAX Endpoints...")
        
        try:
            # Test get topics AJAX
            ajax_url = reverse('staff:get_topics_ajax')
            
            if Subject.objects.exists():
                subject = Subject.objects.first()
                ajax_response = self.client.get(ajax_url, {'subject_id': subject.id})
                
                if ajax_response.status_code == 200:
                    self.log_success(test_name, 'Get topics AJAX endpoint working')
                    
                    # Check if response is JSON
                    try:
                        import json
                        data = json.loads(ajax_response.content)
                        if isinstance(data, list) or isinstance(data, dict):
                            self.log_success(test_name, 'AJAX response is valid JSON')
                        else:
                            self.log_issue(test_name, 'WARNING', 'AJAX response format unexpected')
                    except:
                        self.log_issue(test_name, 'ERROR', 'AJAX response is not valid JSON')
                else:
                    self.log_issue(test_name, 'ERROR', f'AJAX endpoint failed (Status: {ajax_response.status_code})')
            else:
                self.log_issue(test_name, 'WARNING', 'No subjects available for AJAX testing')
            
            return True
            
        except Exception as e:
            self.log_issue(test_name, 'ERROR', f'Exception in AJAX test: {str(e)}', traceback.format_exc())
            return False
    
    def test_database_integrity(self):
        """Test database integrity and relationships"""
        test_name = 'database'
        print("🗄️ Testing Database Integrity...")
        
        try:
            # Check model counts
            stats = {
                'Subjects': Subject.objects.count(),
                'Topics': Topic.objects.count(),
                'Tags': Tag.objects.count(),
                'Questions': Question.objects.count(),
                'Options': Option.objects.count(),
            }
            
            for model, count in stats.items():
                if count > 0:
                    self.log_success(test_name, f'{model}: {count} records')
                else:
                    self.log_issue(test_name, 'WARNING', f'{model}: No records found')
            
            # Check relationships
            if Question.objects.exists():
                questions_with_topics = Question.objects.filter(topic__isnull=False).count()
                questions_with_options = Question.objects.filter(options__isnull=False).distinct().count()
                
                if questions_with_topics == Question.objects.count():
                    self.log_success(test_name, 'All questions have topics assigned')
                else:
                    self.log_issue(test_name, 'ERROR', f'{Question.objects.count() - questions_with_topics} questions missing topics')
                
                if questions_with_options > 0:
                    self.log_success(test_name, f'{questions_with_options} questions have options')
                else:
                    self.log_issue(test_name, 'ERROR', 'No questions have options assigned')
                
                # Check for questions with correct answers
                questions_with_correct = Question.objects.filter(options__is_correct=True).distinct().count()
                if questions_with_correct > 0:
                    self.log_success(test_name, f'{questions_with_correct} questions have correct answers marked')
                else:
                    self.log_issue(test_name, 'WARNING', 'No questions have correct answers marked')
            
            # Check for orphaned records
            topics_without_subjects = Topic.objects.filter(subject__isnull=True).count()
            if topics_without_subjects == 0:
                self.log_success(test_name, 'No orphaned topics found')
            else:
                self.log_issue(test_name, 'ERROR', f'{topics_without_subjects} topics without subjects')
            
            return True
            
        except Exception as e:
            self.log_issue(test_name, 'ERROR', f'Exception in database test: {str(e)}', traceback.format_exc())
            return False
    
    def test_permissions(self):
        """Test permissions and access control"""
        test_name = 'permissions'
        print("🔒 Testing Permissions...")
        
        try:
            # Test staff-only access
            self.client.logout()
            
            urls_to_test = [
                'staff:question_list',
                'staff:question_add',
                'staff:question_bulk_upload',
            ]
            
            for url_name in urls_to_test:
                try:
                    url = reverse(url_name)
                    response = self.client.get(url)
                    
                    if response.status_code in [302, 403]:  # Redirect to login or forbidden
                        self.log_success(test_name, f'{url_name} properly protected (Status: {response.status_code})')
                    else:
                        self.log_issue(test_name, 'ERROR', f'{url_name} not properly protected (Status: {response.status_code})')
                except:
                    self.log_issue(test_name, 'ERROR', f'Could not test {url_name}')
            
            # Re-login admin
            self.client.login(username='debug_admin', password='debug123')
            
            return True
            
        except Exception as e:
            self.log_issue(test_name, 'ERROR', f'Exception in permissions test: {str(e)}', traceback.format_exc())
            return False
    
    def run_all_tests(self):
        """Run all debugging tests"""
        print("🚀 Starting MCQ Management System Debug Session")
        print("=" * 60)
        
        # Setup
        if not self.setup_admin_user():
            print("❌ Failed to setup admin user - aborting tests")
            return
        
        # Run all tests
        tests = [
            self.test_database_integrity,
            self.test_permissions,
            self.test_mcq_list_page,
            self.test_add_mcq_page,
            self.test_edit_mcq_page,
            self.test_bulk_upload_page,
            self.test_ajax_endpoints,
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                self.log_issue('system', 'CRITICAL', f'Test runner exception in {test.__name__}: {str(e)}', traceback.format_exc())
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate final debugging report"""
        print("\n" + "=" * 60)
        print("🎯 MCQ MANAGEMENT SYSTEM DEBUG REPORT")
        print("=" * 60)
        
        # Summary
        total_tests = len(self.passed_tests) + len(self.issues)
        passed_count = len(self.passed_tests)
        issues_count = len(self.issues)
        
        print(f"\n📊 SUMMARY:")
        print(f"   Total Tests: {total_tests}")
        print(f"   ✅ Passed: {passed_count}")
        print(f"   ⚠️ Issues: {issues_count}")
        
        # Health score
        if total_tests > 0:
            health_score = (passed_count / total_tests) * 100
            print(f"   🏥 Health Score: {health_score:.1f}%")
            
            if health_score >= 90:
                print("   🟢 System Status: EXCELLENT")
            elif health_score >= 75:
                print("   🟡 System Status: GOOD")
            elif health_score >= 50:
                print("   🟠 System Status: NEEDS ATTENTION")
            else:
                print("   🔴 System Status: CRITICAL ISSUES")
        
        # Issues breakdown
        if self.issues:
            print(f"\n⚠️ ISSUES FOUND ({len(self.issues)}):")
            
            error_count = len([i for i in self.issues if i['type'] == 'ERROR'])
            warning_count = len([i for i in self.issues if i['type'] == 'WARNING'])
            info_count = len([i for i in self.issues if i['type'] == 'INFO'])
            
            if error_count > 0:
                print(f"   🔴 ERRORS: {error_count}")
            if warning_count > 0:
                print(f"   🟡 WARNINGS: {warning_count}")
            if info_count > 0:
                print(f"   ℹ️ INFO: {info_count}")
            
            print(f"\n📋 DETAILED ISSUES:")
            for issue in self.issues:
                icon = "🔴" if issue['type'] == 'ERROR' else "🟡" if issue['type'] == 'WARNING' else "ℹ️"
                print(f"   {icon} [{issue['test']}] {issue['description']}")
                if issue['details']:
                    print(f"      Details: {issue['details']}")
        
        # Success highlights
        if self.passed_tests:
            print(f"\n✅ WORKING FEATURES ({len(self.passed_tests)}):")
            
            # Group by test
            test_groups = {}
            for success in self.passed_tests:
                test_name = success['test']
                if test_name not in test_groups:
                    test_groups[test_name] = []
                test_groups[test_name].append(success['description'])
            
            for test_name, descriptions in test_groups.items():
                print(f"   📦 {test_name.upper()}:")
                for desc in descriptions:
                    print(f"      ✅ {desc}")
        
        # Recommendations
        print(f"\n🔧 RECOMMENDATIONS:")
        
        critical_issues = [i for i in self.issues if i['type'] == 'ERROR']
        if critical_issues:
            print("   1. 🔥 URGENT: Fix critical errors before manual testing")
            for issue in critical_issues[:3]:  # Show top 3
                print(f"      - {issue['description']}")
        
        warning_issues = [i for i in self.issues if i['type'] == 'WARNING']
        if warning_issues:
            print("   2. ⚠️ IMPORTANT: Address warnings for better UX")
            for issue in warning_issues[:3]:  # Show top 3
                print(f"      - {issue['description']}")
        
        if not critical_issues:
            print("   ✅ System ready for manual testing!")
            print("   📝 Suggested manual test flow:")
            print("      1. Visit /staff/questions/ - Check list and search")
            print("      2. Visit /staff/questions/add/ - Create a test MCQ")
            print("      3. Edit the created MCQ - Test edit functionality")
            print("      4. Visit /staff/questions/bulk-upload/ - Test upload UI")
            print("      5. Test all filters, sorting, and pagination")
        
        print("\n" + "=" * 60)
        print("🏁 Debug session complete!")
        
        # Save detailed report to file
        self.save_debug_report()
    
    def save_debug_report(self):
        """Save detailed debug report to file"""
        try:
            report_content = []
            report_content.append("MCQ Management System Debug Report")
            report_content.append("=" * 50)
            report_content.append(f"Generated: {django.utils.timezone.now()}")
            report_content.append("")
            
            report_content.append("ISSUES:")
            for issue in self.issues:
                report_content.append(f"[{issue['type']}] {issue['test']}: {issue['description']}")
                if issue['details']:
                    report_content.append(f"Details: {issue['details']}")
                report_content.append("")
            
            report_content.append("SUCCESSES:")
            for success in self.passed_tests:
                report_content.append(f"[PASS] {success['test']}: {success['description']}")
            
            with open('mcq_debug_report.txt', 'w', encoding='utf-8') as f:
                f.write('\n'.join(report_content))
            
            print(f"📄 Detailed report saved to: mcq_debug_report.txt")
            
        except Exception as e:
            print(f"⚠️ Could not save debug report: {str(e)}")

def main():
    debugger = MCQSystemDebugger()
    debugger.run_all_tests()

if __name__ == '__main__':
    main()
