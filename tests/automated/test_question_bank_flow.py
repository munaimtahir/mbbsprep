import pytest
from django.urls import reverse

from core.models import Subject, Topic


@pytest.mark.django_db
@pytest.mark.integration
def test_question_bank_filters_subjects_by_year_and_loads_topics_for_selected_subject(
    client,
    subject_with_questions,
):
    off_year_subject = Subject.objects.create(
        name='Second Year Pathology',
        code='PATH2',
        description='Off-year subject for question bank filtering',
        year_applicable='2nd',
        is_active=True,
    )
    off_year_topic = Topic.objects.create(
        subject=off_year_subject,
        name='Cell Injury',
        description='Pathology topic that should not appear for 1st year filter',
        order=1,
        is_active=True,
    )

    response = client.get(
        reverse('core:question_bank'),
        data={
            'year': '1st',
            'subject': subject_with_questions['subject'].pk,
        },
    )

    assert response.status_code == 200
    assert subject_with_questions['subject'] in response.context['subjects']
    assert off_year_subject not in response.context['subjects']
    assert list(response.context['topics']) == [subject_with_questions['topic']]
    assert subject_with_questions['topic'].name.encode() in response.content
    assert off_year_topic.name.encode() not in response.content
