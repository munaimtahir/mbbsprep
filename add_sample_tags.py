#!/usr/bin/env python
"""
Add sample tags and assign them to questions for testing MCQ management
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medprep.settings')
django.setup()

from core.models import Tag, Question
import random

# Create sample tags
tag_data = [
    {'name': 'High Yield', 'color': '#43B284', 'description': 'High-yield questions for exams'},
    {'name': 'Easy', 'color': '#43B284', 'description': 'Easy difficulty level'},
    {'name': 'Moderate', 'color': '#FFB74D', 'description': 'Moderate difficulty level'},
    {'name': 'Challenging', 'color': '#FF7043', 'description': 'Challenging questions'},
    {'name': 'Clinical', 'color': '#0057A3', 'description': 'Clinical scenario based'},
    {'name': 'Theory', 'color': '#6C757D', 'description': 'Theoretical concepts'},
    {'name': 'Image Based', 'color': '#9C27B0', 'description': 'Contains images or diagrams'},
    {'name': 'Must Know', 'color': '#E91E63', 'description': 'Essential knowledge'},
    {'name': 'MBBS Final', 'color': '#F44336', 'description': 'Final year MBBS level'},
    {'name': 'Quick Review', 'color': '#4CAF50', 'description': 'Quick revision questions'},
]

print("Creating sample tags...")
created_tags = []
for tag_info in tag_data:
    tag, created = Tag.objects.get_or_create(
        name=tag_info['name'],
        defaults={
            'color': tag_info['color'],
            'description': tag_info['description'],
            'is_active': True
        }
    )
    created_tags.append(tag)
    if created:
        print(f"✓ Created tag: {tag.name}")
    else:
        print(f"• Tag already exists: {tag.name}")

print(f"\nAssigning random tags to questions...")
questions = Question.objects.all()
for question in questions:
    # Clear existing tags
    question.tags.clear()
    
    # Assign 1-3 random tags
    num_tags = random.randint(1, 3)
    random_tags = random.sample(created_tags, min(num_tags, len(created_tags)))
    question.tags.set(random_tags)
    
    # Randomly set some as premium
    if random.choice([True, False, False]):  # 33% chance
        question.is_premium = True
        question.save()

print(f"✓ Updated {questions.count()} questions with tags and premium status")

# Print summary
print(f"\n=== Summary ===")
print(f"Total Tags: {Tag.objects.count()}")
print(f"Total Questions: {Question.objects.count()}")
print(f"Premium Questions: {Question.objects.filter(is_premium=True).count()}")
print(f"Active Questions: {Question.objects.filter(is_active=True).count()}")

print(f"\nSample data setup complete! Visit http://localhost:8000/staff/questions/ to see the MCQ management interface.")
