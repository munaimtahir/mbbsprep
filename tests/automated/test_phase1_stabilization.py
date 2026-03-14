from pathlib import Path

import pytest
from django.conf import settings
from django.urls import NoReverseMatch, reverse

from core.models import QuizSession


@pytest.mark.django_db
@pytest.mark.integration
def test_gap008_quick_start_uses_quiz_endpoint_and_starts_session(
    authenticated_client,
    student_user,
    subject_with_questions,
):
    topic = subject_with_questions['topic']

    quiz_page = authenticated_client.get(reverse('core:quiz'))
    assert quiz_page.status_code == 200
    assert b'action="/quiz/"' in quiz_page.content
    assert b'/quiz/topic/0/' not in quiz_page.content

    start_response = authenticated_client.post(
        reverse('core:quiz'),
        data={
            'topic': topic.pk,
            'difficulty': 'all',
            'number_of_questions': 5,
            'time_limit': 30,
        },
        follow=False,
    )

    assert start_response.status_code == 302
    quiz_session = QuizSession.objects.get(user=student_user, topic=topic, status='in_progress')
    assert start_response.url == reverse('core:quiz_session', kwargs={'pk': quiz_session.pk})


@pytest.mark.django_db
@pytest.mark.integration
def test_gap008_quick_start_handles_missing_and_invalid_topic_gracefully(authenticated_client):
    missing_topic_response = authenticated_client.post(
        reverse('core:quiz'),
        data={
            'difficulty': 'all',
            'number_of_questions': 5,
            'time_limit': 30,
        },
        follow=False,
    )
    assert missing_topic_response.status_code == 200
    assert 'topic' in missing_topic_response.context['form'].errors

    invalid_topic_response = authenticated_client.post(
        reverse('core:quiz'),
        data={
            'topic': 999999,
            'difficulty': 'all',
            'number_of_questions': 5,
            'time_limit': 30,
        },
        follow=False,
    )
    assert invalid_topic_response.status_code == 200
    assert 'topic' in invalid_topic_response.context['form'].errors


@pytest.mark.django_db
@pytest.mark.integration
def test_gap008_quick_start_shows_truthful_unavailable_state_without_topics(authenticated_client):
    response = authenticated_client.get(reverse('core:quiz'))

    assert response.status_code == 200
    assert b'Quick Start is unavailable because there are currently no quiz topics available for your account.' in response.content
    assert b'class="quiz-form"' not in response.content


@pytest.mark.django_db
@pytest.mark.integration
def test_gap012_legacy_quiz_js_is_retired_from_runtime_pages(
    authenticated_client,
    student_user,
    subject_with_questions,
):
    topic = subject_with_questions['topic']

    quiz_center = authenticated_client.get(reverse('core:quiz'))
    start_page = authenticated_client.get(reverse('core:start_quiz', kwargs={'topic_id': topic.pk}))
    start_response = authenticated_client.post(
        reverse('core:start_quiz', kwargs={'topic_id': topic.pk}),
        data={
            'topic': topic.pk,
            'difficulty': 'all',
            'number_of_questions': 5,
            'time_limit': 30,
        },
        follow=False,
    )
    quiz_session = QuizSession.objects.get(user=student_user, topic=topic, status='in_progress')
    session_page = authenticated_client.get(reverse('core:quiz_session', kwargs={'pk': quiz_session.pk}))

    assert quiz_center.status_code == 200
    assert start_page.status_code == 200
    assert start_response.status_code == 302
    assert session_page.status_code == 200

    for response in (quiz_center, start_page, session_page):
        assert b'core/js/quiz.js' not in response.content

    assert not Path(settings.BASE_DIR / 'static/core/js/quiz.js').exists()


@pytest.mark.django_db
@pytest.mark.integration
def test_gap014_staff_tag_views_render_canonical_tag_paths(staff_client, tag):
    tag_list_response = staff_client.get(reverse('staff:tag_list'))

    assert tag_list_response.status_code == 200
    assert reverse('staff:tag_create_ajax').encode() in tag_list_response.content
    assert reverse('staff:subtag_create_ajax').encode() in tag_list_response.content
    assert reverse('staff:subtag_update_ajax', kwargs={'pk': 0}).encode() in tag_list_response.content
    assert b'/staff/tags/add/' not in tag_list_response.content


@pytest.mark.django_db
@pytest.mark.integration
def test_gap014_noncanonical_tag_route_aliases_are_not_resolvable():
    with pytest.raises(NoReverseMatch):
        reverse('staff:tag_create')
    with pytest.raises(NoReverseMatch):
        reverse('staff:tag_edit', kwargs={'pk': 1})
    with pytest.raises(NoReverseMatch):
        reverse('staff:tag_add')
    with pytest.raises(NoReverseMatch):
        reverse('staff:ajax_tag_create')
    with pytest.raises(NoReverseMatch):
        reverse('staff:subtag_create')
    with pytest.raises(NoReverseMatch):
        reverse('staff:subtag_edit', kwargs={'pk': 1})


@pytest.mark.django_db
@pytest.mark.integration
def test_gap015_support_and_contact_surfaces_are_truthful(client, staff_client):
    faq_response = client.get(reverse('core:faq'))
    contact_get_response = client.get(reverse('core:contact'))
    contact_post_response = client.post(
        reverse('core:contact'),
        data={
            'name': 'Amina Raza',
            'email': 'amina@example.com',
            'subject': 'general',
            'message': 'Need support details.',
        },
        follow=False,
    )
    support_inbox_response = staff_client.get(reverse('staff:support_inbox'))

    assert faq_response.status_code == 200
    assert b'href="/help/"' not in faq_response.content
    assert reverse('core:about').encode() in faq_response.content

    assert contact_get_response.status_code == 200
    assert b'our team will follow up' not in contact_get_response.content
    assert b'form currently validates submissions only' in contact_get_response.content

    assert contact_post_response.status_code == 200
    assert b'Thanks for reaching out. This form currently validates submissions only' in contact_post_response.content

    assert support_inbox_response.status_code == 200
    assert b'underlying support/message model has not been implemented' in support_inbox_response.content
