import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from core.models import UserProfile


@pytest.mark.django_db
@pytest.mark.integration
def test_staff_bulk_upload_preview_can_be_confirmed_without_reuploading_file(staff_client):
    csv_content = (
        'first_name,last_name,email,password,role,year_of_study,province,college_type,college_name,phone_number,is_premium,is_active\n'
        'Amina,Raza,amina.raza@example.com,TempPass123!,student,1st_year,Punjab,Public,Test Medical College,03001234567,FALSE,TRUE\n'
    )
    upload = SimpleUploadedFile('users.csv', csv_content.encode('utf-8'), content_type='text/csv')

    preview_response = staff_client.post(
        reverse('staff:bulk_user_upload'),
        data={
            'action': 'upload',
            'csv_file': upload,
            'default_password': 'FallbackPass123!',
            'default_role': 'student',
            'send_welcome_emails': '',
            'skip_errors': 'on',
        },
        follow=True,
    )

    assert preview_response.status_code == 200
    assert b'Valid Users' in preview_response.content

    confirm_response = staff_client.post(
        reverse('staff:bulk_user_upload'),
        data={'action': 'confirm'},
        follow=False,
    )

    assert confirm_response.status_code == 302
    assert confirm_response.url == reverse('staff:user_list')
    assert User.objects.filter(email='amina.raza@example.com').exists()


@pytest.mark.django_db
@pytest.mark.integration
def test_staff_bulk_upload_confirm_without_preview_redirects_back_to_upload(staff_client):
    response = staff_client.post(
        reverse('staff:bulk_user_upload'),
        data={'action': 'confirm'},
        follow=False,
    )

    assert response.status_code == 302
    assert response.url == reverse('staff:bulk_user_upload')


@pytest.mark.django_db
@pytest.mark.integration
def test_staff_can_create_user_with_profile_details(staff_client):
    response = staff_client.post(
        reverse('staff:user_create'),
        data={
            'first_name': 'Bilal',
            'last_name': 'Khan',
            'email': 'bilal.khan@example.com',
            'phone_number': '03001112222',
            'password': 'StrongPass123!',
            'confirm_password': 'StrongPass123!',
            'year_of_study': '2nd_year',
            'college_type': 'Private',
            'college_name': 'Test Medical College',
            'province': 'Punjab',
            'user_role': 'faculty',
            'is_premium': 'on',
            'send_welcome_email': '',
            'is_active': 'on',
        },
        follow=False,
    )

    assert response.status_code == 302
    assert response.url == reverse('staff:user_list')

    user = User.objects.get(email='bilal.khan@example.com')
    profile = UserProfile.objects.get(user=user)

    assert user.username == 'bilal.khan@example.com'
    assert user.is_staff is True
    assert user.is_superuser is False
    assert profile.year_of_study == '2nd_year'
    assert profile.college_type == 'Private'
    assert profile.is_premium is True
    assert profile.premium_expires_at is not None
