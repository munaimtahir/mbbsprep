import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.integration
def test_staff_subject_topic_question_management_pages_render(
    staff_client,
    subject_with_questions,
):
    question = subject_with_questions['questions'][0]

    routes = [
        reverse('staff:subject_list'),
        reverse('staff:subject_create'),
        reverse('staff:subject_edit', kwargs={'pk': subject_with_questions['subject'].pk}),
        reverse('staff:topic_list'),
        reverse('staff:topic_create'),
        reverse('staff:topic_edit', kwargs={'pk': subject_with_questions['topic'].pk}),
        reverse('staff:question_list'),
        reverse('staff:question_create'),
        reverse('staff:question_edit', kwargs={'pk': question.pk}),
    ]

    for route in routes:
        response = staff_client.get(route)
        assert response.status_code == 200, route


@pytest.mark.django_db
@pytest.mark.integration
def test_staff_resource_management_pages_render(
    staff_client,
    note_resource,
    video_resource,
    flashcard_resource,
):
    routes = [
        reverse('staff:resource_list'),
        reverse('staff:note_list'),
        reverse('staff:note_create'),
        reverse('staff:note_edit', kwargs={'pk': note_resource.pk}),
        reverse('staff:video_list'),
        reverse('staff:video_create'),
        reverse('staff:video_edit', kwargs={'pk': video_resource.pk}),
        reverse('staff:flashcard_list'),
        reverse('staff:flashcard_create'),
        reverse('staff:flashcard_edit', kwargs={'pk': flashcard_resource.pk}),
    ]

    for route in routes:
        response = staff_client.get(route)
        assert response.status_code == 200, route
