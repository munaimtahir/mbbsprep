import pytest
from django.urls import reverse

from core.models import Subject


@pytest.mark.django_db
@pytest.mark.integration
def test_staff_can_create_and_update_subject(staff_client):
    create_response = staff_client.post(
        reverse('staff:subject_create'),
        data={
            'name': 'Biochemistry',
            'code': 'BIO1',
            'description': 'Foundational metabolism subject.',
            'year_applicable': '1st',
            'is_active': 'true',
        },
        follow=False,
    )

    assert create_response.status_code == 302
    assert create_response.url == reverse('staff:subject_list')

    subject = Subject.objects.get(code='BIO1')
    assert subject.name == 'Biochemistry'
    assert subject.year_applicable == '1st'
    assert subject.is_active is True

    update_response = staff_client.post(
        reverse('staff:subject_edit', kwargs={'pk': subject.pk}),
        data={
            'name': 'Clinical Biochemistry',
            'code': 'BIO1',
            'description': 'Updated subject description.',
            'year_applicable': '2nd',
            'is_active': '',
        },
        follow=False,
    )

    assert update_response.status_code == 302
    assert update_response.url == reverse('staff:subject_list')

    subject.refresh_from_db()
    assert subject.name == 'Clinical Biochemistry'
    assert subject.year_applicable == '2nd'
    assert subject.is_active is False
