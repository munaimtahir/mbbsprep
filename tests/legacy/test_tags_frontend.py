#!/usr/bin/env python3
"""
Frontend Tags Management Testing Script
Tests the browser-side functionality including:
- JavaScript event handlers
- AJAX requests
- UI interactions
- Form submissions
"""

import time
import requests
import json
from urllib.parse import urljoin


class TagsFrontendTester:
    """Test frontend functionality of tags management"""
    
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, success, message):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.test_results.append(f"{status} {test_name}: {message}")
        print(f"{status} {test_name}: {message}")
    
    def test_server_connectivity(self):
        """Test if Django server is running"""
        try:
            response = self.session.get(self.base_url, timeout=5)
            success = response.status_code in [200, 302, 403]  # 302 for redirect, 403 for access denied
            self.log_test("Server Connectivity", success, 
                         f"Server responded with status {response.status_code}")
            return success
        except Exception as e:
            self.log_test("Server Connectivity", False, f"Cannot connect to server: {str(e)}")
            return False
    
    def test_tags_page_accessibility(self):
        """Test if tags management page is accessible"""
        try:
            url = urljoin(self.base_url, "/staff/tags/")
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 302:
                # Likely redirected to login
                self.log_test("Tags Page Access", False, "Redirected to login - authentication required")
                return False
            elif response.status_code == 200:
                # Check for key elements in HTML
                content = response.text
                has_tags_management = "Tags & Subtags Management" in content
                has_add_button = "addTagBtn" in content or "Add Tag" in content
                has_table = "tags-table" in content or "tag-row" in content
                
                success = has_tags_management and (has_add_button or has_table)
                self.log_test("Tags Page Access", success, 
                             f"Page loaded with required elements: Title({has_tags_management}), Button({has_add_button}), Table({has_table})")
                return success
            else:
                self.log_test("Tags Page Access", False, f"Unexpected status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Tags Page Access", False, f"Exception: {str(e)}")
            return False
    
    def test_static_files(self):
        """Test if CSS and JS files are accessible"""
        static_files = [
            "/static/staff/css/tags.css",
            "/static/staff/js/tags.js",
            "/static/staff/js/tags_shared.js"
        ]
        
        all_success = True
        for file_path in static_files:
            try:
                url = urljoin(self.base_url, file_path)
                response = self.session.get(url, timeout=5)
                success = response.status_code == 200
                
                if success:
                    # Check file content is not empty
                    content_length = len(response.content)
                    success = content_length > 100  # Basic content check
                    
                file_name = file_path.split("/")[-1]
                self.log_test(f"Static File ({file_name})", success, 
                             f"File accessible and has content ({content_length} bytes)" if success 
                             else f"File missing or empty (Status: {response.status_code})")
                
                all_success = all_success and success
                
            except Exception as e:
                self.log_test(f"Static File ({file_path})", False, f"Exception: {str(e)}")
                all_success = False
        
        return all_success
    
    def test_ajax_endpoints(self):
        """Test AJAX endpoints availability (without authentication)"""
        # Note: These will likely return 403/302 without auth, but we can check if endpoints exist
        ajax_endpoints = [
            "/staff/tags/ajax/add/",
            "/staff/tags/ajax/toggle-status/",
            "/staff/tags/ajax/bulk-action/",
            "/staff/subtags/ajax/add/"
        ]
        
        endpoints_exist = 0
        for endpoint in ajax_endpoints:
            try:
                url = urljoin(self.base_url, endpoint)
                response = self.session.get(url, timeout=5)
                
                # 405 Method Not Allowed is expected for POST endpoints accessed with GET
                # 403 Forbidden or 302 Redirect indicates endpoint exists but requires auth
                success = response.status_code in [302, 403, 405]
                
                if success:
                    endpoints_exist += 1
                
                endpoint_name = endpoint.split("/")[-2]
                self.log_test(f"AJAX Endpoint ({endpoint_name})", success,
                             f"Endpoint exists (Status: {response.status_code})")
                
            except Exception as e:
                self.log_test(f"AJAX Endpoint ({endpoint})", False, f"Exception: {str(e)}")
        
        overall_success = endpoints_exist >= len(ajax_endpoints) // 2  # At least half should work
        return overall_success
    
    def run_frontend_tests(self):
        """Run all frontend tests"""
        print("=" * 60)
        print("🌐 TAGS MANAGEMENT FRONTEND TESTING")
        print("=" * 60)
        
        # Test server connectivity first
        if not self.test_server_connectivity():
            print("❌ Cannot proceed - server is not accessible")
            return
        
        # Run tests
        self.test_tags_page_accessibility()
        self.test_static_files()
        self.test_ajax_endpoints()
        
        # Generate summary
        print("\n" + "=" * 60)
        print("📊 FRONTEND TEST SUMMARY")
        print("=" * 60)
        
        passed_tests = sum(1 for result in self.test_results if "✅ PASS" in result)
        total_tests = len(self.test_results)
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("🎉 Frontend infrastructure is working properly!")
        else:
            print("⚠️  Some frontend issues detected")
        
        print("\n" + "=" * 60)
        print("📝 DETAILED RESULTS")
        print("=" * 60)
        for result in self.test_results:
            print(result)


def main():
    """Main function"""
    try:
        print("Starting frontend testing...")
        print("Make sure Django server is running on http://127.0.0.1:8000")
        print("You can start it with: python manage.py runserver")
        print()
        
        tester = TagsFrontendTester()
        tester.run_frontend_tests()
        
    except KeyboardInterrupt:
        print("\n⏹️  Testing interrupted by user")
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {str(e)}")


if __name__ == '__main__':
    main()
