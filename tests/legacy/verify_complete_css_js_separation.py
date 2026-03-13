#!/usr/bin/env python3
"""
Verification script to ensure complete CSS/JS separation for MCQ management pages.
This script checks for:
1. No inline <style> blocks
2. No large inline <script> blocks (small URL config scripts are allowed)
3. No inline event handlers (onclick, onchange, etc.)
4. Proper external CSS/JS file references
5. Event delegation implementation in JS files
"""

import os
import re
import sys
from pathlib import Path

def check_template_separation(template_path):
    """Check a template for proper CSS/JS separation."""
    issues = []
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for inline styles
    style_matches = re.findall(r'<style[^>]*>.*?</style>', content, re.DOTALL | re.IGNORECASE)
    if style_matches:
        issues.append(f"Found {len(style_matches)} inline <style> block(s)")
    
    # Check for large inline scripts (allow small URL config scripts)
    script_matches = re.findall(r'<script[^>]*>(?:(?!</script>).)*</script>', content, re.DOTALL | re.IGNORECASE)
    large_scripts = []
    for script in script_matches:
        # Skip if it's just URL configuration (small and contains staffUrls)
        script_content = re.sub(r'</?script[^>]*>', '', script).strip()
        if len(script_content) > 100 and 'staffUrls' not in script_content:
            large_scripts.append(script)
    
    if large_scripts:
        issues.append(f"Found {len(large_scripts)} large inline <script> block(s)")
    
    # Check for inline event handlers
    event_handlers = [
        'onclick=', 'onchange=', 'oninput=', 'onsubmit=', 'onload=', 
        'onmouseover=', 'onmouseout=', 'onfocus=', 'onblur=', 'onkeyup=',
        'onkeydown=', 'ondrop=', 'ondragover=', 'ondragleave='
    ]
    
    inline_events = []
    for handler in event_handlers:
        matches = re.findall(f'{handler}["\'][^"\']*["\']', content, re.IGNORECASE)
        inline_events.extend(matches)
    
    if inline_events:
        issues.append(f"Found {len(inline_events)} inline event handler(s): {', '.join(inline_events[:3])}{'...' if len(inline_events) > 3 else ''}")
    
    # Check for external CSS/JS references
    has_external_css = re.search(r"{% static 'staff/css/.*\.css' %}", content)
    has_external_js = re.search(r"{% static 'staff/js/.*\.js' %}", content)
    
    if not has_external_css:
        issues.append("Missing external CSS reference")
    
    if not has_external_js:
        issues.append("Missing external JS reference")
    
    return issues

def check_js_event_delegation(js_path):
    """Check JS file for proper event delegation implementation."""
    issues = []
    
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for event delegation setup
    has_event_delegation = 'addEventListener' in content and 'document.addEventListener' in content
    if not has_event_delegation:
        issues.append("Missing event delegation setup")
    
    # Check for setupEventDelegation function
    has_setup_function = 'setupEventDelegation' in content
    if not has_setup_function:
        issues.append("Missing setupEventDelegation function")
    
    return issues

def main():
    # Define paths
    templates_dir = Path('templates/staff/questions')
    static_js_dir = Path('static/staff/js')
    
    templates = [
        'question_list.html',
        'question_add.html', 
        'question_edit.html',
        'bulk_upload.html'
    ]
    
    js_files = [
        'question_list.js',
        'question_add.js',
        'question_edit.js', 
        'bulk_upload.js'
    ]
    
    print("🔍 Verifying Complete CSS/JS Separation")
    print("=" * 50)
    
    total_issues = 0
    
    # Check templates
    print("\n📄 Template Analysis:")
    for template in templates:
        template_path = templates_dir / template
        if template_path.exists():
            issues = check_template_separation(template_path)
            if issues:
                print(f"❌ {template}:")
                for issue in issues:
                    print(f"   • {issue}")
                total_issues += len(issues)
            else:
                print(f"✅ {template}: Clean separation")
        else:
            print(f"⚠️  {template}: File not found")
    
    # Check JavaScript files
    print("\n🟨 JavaScript Analysis:")
    for js_file in js_files:
        js_path = static_js_dir / js_file
        if js_path.exists():
            issues = check_js_event_delegation(js_path)
            if issues:
                print(f"❌ {js_file}:")
                for issue in issues:
                    print(f"   • {issue}")
                total_issues += len(issues)
            else:
                print(f"✅ {js_file}: Proper event delegation")
        else:
            print(f"⚠️  {js_file}: File not found")
    
    # Check external file structure
    print("\n📁 File Structure:")
    required_files = [
        'static/staff/css/question_list.css',
        'static/staff/css/question_add.css',
        'static/staff/css/question_edit.css',
        'static/staff/css/bulk_upload.css',
        'static/staff/js/mcq_shared.js',
        'static/staff/js/question_list.js',
        'static/staff/js/question_add.js',
        'static/staff/js/question_edit.js',
        'static/staff/js/bulk_upload.js'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files:")
        for missing in missing_files:
            print(f"   • {missing}")
        total_issues += len(missing_files)
    else:
        print("✅ All required external files exist")
    
    # Summary
    print("\n" + "=" * 50)
    if total_issues == 0:
        print("🎉 SUCCESS: Complete CSS/JS separation achieved!")
        print("   • No inline styles or large scripts")
        print("   • No inline event handlers")
        print("   • Proper external file references")
        print("   • Event delegation implemented")
        return 0
    else:
        print(f"❌ ISSUES FOUND: {total_issues} issue(s) need attention")
        return 1

if __name__ == '__main__':
    sys.exit(main())
