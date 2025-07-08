#!/usr/bin/env python3
"""
Simple Tags Management Structure Verification
Checks file structure and key components without requiring server
"""

import os
import re

def check_file_exists(filepath, description):
    """Check if a file exists and return status"""
    exists = os.path.exists(filepath)
    status = "✅ FOUND" if exists else "❌ MISSING"
    print(f"{status} {description}: {filepath}")
    return exists

def check_file_content(filepath, patterns, description):
    """Check if file contains required patterns"""
    if not os.path.exists(filepath):
        print(f"❌ MISSING {description}: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        all_found = True
        for pattern_name, pattern in patterns.items():
            if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                print(f"✅ FOUND {pattern_name} in {description}")
            else:
                print(f"❌ MISSING {pattern_name} in {description}")
                all_found = False
        
        return all_found
        
    except Exception as e:
        print(f"❌ ERROR reading {description}: {str(e)}")
        return False

def main():
    """Main verification function"""
    print("=" * 60)
    print("🔍 TAGS MANAGEMENT STRUCTURE VERIFICATION")
    print("=" * 60)
    
    base_path = "D:\\PMC\\Exam-Prep-Site"
    
    # Check key files exist
    files_to_check = [
        (f"{base_path}\\templates\\staff\\tags\\tag_list.html", "Tag List Template"),
        (f"{base_path}\\templates\\staff\\tags\\tag_form.html", "Tag Form Template"),
        (f"{base_path}\\static\\staff\\css\\tags.css", "Tags CSS"),
        (f"{base_path}\\static\\staff\\js\\tags.js", "Tags JavaScript"),
        (f"{base_path}\\static\\staff\\js\\tags_shared.js", "Tags Shared JS"),
        (f"{base_path}\\staff\\views\\tag_views.py", "Tag Views"),
        (f"{base_path}\\staff\\views\\tag_ajax_views.py", "Tag AJAX Views"),
        (f"{base_path}\\staff\\forms.py", "Staff Forms"),
        (f"{base_path}\\core\\models\\tag_models.py", "Tag Models"),
        (f"{base_path}\\staff\\urls.py", "Staff URLs"),
    ]
    
    print("\\n📁 FILE EXISTENCE CHECK:")
    all_files_exist = True
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_files_exist = False
    
    print("\\n🔧 TEMPLATE CONTENT CHECK:")
    # Check tag_list.html content
    tag_list_patterns = {
        "Add Tag Button": r'id=["\']addTagBtn["\']',
        "Tags Table": r'class=["\'].*tags-table.*["\']',
        "Search Input": r'id=["\']searchInput["\']',
        "Status Filter": r'id=["\']statusFilter["\']',
        "Bulk Actions": r'id=["\']bulkActionBtn["\']',
        "Tag Modal": r'id=["\']tagModal["\']',
    }
    
    tag_list_ok = check_file_content(
        f"{base_path}\\templates\\staff\\tags\\tag_list.html",
        tag_list_patterns,
        "Tag List Template"
    )
    
    print("\\n🎨 CSS CONTENT CHECK:")
    # Check CSS file
    css_patterns = {
        "Tags Header": r'\.tags-header',
        "Filter Section": r'\.filter-section',
        "Tags Table": r'\.tags-table',
        "Tag Actions": r'\.tag-actions',
        "Status Badge": r'\.status-badge',
    }
    
    css_ok = check_file_content(
        f"{base_path}\\static\\staff\\css\\tags.css",
        css_patterns,
        "Tags CSS"
    )
    
    print("\\n⚡ JAVASCRIPT CONTENT CHECK:")
    # Check JavaScript file
    js_patterns = {
        "DOM Content Loaded": r'DOMContentLoaded',
        "Initialize Modals": r'initializeModals',
        "Bind Event Handlers": r'bindEventHandlers',
        "Save Tag Function": r'function saveTag',
        "AJAX Fetch": r'fetch\(',
        "Show Toast": r'showToast',
        "Proper Closure": r'\}\)\(\);.*End IIFE',
    }
    
    js_ok = check_file_content(
        f"{base_path}\\static\\staff\\js\\tags.js",
        js_patterns,
        "Tags JavaScript"
    )
    
    print("\\n🐍 BACKEND CONTENT CHECK:")
    # Check views file
    views_patterns = {
        "Tag List View": r'class TagListView',
        "Staff Required Mixin": r'StaffRequiredMixin',
        "Tag Model Import": r'from.*Tag',
    }
    
    views_ok = check_file_content(
        f"{base_path}\\staff\\views\\tag_views.py",
        views_patterns,
        "Tag Views"
    )
    
    # Check AJAX views
    ajax_patterns = {
        "Tag AJAX Mixin": r'class TagAjaxMixin',
        "JSON Response": r'JsonResponse',
        "Tag Create AJAX": r'class TagCreateAjaxView',
        "Tag Update AJAX": r'class TagUpdateAjaxView',
        "Tag Toggle Status": r'class TagToggleStatusView',
    }
    
    ajax_ok = check_file_content(
        f"{base_path}\\staff\\views\\tag_ajax_views.py",
        ajax_patterns,
        "Tag AJAX Views"
    )
    
    # Check models
    models_patterns = {
        "Tag Model": r'class Tag\(models\.Model\)',
        "Subtag Model": r'class Subtag\(models\.Model\)',
        "Resource Fields": r'apply_to_.*resources',
        "Color Field": r'color.*CharField',
    }
    
    models_ok = check_file_content(
        f"{base_path}\\core\\models\\tag_models.py",
        models_patterns,
        "Tag Models"
    )
    
    # Check URLs
    urls_patterns = {
        "Tag List URL": r'tags/',
        "Tag AJAX URLs": r'tags/ajax/',
        "Subtag AJAX URLs": r'subtags/ajax/',
        "Tag Views Import": r'from.*views',
    }
    
    urls_ok = check_file_content(
        f"{base_path}\\staff\\urls.py",
        urls_patterns,
        "Staff URLs"
    )
    
    print("\\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    checks = [
        ("File Existence", all_files_exist),
        ("Tag List Template", tag_list_ok),
        ("Tags CSS", css_ok),
        ("Tags JavaScript", js_ok),
        ("Tag Views", views_ok),
        ("Tag AJAX Views", ajax_ok),
        ("Tag Models", models_ok),
        ("Staff URLs", urls_ok),
    ]
    
    passed = sum(1 for _, ok in checks if ok)
    total = len(checks)
    success_rate = (passed / total) * 100
    
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    if success_rate == 100:
        print("🎉 ALL STRUCTURE CHECKS PASSED!")
        print("✨ Tags management implementation appears complete")
        print("🚀 Ready for server testing")
    elif success_rate >= 80:
        print("⚠️  Most checks passed, minor issues detected")
        print("🔧 Some components may need attention")
    else:
        print("❌ Multiple issues detected")
        print("🛠️  Significant fixes required")
    
    print("\\n" + "=" * 60)
    print("📋 DETAILED RESULTS")
    print("=" * 60)
    for check_name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {check_name}")
    
    print("\\n💡 NEXT STEPS:")
    if success_rate >= 80:
        print("1. Start Django server: python manage.py runserver")
        print("2. Navigate to: http://127.0.0.1:8000/staff/tags/")
        print("3. Test all functionality manually")
        print("4. Check browser console for JavaScript errors")
        print("5. Verify AJAX requests in Network tab")
    else:
        print("1. Fix missing files and components")
        print("2. Re-run this verification")
        print("3. Then proceed with server testing")

if __name__ == '__main__':
    main()
