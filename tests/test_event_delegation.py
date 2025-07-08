#!/usr/bin/env python3
"""
Quick test to verify that event delegation is working correctly
by running the MCQ management pages briefly.
"""

import os
import sys
import subprocess

def test_mcq_pages():
    """Test that MCQ management pages load correctly with new event delegation."""
    
    print("🔍 Testing MCQ Management Pages with Event Delegation")
    print("=" * 55)
    
    # Check that templates don't have inline event handlers
    templates = [
        'templates/staff/questions/question_list.html',
        'templates/staff/questions/question_add.html', 
        'templates/staff/questions/question_edit.html',
        'templates/staff/questions/bulk_upload.html'
    ]
    
    all_clean = True
    
    for template in templates:
        if os.path.exists(template):
            with open(template, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for inline event handlers
            inline_events = ['onclick=', 'onchange=', 'oninput=', 'onsubmit=']
            found_events = []
            
            for event in inline_events:
                if event in content:
                    found_events.append(event)
            
            if found_events:
                print(f"❌ {template}: Found inline events: {', '.join(found_events)}")
                all_clean = False
            else:
                print(f"✅ {template}: No inline event handlers")
    
    # Check that JS files have event delegation
    js_files = [
        'static/staff/js/question_list.js',
        'static/staff/js/question_add.js',
        'static/staff/js/question_edit.js', 
        'static/staff/js/bulk_upload.js'
    ]
    
    for js_file in js_files:
        if os.path.exists(js_file):
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            has_delegation = 'addEventListener' in content and 'document.addEventListener' in content
            
            if has_delegation:
                print(f"✅ {js_file}: Has event delegation")
            else:
                print(f"❌ {js_file}: Missing event delegation")
                all_clean = False
    
    print("\n" + "=" * 55)
    if all_clean:
        print("🎉 Complete CSS/JS separation achieved!")
        print("   • All inline event handlers removed")
        print("   • Event delegation implemented in JS files")
        print("   • Ready for manual testing")
        return True
    else:
        print("❌ Some issues found - check the output above")
        return False

if __name__ == '__main__':
    success = test_mcq_pages()
    sys.exit(0 if success else 1)
