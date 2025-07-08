#!/usr/bin/env python3
"""
MCQ Template Health Check
Verifies HTML template structure and common issues
"""

import os
import re

def check_template_files():
    """Check MCQ template files for common issues"""
    
    template_dir = "templates/staff/questions"
    templates = [
        "question_list.html",
        "question_add.html", 
        "question_edit.html",
        "bulk_upload.html"
    ]
    
    print("🔍 MCQ Template Health Check")
    print("=" * 40)
    
    issues = []
    successes = []
    
    for template in templates:
        template_path = os.path.join(template_dir, template)
        print(f"\n📄 Checking {template}...")
        
        if not os.path.exists(template_path):
            issues.append(f"❌ {template} - File does not exist")
            continue
        
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Basic structure checks
        checks = [
            (r'{% extends [\'"]staff/base_admin\.html[\'"] %}', "Extends base template"),
            (r'{% load static %}', "Loads static files"),
            (r'{% block title %}', "Has title block"),
            (r'{% block.*content.*%}', "Has content block"),
            (r'<form.*method=[\'"]post[\'"]', "Has POST form"),
            (r'{% csrf_token %}', "Has CSRF token"),
            (r'class=[\'"].*form-control.*[\'"]', "Uses Bootstrap form classes"),
            (r'<button.*type=[\'"]submit[\'"]', "Has submit button"),
        ]
        
        template_successes = []
        template_issues = []
        
        for pattern, description in checks:
            if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
                template_successes.append(f"✅ {description}")
            else:
                template_issues.append(f"⚠️ {description} - missing")
        
        # Template-specific checks
        if template == "question_list.html":
            specific_checks = [
                (r'search.*input', "Has search input"),
                (r'filter', "Has filter options"),
                (r'table.*questions', "Has questions table"),
                (r'pagination', "Has pagination"),
            ]
        elif template == "question_add.html":
            specific_checks = [
                (r'id_subject', "Has subject field"),
                (r'id_topic', "Has topic field"),
                (r'question_text', "Has question text field"),
                (r'option.*text', "Has option fields"),
                (r'difficulty', "Has difficulty field"),
            ]
        elif template == "question_edit.html":
            specific_checks = [
                (r'value=.*{{.*}}', "Has pre-filled values"),
                (r'delete.*button', "Has delete button"),
                (r'reset.*button', "Has reset button"),
            ]
        elif template == "bulk_upload.html":
            specific_checks = [
                (r'file.*input', "Has file input"),
                (r'csv.*excel', "Mentions CSV/Excel"),
                (r'template.*download', "Has template download"),
            ]
        
        for pattern, description in specific_checks:
            if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
                template_successes.append(f"✅ {description}")
            else:
                template_issues.append(f"⚠️ {description} - missing")
        
        # Check for common issues
        common_issues = [
            (r'{{ ?[a-zA-Z_][a-zA-Z0-9_]*\|safe ?}}', "⚠️ Unsafe output (potential XSS)"),
            (r'onclick=.*javascript', "⚠️ Inline JavaScript (should use event listeners)"),
            (r'style=.*[\'"]', "⚠️ Inline styles (should use CSS classes)"),
        ]
        
        for pattern, warning in common_issues:
            if re.search(pattern, content, re.IGNORECASE):
                template_issues.append(warning)
        
        # Display results for this template
        for success in template_successes:
            print(f"   {success}")
        
        for issue in template_issues:
            print(f"   {issue}")
        
        if not template_issues:
            successes.append(f"✅ {template} - All checks passed")
        else:
            issues.extend([f"{template}: {issue}" for issue in template_issues])
        
        # File size check
        file_size = len(content)
        if file_size > 100000:  # 100KB
            issues.append(f"⚠️ {template} - Large file size ({file_size} bytes)")
        else:
            successes.append(f"✅ {template} - Reasonable file size ({file_size} bytes)")
    
    # Summary
    print(f"\n" + "=" * 40)
    print("📊 TEMPLATE HEALTH SUMMARY")
    print("=" * 40)
    
    total_checks = len(successes) + len(issues)
    health_score = (len(successes) / total_checks * 100) if total_checks > 0 else 0
    
    print(f"✅ Passed: {len(successes)}")
    print(f"⚠️ Issues: {len(issues)}")
    print(f"🏥 Health Score: {health_score:.1f}%")
    
    if health_score >= 90:
        print("🟢 Template Status: EXCELLENT")
    elif health_score >= 75:
        print("🟡 Template Status: GOOD")
    else:
        print("🔴 Template Status: NEEDS ATTENTION")
    
    if issues:
        print(f"\n⚠️ Issues to address:")
        for issue in issues:
            print(f"   {issue}")
    
    if health_score >= 75:
        print(f"\n✅ Templates are ready for manual testing!")
    
    return health_score >= 75

if __name__ == "__main__":
    check_template_files()
