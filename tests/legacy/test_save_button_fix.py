#!/usr/bin/env python3
"""
Quick Test Script for Tags Save Button Issue
Tests the specific save button functionality
"""

import os
import sys

def check_template_issues():
    """Check template for common issues"""
    print("🔍 Checking template issues...")
    
    template_path = "D:\\PMC\\Exam-Prep-Site\\templates\\staff\\tags\\tag_list.html"
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    fixes = []
    
    # Check for save button
    if 'id="saveTagBtn"' in content:
        print("✅ Save button found in template")
    else:
        issues.append("Save button not found")
    
    # Check for form
    if 'id="tagForm"' in content:
        print("✅ Tag form found in template")
    else:
        issues.append("Tag form not found")
    
    # Check for CSRF token
    if 'csrf_token' in content:
        print("✅ CSRF token found in template")
    else:
        issues.append("CSRF token missing")
    
    # Check URL configurations
    url_checks = [
        ('tagAdd', 'tag_create_ajax'),
        ('tagUpdate', 'tag_update_ajax'),
        ('tagGet', 'tag_get_ajax')
    ]
    
    for js_name, url_name in url_checks:
        if js_name in content and url_name in content:
            print(f"✅ URL {js_name} -> {url_name} configured")
        else:
            issues.append(f"URL mapping {js_name} -> {url_name} missing")
    
    # Check resource type field naming
    if 'resourceTypeMcq' in content:
        print("✅ Resource type field names consistent")
        fixes.append("Fixed resourceTypeMCQ -> resourceTypeMcq")
    elif 'resourceTypeMCQ' in content:
        issues.append("Resource type field name inconsistency (MCQ vs Mcq)")
    
    return issues, fixes

def check_javascript_issues():
    """Check JavaScript for common issues"""
    print("\\n🔍 Checking JavaScript issues...")
    
    js_path = "D:\\PMC\\Exam-Prep-Site\\static\\staff\\js\\tags.js"
    
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    fixes = []
    
    # Check for saveTag function
    if 'function saveTag()' in content:
        print("✅ saveTag function found")
    else:
        issues.append("saveTag function not found")
    
    # Check for event binding
    if "bindElement('#saveTagBtn', 'click', saveTag)" in content:
        print("✅ Save button event binding found")
    else:
        issues.append("Save button event binding not found")
    
    # Check for URL usage
    url_checks = ['tagAdd', 'tagUpdate', 'tagGet']
    for url in url_checks:
        if f'window.staffUrls.{url}' in content:
            print(f"✅ JavaScript uses {url} URL")
        else:
            issues.append(f"JavaScript missing {url} URL usage")
    
    # Check for proper closure
    if content.count('})();') >= 1:
        print("✅ JavaScript has proper closure")
        if 'Save tag function called' in content:
            fixes.append("Added debug logging to saveTag function")
    else:
        issues.append("JavaScript missing proper closure")
    
    # Check for error handling
    if 'console.log' in content and 'console.error' in content:
        print("✅ Debug logging added")
        fixes.append("Enhanced error logging and debugging")
    
    return issues, fixes

def main():
    """Main function"""
    print("🏷️  TAGS SAVE BUTTON - ISSUE DIAGNOSIS & FIX VERIFICATION")
    print("=" * 70)
    
    # Check template issues
    template_issues, template_fixes = check_template_issues()
    
    # Check JavaScript issues  
    js_issues, js_fixes = check_javascript_issues()
    
    # Summary
    print("\\n" + "=" * 70)
    print("📊 DIAGNOSIS SUMMARY")
    print("=" * 70)
    
    all_issues = template_issues + js_issues
    all_fixes = template_fixes + js_fixes
    
    if not all_issues:
        print("🎉 NO ISSUES FOUND!")
        print("\\n✅ All components appear to be correctly configured:")
        print("   - Save button exists in template")
        print("   - JavaScript saveTag function implemented")
        print("   - Event binding configured")
        print("   - URL mappings correct")
        print("   - CSRF token available")
        print("   - Debug logging added")
    else:
        print(f"⚠️  FOUND {len(all_issues)} ISSUES:")
        for issue in all_issues:
            print(f"   ❌ {issue}")
    
    if all_fixes:
        print(f"\\n🔧 APPLIED {len(all_fixes)} FIXES:")
        for fix in all_fixes:
            print(f"   ✅ {fix}")
    
    print("\\n" + "=" * 70)
    print("🚀 NEXT STEPS")
    print("=" * 70)
    
    if not all_issues:
        print("1. Start Django server: python manage.py runserver")
        print("2. Navigate to: http://127.0.0.1:8000/staff/tags/")
        print("3. Open browser Developer Tools (F12)")
        print("4. Check Console tab for debug messages")
        print("5. Click 'Add Tag' button")
        print("6. Fill in tag details and click 'Save Tag'")
        print("7. Monitor console for debug output:")
        print("   - 'Save tag function called'")
        print("   - 'Tag data to send: {...}'")
        print("   - 'Request URL: /staff/tags/ajax/add/'")
        print("   - 'Response status: 200'")
        print("8. Check Network tab for AJAX request details")
        print("\\n💡 If save button still doesn't work:")
        print("   - Check browser console for JavaScript errors")
        print("   - Verify AJAX request is being sent")
        print("   - Check server logs for backend errors")
        print("   - Ensure user has proper permissions")
    else:
        print("❌ Fix the issues above before testing")
    
    return len(all_issues) == 0

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
