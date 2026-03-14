import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import reverse

from core.models import Question, QuizSession, Subject


@pytest.mark.django_db
@pytest.mark.integration
def test_topic_detail_renders_with_real_contract(client, subject_with_questions):
    topic = subject_with_questions['topic']

    response = client.get(reverse('core:topic_detail', kwargs={'pk': topic.pk}))

    assert response.status_code == 200
    assert topic.name.encode() in response.content
    assert reverse('core:start_quiz', kwargs={'topic_id': topic.pk}).encode() in response.content
    assert b'bookmark_topic' not in response.content
    assert b'add_comment' not in response.content


@pytest.mark.django_db
@pytest.mark.integration
def test_contact_page_uses_backend_form_contract(client):
    get_response = client.get(reverse('core:contact'))
    assert get_response.status_code == 200
    assert b'name="name"' in get_response.content
    assert b'name="email"' in get_response.content
    assert b'name="subject"' in get_response.content
    assert b'name="message"' in get_response.content

    post_response = client.post(
        reverse('core:contact'),
        data={
            'name': 'Amina Raza',
            'email': 'amina@example.com',
            'subject': 'general',
            'message': 'I need help with accessing quiz history.',
        },
        follow=False,
    )
    assert post_response.status_code == 200
    assert 'form' in post_response.context
    assert post_response.context['form'].is_bound is False

    invalid_response = client.post(
        reverse('core:contact'),
        data={
            'name': '',
            'email': 'amina@example.com',
            'subject': 'general',
            'message': 'Still need help.',
        },
        follow=False,
    )
    assert invalid_response.status_code == 200
    assert invalid_response.context['form'].is_bound is True
    assert 'name' in invalid_response.context['form'].errors


@pytest.mark.django_db
@pytest.mark.integration
def test_staff_bulk_question_upload_succeeds_with_current_schema(staff_client):
    csv_content = (
        'Subject,Topic,Question Text,Option A,Option B,Option C,Option D,Option E,Option F,'
        'Correct Answer,Difficulty,Tags,Explanation,Reference\n'
        'Physiology,Cardiac Cycle,Which node is the natural pacemaker?,AV node,SA node,'
        'Bundle branch,Purkinje fibers,,,B,Easy,High Yield,SA node initiates impulse,Guyton p.115\n'
    )
    upload = SimpleUploadedFile('mcqs.csv', csv_content.encode('utf-8'), content_type='text/csv')

    response = staff_client.post(
        reverse('staff:bulk_question_upload'),
        data={'csv_file': upload},
        follow=False,
    )

    assert response.status_code == 302
    assert response.url == reverse('staff:question_list')

    question = Question.objects.get(question_text='Which node is the natural pacemaker?')
    assert question.options.count() == 4
    assert question.correct_option.option_text == 'SA node'
    assert list(question.options.values_list('order', flat=True)) == [1, 2, 3, 4]


@pytest.mark.django_db
@pytest.mark.integration
def test_staff_bulk_question_upload_shows_validation_error_for_bad_columns(staff_client):
    csv_content = 'question_text,topic,difficulty,option_a,option_b,correct_answer\nBad row,Cardiology,easy,A,B,B\n'
    upload = SimpleUploadedFile('mcqs.csv', csv_content.encode('utf-8'), content_type='text/csv')

    response = staff_client.post(
        reverse('staff:bulk_question_upload'),
        data={'csv_file': upload},
        follow=False,
    )

    assert response.status_code == 200
    assert 'form' in response.context
    assert 'csv_file' in response.context['form'].errors
    assert 'CSV must contain these columns' in str(response.context['form'].errors['csv_file'][0])


@pytest.mark.django_db
@pytest.mark.integration
def test_staff_quiz_attempts_route_renders_clean_placeholder(staff_client):
    response = staff_client.get(reverse('staff:quiz_list'))

    assert response.status_code == 200
    assert b'All Quiz Attempts' in response.content
    assert b'truthful placeholder' in response.content


@pytest.mark.django_db
@pytest.mark.integration
def test_user_export_uses_status_based_quiz_completion(staff_client, student_user, subject_with_questions):
    topic = subject_with_questions['topic']
    QuizSession.objects.create(
        user=student_user,
        topic=topic,
        status='completed',
        score=3,
        total_questions=5,
    )
    QuizSession.objects.create(
        user=student_user,
        topic=topic,
        status='in_progress',
        score=0,
        total_questions=5,
    )

    single_response = staff_client.get(
        reverse('staff:user_export_single', kwargs={'pk': student_user.pk})
    )
    assert single_response.status_code == 200
    single_csv = single_response.content.decode('utf-8')
    assert 'Field,Value' in single_csv
    assert 'Total Quiz Sessions,2' in single_csv
    assert 'Completed Sessions,1' in single_csv

    multi_response = staff_client.get(reverse('staff:user_export'))
    assert multi_response.status_code == 200
    multi_csv = multi_response.content.decode('utf-8')
    assert 'ID,Username,Email,First Name,Last Name' in multi_csv
    assert 'Field,Value' not in multi_csv
    assert '--- Quiz Statistics ---' not in multi_csv


@pytest.mark.django_db
@pytest.mark.integration
def test_subject_detail_handles_zero_topics_truthfully(client):
    subject = Subject.objects.create(
        name='Histology',
        code='HISTO1',
        description='No topics yet.',
        year_applicable='all',
        is_active=True,
    )

    response = client.get(reverse('core:subject_detail', kwargs={'pk': subject.pk}))

    assert response.status_code == 200
    assert b'Topics will appear here soon' in response.content
    assert b'No Topics Available' in response.content


@pytest.mark.django_db
@pytest.mark.integration
def test_subject_ajax_add_requires_csrf_and_accepts_valid_csrf(staff_user):
    csrf_client = Client(enforce_csrf_checks=True)
    csrf_client.force_login(staff_user)
    ajax_url = reverse('staff:subject_ajax_add')

    forbidden_response = csrf_client.post(
        ajax_url,
        data={'name': 'Protected Subject', 'code': 'CSRF1', 'is_active': 'true'},
    )
    assert forbidden_response.status_code == 403

    page_response = csrf_client.get(reverse('staff:subject_list'))
    token = page_response.cookies['csrftoken'].value

    allowed_response = csrf_client.post(
        ajax_url,
        data={'name': 'Protected Subject', 'code': 'CSRF1', 'is_active': 'true'},
        HTTP_X_CSRFTOKEN=token,
    )
    assert allowed_response.status_code == 200
    assert allowed_response.json()['success'] is True


@pytest.mark.django_db
@pytest.mark.integration
def test_resources_and_leaderboard_pages_do_not_load_dead_ajax_scripts(client):
    resources_response = client.get(reverse('core:resources'))
    leaderboard_response = client.get(reverse('core:leaderboard'))

    assert resources_response.status_code == 200
    assert leaderboard_response.status_code == 200
    assert b'core/js/resources.js' not in resources_response.content
    assert b'core/js/leaderboard.js' not in leaderboard_response.content
