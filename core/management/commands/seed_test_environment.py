from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from core.models import Option, Question, Subject, SubscriptionPlan, Topic, UserProfile


class Command(BaseCommand):
    help = 'Seed deterministic users, plans, and quiz data for automated tests.'

    def handle(self, *args, **options):
        student, _ = User.objects.get_or_create(
            username='playwright_student',
            defaults={
                'email': 'playwright.student@example.com',
                'first_name': 'Playwright',
                'last_name': 'Student',
            },
        )
        student.set_password('PlaywrightPass123!')
        student.save()

        UserProfile.objects.get_or_create(
            user=student,
            defaults={
                'year_of_study': '1st_year',
                'province': 'Punjab',
                'college_type': 'Public',
                'college_name': 'King Edward Medical University (Lahore)',
                'phone_number': '03001234567',
            },
        )

        staff_user, _ = User.objects.get_or_create(
            username='playwright_staff',
            defaults={
                'email': 'playwright.staff@example.com',
                'first_name': 'Playwright',
                'last_name': 'Staff',
                'is_staff': True,
            },
        )
        staff_user.is_staff = True
        staff_user.set_password('PlaywrightStaff123!')
        staff_user.save()

        subject, _ = Subject.objects.get_or_create(
            code='PLY',
            defaults={
                'name': 'Playwright Medicine',
                'description': 'Stable subject for automated tests.',
                'year_applicable': 'all',
                'is_active': True,
            },
        )
        topic, _ = Topic.objects.get_or_create(
            subject=subject,
            name='Automated Quiz Topic',
            defaults={
                'description': 'Topic used by Playwright and pytest automation.',
                'order': 1,
                'is_active': True,
            },
        )

        if topic.questions.count() < 5:
            existing_count = topic.questions.count()
            for index in range(existing_count, 5):
                question = Question.objects.create(
                    topic=topic,
                    question_text=f'Automated question {index + 1}?',
                    explanation='Deterministic explanation for automated tests.',
                    reference='Automation',
                    difficulty='easy',
                    is_premium=False,
                    is_active=True,
                )
                Option.objects.bulk_create(
                    [
                        Option(
                            question=question,
                            option_text='Correct answer',
                            is_correct=True,
                            order=1,
                        ),
                        Option(
                            question=question,
                            option_text='Distractor 1',
                            is_correct=False,
                            order=2,
                        ),
                        Option(
                            question=question,
                            option_text='Distractor 2',
                            is_correct=False,
                            order=3,
                        ),
                        Option(
                            question=question,
                            option_text='Distractor 3',
                            is_correct=False,
                            order=4,
                        ),
                    ]
                )

        for plan_type, name, price, duration in [
            ('monthly', 'Monthly Premium', '1500.00', 30),
            ('quarterly', 'Quarterly Premium', '4000.00', 90),
            ('yearly', 'Yearly Premium', '14000.00', 365),
        ]:
            SubscriptionPlan.objects.update_or_create(
                plan_type=plan_type,
                defaults={
                    'name': name,
                    'price': price,
                    'duration_days': duration,
                    'features': 'Automated test plan',
                    'is_active': True,
                },
            )

        self.stdout.write(self.style.SUCCESS('Automated test environment is ready.'))
