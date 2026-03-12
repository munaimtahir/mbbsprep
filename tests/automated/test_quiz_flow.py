import pytest
from django.urls import reverse

from core.models import QuizSession


@pytest.mark.django_db
@pytest.mark.integration
def test_student_can_complete_quiz_and_profile_stats_update(
    authenticated_client,
    student_user,
    subject_with_questions,
):
    topic = subject_with_questions['topic']

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

    assert start_response.status_code == 302
    quiz_session = QuizSession.objects.get(user=student_user, topic=topic, status='in_progress')

    for question in quiz_session.questions.all():
        correct_option = question.correct_option
        answer_response = authenticated_client.post(
            reverse(
                'core:quiz_question',
                kwargs={'pk': quiz_session.pk, 'question_id': question.pk},
            ),
            data={'selected_option': correct_option.pk, 'time_taken': 10},
        )
        assert answer_response.status_code == 200
        assert answer_response.json()['is_correct'] is True

    submit_response = authenticated_client.post(
        reverse('core:submit_quiz', kwargs={'pk': quiz_session.pk}),
        follow=False,
    )

    quiz_session.refresh_from_db()
    student_user.userprofile.refresh_from_db()

    assert submit_response.status_code == 302
    assert quiz_session.status == 'completed'
    assert quiz_session.score == 5
    assert student_user.userprofile.total_quizzes_taken == 1
    assert student_user.userprofile.total_quiz_score == 5

    quiz_session.save()
    student_user.userprofile.refresh_from_db()

    assert student_user.userprofile.total_quizzes_taken == 1
    assert student_user.userprofile.total_quiz_score == 5


@pytest.mark.django_db
@pytest.mark.integration
def test_quiz_start_session_and_result_pages_render(
    authenticated_client,
    student_user,
    subject_with_questions,
):
    topic = subject_with_questions['topic']

    start_page = authenticated_client.get(reverse('core:start_quiz', kwargs={'topic_id': topic.pk}))
    assert start_page.status_code == 200

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
    assert start_response.status_code == 302

    quiz_session = QuizSession.objects.get(user=student_user, topic=topic, status='in_progress')

    session_page = authenticated_client.get(reverse('core:quiz_session', kwargs={'pk': quiz_session.pk}))
    assert session_page.status_code == 200
    assert topic.name.encode() in session_page.content

    for question in quiz_session.questions.all():
        authenticated_client.post(
            reverse('core:quiz_question', kwargs={'pk': quiz_session.pk, 'question_id': question.pk}),
            data={'selected_option': question.correct_option.pk, 'time_taken': 5},
        )

    authenticated_client.post(reverse('core:submit_quiz', kwargs={'pk': quiz_session.pk}), follow=False)

    result_page = authenticated_client.get(reverse('core:quiz_result', kwargs={'pk': quiz_session.pk}))
    assert result_page.status_code == 200
    assert b'Question Review' in result_page.content


@pytest.mark.django_db
@pytest.mark.integration
def test_quiz_results_history_page_lists_completed_attempts(authenticated_client, completed_quiz):
    response = authenticated_client.get(reverse('core:results'))

    assert response.status_code == 200
    assert completed_quiz.topic.name.encode() in response.content
    assert b'Completed quizzes' in response.content
