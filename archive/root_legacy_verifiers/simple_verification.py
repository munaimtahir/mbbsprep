#!/usr/bin/env python3
"""
Simple Admin Verification - Quick Check
"""
import os
import sys

try:
    # Setup Django environment with explicit path handling
    import os
    import sys
    
    # Get absolute path to the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_dir)
    
    # Set Django settings module without extra spaces
    os.environ['DJANGO_SETTINGS_MODULE'] = 'medprep.settings'
    
    import django
    django.setup()
    
    from django.test import Client
    from django.urls import reverse
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    def simple_test():
        """Simple test of key admin features"""
        client = Client()
        
        # Get staff user
        staff_user = User.objects.filter(is_staff=True).first()
        if not staff_user:
            print("❌ No staff user found")
            return False
        
        # Ensure password is set
        staff_user.set_password('testpass123')
        staff_user.save()
        
        # Login
        login_success = client.login(username=staff_user.username, password='testpass123')
        if not login_success:
            print("❌ Login failed")
            return False
        print("✅ Login successful")
        
        # Test key pages
        test_urls = [
            ('staff:dashboard', 'Dashboard'),
            ('staff:user_list', 'User List'),
            ('staff:question_list', 'Question List'),
            ('staff:subject_list', 'Subject List'),
            ('staff:topic_list', 'Topic List'),
            ('staff:tag_list', 'Tag List'),
        ]
        
        success_count = 0
        total_count = len(test_urls)
        
        for url_name, description in test_urls:
            try:
                response = client.get(reverse(url_name))
                if response.status_code == 200:
                    print(f"✅ {description}: OK")
                    success_count += 1
                else:
                    print(f"❌ {description}: {response.status_code}")
            except Exception as e:
                print(f"❌ {description}: Error - {e}")
        
        success_rate = (success_count / total_count) * 100
        print(f"\n🎯 SUCCESS RATE: {success_rate:.1f}% ({success_count}/{total_count})")
        
        return success_rate >= 80
    
    if __name__ == '__main__':
        print("🚀 Simple Admin Verification")
        print("=" * 40)
        result = simple_test()
        if result:
            print("\n✅ ADMIN SYSTEM IS WORKING!")
        else:
            print("\n❌ ADMIN SYSTEM NEEDS ATTENTION!")

except Exception as e:
    print(f"❌ Setup Error: {e}")
    import traceback
    traceback.print_exc()
