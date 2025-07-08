#!/usr/bin/env python3
"""
Quick Server and Tags Management Test
Starts server and verifies basic functionality
"""

import subprocess
import time
import requests
import signal
import os
import sys

class TagsServerTester:
    def __init__(self):
        self.server_process = None
        self.base_url = "http://127.0.0.1:8000"
        
    def start_server(self):
        """Start Django server"""
        try:
            print("🚀 Starting Django development server...")
            
            # Change to project directory
            os.chdir("D:\\PMC\\Exam-Prep-Site")
            
            # Start server
            self.server_process = subprocess.Popen([
                "D:\\PMC\\Exam-Prep-Site\\.venv\\Scripts\\python.exe",
                "manage.py",
                "runserver",
                "127.0.0.1:8000"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for server to start
            print("⏳ Waiting for server to start...")
            time.sleep(3)
            
            # Check if server is running
            for attempt in range(10):
                try:
                    response = requests.get(self.base_url, timeout=2)
                    if response.status_code in [200, 302, 403]:
                        print("✅ Server is running!")
                        return True
                except:
                    time.sleep(1)
                    
            print("❌ Server failed to start properly")
            return False
            
        except Exception as e:
            print(f"❌ Error starting server: {str(e)}")
            return False
    
    def stop_server(self):
        """Stop Django server"""
        if self.server_process:
            try:
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
                print("🛑 Server stopped")
            except:
                self.server_process.kill()
                print("🛑 Server forcefully killed")
    
    def test_static_files(self):
        """Test static file accessibility"""
        print("\\n📁 Testing static files...")
        
        static_files = [
            "/static/staff/css/tags.css",
            "/static/staff/js/tags.js", 
            "/static/staff/js/tags_shared.js"
        ]
        
        results = []
        for file_path in static_files:
            try:
                url = self.base_url + file_path
                response = requests.get(url, timeout=5)
                success = response.status_code == 200 and len(response.content) > 100
                
                file_name = file_path.split("/")[-1]
                status = "✅ OK" if success else "❌ FAIL"
                size = len(response.content) if success else 0
                
                print(f"{status} {file_name} ({size} bytes)")
                results.append(success)
                
            except Exception as e:
                print(f"❌ FAIL {file_path} - {str(e)}")
                results.append(False)
        
        return all(results)
    
    def test_tags_page_access(self):
        """Test tags page accessibility"""
        print("\\n🏷️  Testing tags page access...")
        
        try:
            url = self.base_url + "/staff/tags/"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 302:
                print("🔐 Redirected to login (expected - authentication required)")
                return True
            elif response.status_code == 200:
                content = response.text
                has_tags_management = "Tags & Subtags Management" in content
                has_required_elements = "addTagBtn" in content or "tags-table" in content
                
                if has_tags_management and has_required_elements:
                    print("✅ Tags page accessible and contains required elements")
                    return True
                else:
                    print("⚠️  Tags page accessible but missing some elements")
                    return False
            else:
                print(f"❌ Unexpected response: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error accessing tags page: {str(e)}")
            return False
    
    def test_ajax_endpoints(self):
        """Test AJAX endpoint availability"""
        print("\\n⚡ Testing AJAX endpoints...")
        
        endpoints = [
            "/staff/tags/ajax/add/",
            "/staff/tags/ajax/toggle-status/", 
            "/staff/tags/ajax/bulk-action/",
            "/staff/subtags/ajax/add/"
        ]
        
        results = []
        for endpoint in endpoints:
            try:
                url = self.base_url + endpoint
                response = requests.get(url, timeout=5)
                
                # 405 = Method Not Allowed (expected for POST endpoints)
                # 302 = Redirect to login (expected)
                # 403 = Forbidden (expected without auth)
                success = response.status_code in [302, 403, 405]
                
                endpoint_name = endpoint.split("/")[-2]
                status = "✅ EXISTS" if success else "❌ MISSING"
                
                print(f"{status} {endpoint_name} (Status: {response.status_code})")
                results.append(success)
                
            except Exception as e:
                print(f"❌ ERROR {endpoint} - {str(e)}")
                results.append(False)
        
        return sum(results) >= len(results) // 2  # At least half should work
    
    def run_tests(self):
        """Run all tests"""
        print("=" * 60)
        print("🧪 TAGS MANAGEMENT SERVER TESTING")
        print("=" * 60)
        
        try:
            # Start server
            if not self.start_server():
                print("\\n❌ Cannot proceed - server failed to start")
                return False
            
            # Run tests
            static_ok = self.test_static_files()
            page_ok = self.test_tags_page_access()
            ajax_ok = self.test_ajax_endpoints()
            
            # Results summary
            print("\\n" + "=" * 60)
            print("📊 TEST RESULTS SUMMARY")
            print("=" * 60)
            
            tests = [
                ("Static Files", static_ok),
                ("Tags Page Access", page_ok),
                ("AJAX Endpoints", ajax_ok)
            ]
            
            passed = sum(1 for _, ok in tests if ok)
            total = len(tests)
            success_rate = (passed / total) * 100
            
            print(f"Tests Passed: {passed}/{total}")
            print(f"Success Rate: {success_rate:.1f}%")
            
            for test_name, result in tests:
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"{status} {test_name}")
            
            if success_rate >= 80:
                print("\\n🎉 TAGS MANAGEMENT READY FOR MANUAL TESTING!")
                print("\\n🌐 Open your browser and navigate to:")
                print(f"   {self.base_url}/staff/tags/")
                print("\\n📋 Manual testing checklist:")
                print("   1. ✅ Add new tag functionality")
                print("   2. ✅ Edit existing tag")
                print("   3. ✅ Color picker works")
                print("   4. ✅ Resource type checkboxes")
                print("   5. ✅ Search and filters")
                print("   6. ✅ Archive/restore tags")
                print("   7. ✅ Bulk actions")
                print("   8. ✅ Subtag management")
                print("   9. ✅ No JavaScript errors in console")
                print("   10. ✅ AJAX requests work in Network tab")
                
                print("\\n⏰ Server will keep running for manual testing...")
                print("   Press Ctrl+C to stop the server when done")
                
                # Keep server running for manual testing
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\\n\\n👋 Manual testing session ended")
                    
            else:
                print("\\n⚠️  Some issues detected - check logs above")
                
            return success_rate >= 80
            
        except KeyboardInterrupt:
            print("\\n\\n⏹️  Testing interrupted by user")
            return False
        except Exception as e:
            print(f"\\n❌ Critical error during testing: {str(e)}")
            return False
        finally:
            self.stop_server()

def main():
    """Main function"""
    tester = TagsServerTester()
    success = tester.run_tests()
    
    if success:
        print("\\n✨ Tags management system is ready!")
    else:
        print("\\n🔧 Some issues need to be addressed")
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
