import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from core.models import (
    Flashcard,
    Note,
    Option,
    PaymentProof,
    Question,
    QuizSession,
    Subject,
    SubscriptionPlan,
    Tag,
    Topic,
    UserProfile,
    VideoResource,
)


@pytest.fixture
def student_user(db):
    user = User.objects.create_user(
        username='student_user',
        email='student@example.com',
        password='StudentPass123!',
        first_name='Student',
        last_name='User',
    )
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.year_of_study = '1st_year'
    profile.province = 'Punjab'
    profile.college_type = 'Public'
    profile.college_name = 'King Edward Medical University (Lahore)'
    profile.save()
    return user


@pytest.fixture
def staff_user(db):
    return User.objects.create_user(
        username='staff_user',
        email='staff@example.com',
        password='StaffPass123!',
        is_staff=True,
    )


@pytest.fixture
def authenticated_client(client, student_user):
    client.force_login(student_user)
    return client


@pytest.fixture
def staff_client(client, staff_user):
    client.force_login(staff_user)
    return client


@pytest.fixture
def monthly_plan(db):
    return SubscriptionPlan.objects.create(
        name='Monthly Premium',
        plan_type='monthly',
        price='1500.00',
        duration_days=30,
        features='Full access',
        is_active=True,
    )


@pytest.fixture
def subject_with_questions(db):
    subject = Subject.objects.create(
        name='Test Anatomy',
        code='TA101',
        description='Subject for automated tests',
        year_applicable='all',
        is_active=True,
    )
    topic = Topic.objects.create(
        subject=subject,
        name='Test Topic',
        description='Topic for quiz automation',
        order=1,
        is_active=True,
    )
    questions = []
    for index in range(5):
        question = Question.objects.create(
            topic=topic,
            question_text=f'Test question {index + 1}?',
            explanation='Automated explanation',
            reference='Automated reference',
            difficulty='easy',
            is_premium=False,
            is_active=True,
        )
        Option.objects.create(question=question, option_text='Correct', is_correct=True, order=1)
        Option.objects.create(question=question, option_text='Wrong 1', is_correct=False, order=2)
        Option.objects.create(question=question, option_text='Wrong 2', is_correct=False, order=3)
        Option.objects.create(question=question, option_text='Wrong 3', is_correct=False, order=4)
        questions.append(question)
    return {'subject': subject, 'topic': topic, 'questions': questions}


@pytest.fixture
def uploaded_gif():
    return SimpleUploadedFile(
        'payment.gif',
        (
            b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00'
            b'\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
        ),
        content_type='image/gif',
    )


@pytest.fixture
def pending_payment(student_user, monthly_plan, uploaded_gif):
    return PaymentProof.objects.create(
        user=student_user,
        subscription_plan=monthly_plan,
        payment_method='jazzcash',
        transaction_id='TXN-1001',
        amount_paid='1500.00',
        payment_screenshot=uploaded_gif,
        status='pending',
    )


@pytest.fixture
def completed_quiz(student_user, subject_with_questions):
    quiz_session = QuizSession.objects.create(
        user=student_user,
        topic=subject_with_questions['topic'],
        status='completed',
        score=4,
        total_questions=5,
        time_limit_minutes=30,
        time_taken_seconds=300,
    )
    quiz_session.questions.set(subject_with_questions['questions'])
    return quiz_session


@pytest.fixture
def note_resource(staff_user, subject_with_questions):
    return Note.objects.create(
        title='Renal Physiology Notes',
        topic=subject_with_questions['topic'],
        content='High-yield renal physiology summary.',
        is_premium=False,
        is_active=True,
        created_by=staff_user,
    )


@pytest.fixture
def flashcard_resource(staff_user, subject_with_questions):
    return Flashcard.objects.create(
        topic=subject_with_questions['topic'],
        front_text='What is the normal serum sodium range?',
        back_text='Approximately 135-145 mEq/L.',
        is_premium=False,
        is_active=True,
        created_by=staff_user,
    )


@pytest.fixture
def video_resource(staff_user, subject_with_questions):
    return VideoResource.objects.create(
        title='Renal Physiology Lecture',
        topic=subject_with_questions['topic'],
        description='Overview lecture for testing.',
        video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        duration_minutes=12,
        is_premium=False,
        is_active=True,
        created_by=staff_user,
    )


@pytest.fixture
def tag():
    return Tag.objects.create(name='High Yield', description='Reusable test tag')
