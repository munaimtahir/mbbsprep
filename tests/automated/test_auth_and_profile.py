import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from core.models import UserProfile


@pytest.mark.django_db
@pytest.mark.integration
def test_signup_page_loads(client):
    response = client.get(reverse('core:signup'))

    assert response.status_code == 200
    assert b'Register' in response.content or b'Sign Up' in response.content


@pytest.mark.django_db
@pytest.mark.integration
def test_signup_creates_user_profile_and_redirects_to_dashboard(client):
    response = client.post(
        reverse('core:signup'),
        data={
            'first_name': 'Ayesha',
            'last_name': 'Khan',
            'email': 'ayesha@example.com',
            'username': 'ayesha',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'year_of_study': '1st_year',
            'province': 'Punjab',
            'college_type': 'Public',
            'college_name': 'King Edward Medical University (Lahore)',
            'phone_number': '03001234567',
        },
        follow=False,
    )

    assert response.status_code == 302
    assert response.url == reverse('core:dashboard')
    user = User.objects.get(username='ayesha')
    profile = UserProfile.objects.get(user=user)
    assert profile.college_name == 'King Edward Medical University (Lahore)'


@pytest.mark.django_db
@pytest.mark.integration
def test_login_accepts_email_address(client, student_user):
    response = client.post(
        reverse('core:login'),
        data={'username': student_user.email, 'password': 'StudentPass123!'},
        follow=False,
    )

    assert response.status_code == 302
    assert response.url == reverse('core:dashboard')


@pytest.mark.django_db
@pytest.mark.integration
def test_logout_clears_authenticated_access(authenticated_client):
    logout_response = authenticated_client.get(reverse('core:logout'))

    assert logout_response.status_code == 200
    assert b'Successfully Logged Out' in logout_response.content

    dashboard_response = authenticated_client.get(reverse('core:dashboard'))
    assert dashboard_response.status_code == 302
    assert reverse('core:login') in dashboard_response.url


@pytest.mark.django_db
@pytest.mark.integration
def test_profile_pages_render_for_authenticated_user(authenticated_client, completed_quiz):
    profile_response = authenticated_client.get(reverse('core:profile'))
    edit_response = authenticated_client.get(reverse('core:profile_edit'))

    assert profile_response.status_code == 200
    assert edit_response.status_code == 200


@pytest.mark.django_db
@pytest.mark.integration
def test_dashboard_loads_for_authenticated_user(authenticated_client, completed_quiz):
    response = authenticated_client.get(reverse('core:dashboard'))

    assert response.status_code == 200
    assert b'Dashboard' in response.content


@pytest.mark.django_db
@pytest.mark.integration
def test_profile_update_persists_changes(authenticated_client, student_user):
    response = authenticated_client.post(
        reverse('core:profile_edit'),
        data={
            'year_of_study': '2nd_year',
            'province': 'Sindh',
            'college_type': 'Private',
            'college_name': 'Updated Medical College',
            'phone_number': '03111222333',
        },
        follow=False,
    )

    assert response.status_code == 302

    student_user.userprofile.refresh_from_db()
    assert student_user.userprofile.year_of_study == '2nd_year'
    assert student_user.userprofile.province == 'Sindh'
    assert student_user.userprofile.college_name == 'Updated Medical College'
