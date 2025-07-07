#!/usr/bin/env python3
"""
MedPrep Platform Feature Analysis
This script analyzes the MedPrep platform to identify all features and their implementation status.
"""

import os
import re
import glob
from pathlib import Path

class MedPrepFeatureAnalyzer:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.features = {
            'core_features': [],
            'admin_features': [],
            'implemented': [],
            'partially_implemented': [],
            'needs_development': [],
            'needs_debugging': []
        }
        
    def analyze_models(self):
        """Analyze Django models to understand data structure"""
        models_info = {}
        models_path = self.base_path / 'core' / 'models'
        
        if models_path.exists():
            for model_file in models_path.glob('*.py'):
                if model_file.name != '__init__.py':
                    try:
                        with open(model_file, 'r') as f:
                            content = f.read()
                            # Extract class definitions
                            classes = re.findall(r'class\s+(\w+)\(.*?\):', content)
                            models_info[model_file.stem] = classes
                    except Exception as e:
                        print(f"Error reading {model_file}: {e}")
        
        return models_info
    
    def analyze_urls(self):
        """Analyze URL patterns to understand available endpoints"""
        url_patterns = {'core': [], 'staff': []}
        
        # Core app URLs
        core_urls = self.base_path / 'core' / 'urls.py'
        if core_urls.exists():
            try:
                with open(core_urls, 'r') as f:
                    content = f.read()
                    patterns = re.findall(r"path\('([^']*)'[^']*name='([^']*)'", content)
                    url_patterns['core'] = patterns
            except Exception as e:
                print(f"Error reading core URLs: {e}")
        
        # Staff app URLs
        staff_urls = self.base_path / 'staff' / 'urls.py'
        if staff_urls.exists():
            try:
                with open(staff_urls, 'r') as f:
                    content = f.read()
                    patterns = re.findall(r"path\('([^']*)'[^']*name='([^']*)'", content)
                    url_patterns['staff'] = patterns
            except Exception as e:
                print(f"Error reading staff URLs: {e}")
        
        return url_patterns
    
    def analyze_views(self):
        """Analyze view implementations"""
        views_info = {'core': [], 'staff': []}
        
        # Core views
        core_views_path = self.base_path / 'core' / 'views'
        if core_views_path.exists():
            for view_file in core_views_path.glob('*.py'):
                if view_file.name != '__init__.py':
                    try:
                        with open(view_file, 'r') as f:
                            content = f.read()
                            classes = re.findall(r'class\s+(\w+View)\(.*?\):', content)
                            functions = re.findall(r'def\s+(\w+)\(.*?\):', content)
                            views_info['core'].extend([(view_file.stem, c, 'class') for c in classes])
                            views_info['core'].extend([(view_file.stem, f, 'function') for f in functions])
                    except Exception as e:
                        print(f"Error reading {view_file}: {e}")
        
        # Staff views
        staff_views_path = self.base_path / 'staff' / 'views'
        if staff_views_path.exists():
            for view_file in staff_views_path.glob('*.py'):
                if view_file.name != '__init__.py':
                    try:
                        with open(view_file, 'r') as f:
                            content = f.read()
                            classes = re.findall(r'class\s+(\w+View)\(.*?\):', content)
                            functions = re.findall(r'def\s+(\w+)\(.*?\):', content)
                            views_info['staff'].extend([(view_file.stem, c, 'class') for c in classes])
                            views_info['staff'].extend([(view_file.stem, f, 'function') for f in functions])
                    except Exception as e:
                        print(f"Error reading {view_file}: {e}")
        
        return views_info
    
    def analyze_templates(self):
        """Analyze template files to understand UI implementation"""
        templates_info = {'core': [], 'staff': []}
        
        # Core templates
        core_templates = self.base_path / 'templates' / 'core'
        if core_templates.exists():
            for template_file in core_templates.rglob('*.html'):
                templates_info['core'].append(template_file.relative_to(core_templates))
        
        # Staff templates  
        staff_templates = self.base_path / 'templates' / 'staff'
        if staff_templates.exists():
            for template_file in staff_templates.rglob('*.html'):
                templates_info['staff'].append(template_file.relative_to(staff_templates))
        
        return templates_info
    
    def analyze_documentation(self):
        """Analyze implementation summary documents"""
        docs_info = {}
        
        # Find all .md files in the root
        for doc_file in self.base_path.glob('*IMPLEMENTATION*.md'):
            try:
                with open(doc_file, 'r') as f:
                    content = f.read()
                    # Look for completed features marked with ✅
                    completed = re.findall(r'✅[^✅]*?(?=\n|$)', content, re.MULTILINE)
                    # Look for pending features marked with ❌ or 🔄 or [ ]
                    pending = re.findall(r'(?:❌|🔄|\[ \])[^✅]*?(?=\n|$)', content, re.MULTILINE)
                    docs_info[doc_file.name] = {
                        'completed': completed,
                        'pending': pending
                    }
            except Exception as e:
                print(f"Error reading {doc_file}: {e}")
        
        return docs_info
    
    def identify_features_from_project_summary(self):
        """Extract feature list from PROJECT_SUMMARY.md"""
        project_summary = self.base_path / 'PROJECT_SUMMARY.md'
        features = []
        
        if project_summary.exists():
            try:
                with open(project_summary, 'r') as f:
                    content = f.read()
                    
                    # Extract core features section
                    core_section = re.search(r'## 🎯 Core Features(.*?)(?=##|$)', content, re.DOTALL)
                    if core_section:
                        # Find numbered features
                        numbered_features = re.findall(r'### \*\*(\d+\. .*?)\*\*(.*?)(?=###|$)', core_section.group(1), re.DOTALL)
                        for title, description in numbered_features:
                            feature_details = re.findall(r'- (.*?)(?=\n|$)', description)
                            features.append({
                                'title': title.strip(),
                                'details': feature_details
                            })
            except Exception as e:
                print(f"Error reading PROJECT_SUMMARY.md: {e}")
        
        return features
    
    def run_analysis(self):
        """Run complete feature analysis"""
        print("🔍 MedPrep Platform Feature Analysis")
        print("=" * 50)
        
        # Analyze models
        print("\n📊 Data Models Analysis:")
        models = self.analyze_models()
        for model_file, classes in models.items():
            print(f"  {model_file}: {', '.join(classes)}")
        
        # Analyze URLs
        print("\n🌐 URL Patterns Analysis:")
        urls = self.analyze_urls()
        for app, patterns in urls.items():
            print(f"  {app.upper()} app: {len(patterns)} endpoints")
            for url, name in patterns[:5]:  # Show first 5
                print(f"    {url} ({name})")
            if len(patterns) > 5:
                print(f"    ... and {len(patterns) - 5} more")
        
        # Analyze views
        print("\n🎭 Views Analysis:")
        views = self.analyze_views()
        for app, view_list in views.items():
            print(f"  {app.upper()} app: {len(view_list)} views")
            for file, view, type_ in view_list[:5]:  # Show first 5
                print(f"    {file}.{view} ({type_})")
            if len(view_list) > 5:
                print(f"    ... and {len(view_list) - 5} more")
        
        # Analyze templates
        print("\n🎨 Templates Analysis:")
        templates = self.analyze_templates()
        for app, template_list in templates.items():
            print(f"  {app.upper()} app: {len(template_list)} templates")
            for template in template_list[:5]:  # Show first 5
                print(f"    {template}")
            if len(template_list) > 5:
                print(f"    ... and {len(template_list) - 5} more")
        
        # Analyze documentation
        print("\n📚 Implementation Documentation:")
        docs = self.analyze_documentation()
        for doc_name, info in docs.items():
            print(f"  {doc_name}:")
            print(f"    Completed: {len(info['completed'])} items")
            print(f"    Pending: {len(info['pending'])} items")
        
        # Extract features from project summary
        print("\n🎯 Core Features from Project Summary:")
        features = self.identify_features_from_project_summary()
        for i, feature in enumerate(features, 1):
            print(f"  {i}. {feature['title']}")
            for detail in feature['details'][:3]:  # Show first 3 details
                print(f"     - {detail}")
            if len(feature['details']) > 3:
                print(f"     ... and {len(feature['details']) - 3} more details")
        
        return {
            'models': models,
            'urls': urls,
            'views': views,
            'templates': templates,
            'docs': docs,
            'features': features
        }

if __name__ == "__main__":
    base_path = "/home/runner/work/Exam-Prep-Site/Exam-Prep-Site"
    analyzer = MedPrepFeatureAnalyzer(base_path)
    results = analyzer.run_analysis()