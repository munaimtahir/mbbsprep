import pytest
from django.conf import settings
from django.core.management import call_command
from django.db import connection
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.quality
def test_django_system_check_passes():
    call_command('check')


@pytest.mark.django_db
@pytest.mark.quality
def test_database_connection_is_usable():
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
        row = cursor.fetchone()

    assert row == (1,)


@pytest.mark.django_db
@pytest.mark.quality
def test_core_url_contracts_reverse(monthly_plan, subject_with_questions):
    assert reverse('core:home') == '/'
    assert reverse('core:payment', kwargs={'plan_id': monthly_plan.pk}).startswith(
        '/subscription/payment/'
    )
    start_quiz_url = reverse(
        'core:start_quiz',
        kwargs={'topic_id': subject_with_questions['topic'].pk},
    )
    assert start_quiz_url.startswith('/quiz/topic/')


@pytest.mark.quality
def test_internationalization_settings_are_enabled():
    assert settings.USE_I18N is True
    assert settings.USE_TZ is True
    assert settings.TIME_ZONE == 'UTC'
