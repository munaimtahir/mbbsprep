import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.integration
def test_public_note_routes_render(client, note_resource):
    list_response = client.get(reverse('core:notes_list'))
    detail_response = client.get(reverse('core:note_detail', kwargs={'pk': note_resource.pk}))

    assert list_response.status_code == 200
    assert detail_response.status_code == 200
    assert note_resource.title.encode() in detail_response.content


@pytest.mark.django_db
@pytest.mark.integration
def test_public_video_routes_render(client, video_resource):
    list_response = client.get(reverse('core:videos_list'))
    detail_response = client.get(reverse('core:video_detail', kwargs={'pk': video_resource.pk}))

    assert list_response.status_code == 200
    assert detail_response.status_code == 200
    assert video_resource.title.encode() in detail_response.content


@pytest.mark.django_db
@pytest.mark.integration
def test_public_flashcard_routes_render(client, flashcard_resource):
    list_response = client.get(reverse('core:flashcards_list'))
    study_response = client.get(
        reverse('core:flashcard_study', kwargs={'topic_id': flashcard_resource.topic.pk})
    )

    assert list_response.status_code == 200
    assert study_response.status_code == 200
    assert flashcard_resource.front_text.encode() in list_response.content
    assert flashcard_resource.back_text.encode() in study_response.content
