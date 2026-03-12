import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.smoke
@pytest.mark.parametrize(
    'route_name',
    [
        'core:home',
        'core:signup',
        'core:login',
        'core:subscription',
        'core:resources',
        'core:about',
        'core:contact',
        'core:faq',
        'core:terms',
        'core:privacy',
        'staff:login',
    ],
)
def test_public_routes_render(client, route_name):
    response = client.get(reverse(route_name))

    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.smoke
def test_authenticated_routes_require_login(client, monthly_plan, subject_with_questions):
    protected_routes = [
        reverse('core:dashboard'),
        reverse('core:profile'),
        reverse('core:profile_edit'),
        reverse('core:quiz'),
        reverse('core:payment_status'),
        reverse('core:payment', kwargs={'plan_id': monthly_plan.pk}),
        reverse('core:start_quiz', kwargs={'topic_id': subject_with_questions['topic'].pk}),
        reverse('staff:dashboard'),
    ]

    for route in protected_routes:
        response = client.get(route)
        assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.smoke
def test_staff_routes_render_for_staff_user(staff_client, pending_payment, tag):
    routes = [
        reverse('staff:dashboard'),
        reverse('staff:payment_list'),
        reverse('staff:payment_review', kwargs={'pk': pending_payment.pk}),
        reverse('staff:payment_history'),
        reverse('staff:support_inbox'),
        reverse('staff:support_message', kwargs={'pk': pending_payment.pk}),
        reverse('staff:tag_delete', kwargs={'pk': tag.pk}),
        reverse('staff:resource_list'),
    ]

    for route in routes:
        response = staff_client.get(route)
        assert response.status_code == 200, route
