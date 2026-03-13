import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from core.models import Question, Subject, Tag, Topic


@pytest.mark.django_db
@pytest.mark.integration
def test_staff_can_create_question_with_options(staff_client, subject_with_questions):
    topic = subject_with_questions['topic']

    response = staff_client.post(
        reverse('staff:question_create'),
        data={
            'question_text': 'Which structure filters blood in the kidney?',
            'topic': topic.pk,
            'difficulty': 'medium',
            'explanation': 'The glomerulus is the primary filtration barrier.',
            'reference': 'Guyton',
            'is_active': 'on',
            'option_0_text': 'Loop of Henle',
            'option_1_text': 'Glomerulus',
            'option_2_text': 'Collecting duct',
            'option_3_text': 'Distal tubule',
            'correct_answer': '1',
        },
        follow=False,
    )

    assert response.status_code == 302
    assert response.url == reverse('staff:question_list')

    question = Question.objects.get(question_text='Which structure filters blood in the kidney?')
    assert question.topic == topic
    assert question.options.count() == 4
    assert question.correct_option.option_text == 'Glomerulus'


@pytest.mark.django_db
@pytest.mark.integration
def test_staff_can_bulk_upload_topics_and_tags(staff_client):
    csv_content = (
        'LOs,Sub-Topic,Topic,Subject,Type,Module,Assessment\n'
        'Explain nephron structure,Nephron,Renal Physiology,Physiology,Major Subject,Foundation,MCQS\n'
    )
    upload = SimpleUploadedFile('topics.csv', csv_content.encode('utf-8'), content_type='text/csv')

    response = staff_client.post(
        reverse('staff:topic_bulk_upload'),
        data={
            'csv_file': upload,
            'create_subjects': 'on',
            'create_tags': 'on',
        },
        follow=False,
    )

    assert response.status_code == 302
    assert response.url == reverse('staff:topic_list')

    subject = Subject.objects.get(name='Physiology')
    topic = Topic.objects.get(subject=subject, name='Renal Physiology')
    assert topic.description == 'Explain nephron structure'
    assert topic.tags.filter(name='Topic: Renal Physiology').exists()
    assert Tag.objects.filter(name='Sub-Topic: Nephron').exists()
