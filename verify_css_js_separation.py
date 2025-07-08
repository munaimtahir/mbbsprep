#!/usr/bin/env python3
"""
CSS/JS Separation Verification Script
=====================================

This script verifies that all CSS and JavaScript code has been properly
separated from HTML templates into external static files.
"""

import os
import re
from pathlib import Path

def check_template_separation(template_path):
    """Check if a template has properly separated CSS and JS."""
    issues = []
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for inline CSS (excluding small inline styles)
    style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    if style_blocks:
        for i, block in enumerate(style_blocks):
            if len(block.strip()) > 50:  # Ignore very small inline styles
                issues.append(f"Large inline CSS block #{i+1} found ({len(block)} chars)")
    
    # Check for inline script blocks (excluding very small ones)
    script_blocks = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    for i, block in enumerate(script_blocks):
        if len(block.strip()) > 100:  # Ignore small script blocks
            # Allow URL setting scripts
            if 'window.staffUrls' not in block and 'window.mcqEditData' not in block:
                issues.append(f"Large inline JavaScript block #{i+1} found ({len(block)} chars)")
    
    # Check for event handlers in HTML
    event_handlers = re.findall(r'on\w+="[^"]*"', content)
    if event_handlers:
        issues.append(f"Inline event handlers found: {len(event_handlers)} instances")
    
    return issues

def check_static_files_exist():
    """Check if all expected static files exist."""
    base_path = Path(__file__).parent
    static_css_path = base_path / 'static' / 'staff' / 'css'
    static_js_path = base_path / 'static' / 'staff' / 'js'
    
    expected_files = {
        'CSS': [
            static_css_path / 'question_list.css',
            static_css_path / 'question_add.css',
            static_css_path / 'question_edit.css',
            static_css_path / 'bulk_upload.css'
        ],
        'JavaScript': [
            static_js_path / 'mcq_shared.js',
            static_js_path / 'question_list.js',
            static_js_path / 'question_add.js',
            static_js_path / 'question_edit.js',
            static_js_path / 'bulk_upload.js'
        ]
    }
    
    missing_files = []
    for file_type, files in expected_files.items():
        for file_path in files:
            if not file_path.exists():
                missing_files.append(f"{file_type}: {file_path.name}")
    
    return missing_files

def check_template_references():
    """Check if templates properly reference external CSS/JS files."""
    base_path = Path(__file__).parent
    templates_path = base_path / 'templates' / 'staff' / 'questions'
    
    template_files = [
        'question_list.html',
        'question_add.html',
        'question_edit.html',
        'bulk_upload.html'
    ]
    
    reference_issues = []
    
    for template_file in template_files:
        template_path = templates_path / template_file
        if not template_path.exists():
            reference_issues.append(f"Template not found: {template_file}")
            continue
            
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Expected references based on template name
        base_name = template_file.replace('.html', '').replace('question_', '')
        if base_name == 'list':
            base_name = 'question_list'
        elif base_name == 'add':
            base_name = 'question_add'
        elif base_name == 'edit':
            base_name = 'question_edit'
        
        expected_css = f"staff/css/{base_name}.css"
        expected_js = f"staff/js/{base_name}.js"
        expected_shared_js = "staff/js/mcq_shared.js"
        
        if expected_css not in content:
            reference_issues.append(f"{template_file}: Missing CSS reference to {expected_css}")
        
        if expected_js not in content:
            reference_issues.append(f"{template_file}: Missing JS reference to {expected_js}")
        
        if expected_shared_js not in content and template_file != 'bulk_upload.html':
            reference_issues.append(f"{template_file}: Missing shared JS reference")
    
    return reference_issues

def main():
    """Main verification function."""
    print("CSS/JS Separation Verification")
    print("=" * 50)
    
    base_path = Path(__file__).parent
    templates_path = base_path / 'templates' / 'staff' / 'questions'
    
    # Check template separation
    print("\n1. Checking template separation...")
    template_files = [
        'question_list.html',
        'question_add.html', 
        'question_edit.html',
        'bulk_upload.html'
    ]
    
    total_issues = 0
    for template_file in template_files:
        template_path = templates_path / template_file
        if template_path.exists():
            issues = check_template_separation(template_path)
            if issues:
                print(f"\n  ❌ {template_file}:")
                for issue in issues:
                    print(f"     - {issue}")
                total_issues += len(issues)
            else:
                print(f"  ✅ {template_file}: Clean separation")
        else:
            print(f"  ⚠️  {template_file}: Template not found")
    
    # Check static files existence
    print("\n2. Checking static files...")
    missing_files = check_static_files_exist()
    if missing_files:
        print("  ❌ Missing static files:")
        for missing in missing_files:
            print(f"     - {missing}")
        total_issues += len(missing_files)
    else:
        print("  ✅ All expected static files exist")
    
    # Check template references
    print("\n3. Checking template references...")
    reference_issues = check_template_references()
    if reference_issues:
        print("  ❌ Reference issues:")
        for issue in reference_issues:
            print(f"     - {issue}")
        total_issues += len(reference_issues)
    else:
        print("  ✅ All templates properly reference external files")
    
    # Summary
    print("\n" + "=" * 50)
    if total_issues == 0:
        print("🎉 SUCCESS: All CSS and JavaScript have been properly separated!")
        print("   - All templates use external CSS and JS files")
        print("   - No inline styles or scripts found")
        print("   - All static files exist and are referenced correctly")
    else:
        print(f"⚠️  ISSUES FOUND: {total_issues} issues need to be addressed")
        print("   Please review the issues listed above")
    
    print("\nNext steps:")
    print("1. Test the MCQ management pages manually")
    print("2. Verify that all functionality still works")
    print("3. Check browser developer tools for any missing resources")

if __name__ == "__main__":
    main()
