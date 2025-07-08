#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medprep.settings")
    django.setup()
    
    # Test imports
    try:
        from staff.views import (
            SubjectListView, TopicListEnhancedView, 
            TopicCreateAjaxEnhancedView, TopicEditAjaxEnhancedView,
            TopicToggleStatusView, TopicDeleteView
        )
        print("✅ All views imported successfully!")
        
        # Test template existence
        template_paths = [
            'templates/staff/subjects/subject_form.html',
            'templates/staff/topics/topic_list_new.html',
            'templates/staff/topics/topic_form.html',
        ]
        
        for template_path in template_paths:
            if os.path.exists(template_path):
                print(f"✅ Template exists: {template_path}")
            else:
                print(f"❌ Template missing: {template_path}")
        
        # Test static file existence
        static_paths = [
            'static/staff/css/subjects.css',
            'static/staff/css/subject_form.css', 
            'static/staff/css/topics.css',
            'static/staff/js/subjects.js',
            'static/staff/js/subject_form.js',
            'static/staff/js/topics.js',
            'static/staff/js/topic_form.js',
            'static/staff/js/subjects_shared.js',
            'static/staff/js/topics_shared.js'
        ]
        
        for static_path in static_paths:
            if os.path.exists(static_path):
                print(f"✅ Static file exists: {static_path}")
            else:
                print(f"❌ Static file missing: {static_path}")
        
        print("\n🎉 Basic verification complete!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
