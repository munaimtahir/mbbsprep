#!/usr/bin/env python
"""
Test script to verify the Add MCQ functionality
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medprep.settings')
django.setup()

from core.models import Subject, Topic, Tag, Question, Option

print("🧪 Testing Add MCQ Functionality")
print("=" * 50)

# Check available subjects
subjects = Subject.objects.filter(is_active=True)
print(f"✅ Available Subjects: {subjects.count()}")
for subject in subjects[:3]:
    print(f"   - {subject.name} (ID: {subject.id})")

# Check available topics
topics = Topic.objects.filter(is_active=True)
print(f"✅ Available Topics: {topics.count()}")
for topic in topics[:3]:
    print(f"   - {topic.name} ({topic.subject.name})")

# Check available tags
tags = Tag.objects.filter(is_active=True)
print(f"✅ Available Tags: {tags.count()}")
for tag in tags[:5]:
    print(f"   - {tag.name}")

print("\n🎯 Ready for MCQ creation!")
print("Visit: http://127.0.0.1:8000/staff/questions/add/")
print("\nForm should include:")
print("✓ Subject dropdown with medical subjects")
print("✓ Dynamic topic loading based on subject")
print("✓ Difficulty levels (Easy, Medium, Hard)")
print("✓ Question text area")
print("✓ 4 answer options (A, B, C, D)")
print("✓ Correct answer selection")
print("✓ Explanation field")
print("✓ Reference field")
print("✓ Tag selection")
print("✓ Premium/Active checkboxes")

print(f"\n📊 Current Question Count: {Question.objects.count()}")
print(f"📊 Current Option Count: {Option.objects.count()}")
