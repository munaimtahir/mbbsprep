import pytest
from django.urls import reverse

from core.models import PaymentProof


@pytest.mark.django_db
@pytest.mark.integration
def test_student_can_upload_payment_proof(
    authenticated_client,
    student_user,
    monthly_plan,
    uploaded_gif,
):
    response = authenticated_client.post(
        reverse('core:payment_proof_upload'),
        data={
            'subscription_plan': monthly_plan.pk,
            'payment_method': 'jazzcash',
            'transaction_id': 'TXN-5001',
            'amount_paid': monthly_plan.price,
            'payment_screenshot': uploaded_gif,
        },
        follow=False,
    )

    assert response.status_code == 302
    assert response.url == reverse('core:payment_status')

    payment = PaymentProof.objects.get(user=student_user, transaction_id='TXN-5001')
    assert payment.status == 'pending'


@pytest.mark.django_db
@pytest.mark.integration
def test_payment_status_page_lists_uploaded_proofs(authenticated_client, pending_payment):
    response = authenticated_client.get(reverse('core:payment_status'))

    assert response.status_code == 200
    assert pending_payment.transaction_id.encode() in response.content


@pytest.mark.django_db
@pytest.mark.integration
def test_payment_instruction_page_loads(authenticated_client, monthly_plan):
    response = authenticated_client.get(
        reverse('core:payment', kwargs={'plan_id': monthly_plan.pk})
    )

    assert response.status_code == 200
    assert monthly_plan.name.encode() in response.content


@pytest.mark.django_db
@pytest.mark.integration
def test_staff_can_review_and_approve_payment(staff_client, pending_payment):
    review_url = reverse('staff:payment_review', kwargs={'pk': pending_payment.pk})

    get_response = staff_client.get(review_url)
    assert get_response.status_code == 200

    post_response = staff_client.post(
        review_url,
        data={
            'action': 'approve',
            'status': 'pending',
            'admin_notes': 'Verified successfully.',
        },
        follow=False,
    )

    assert post_response.status_code == 302

    pending_payment.refresh_from_db()
    pending_payment.user.userprofile.refresh_from_db()

    assert pending_payment.status == 'approved'
    assert pending_payment.reviewed_by.is_staff is True
    assert pending_payment.user.userprofile.is_premium is True


@pytest.mark.django_db
@pytest.mark.integration
def test_staff_can_reject_payment(staff_client, pending_payment):
    review_url = reverse('staff:payment_review', kwargs={'pk': pending_payment.pk})

    response = staff_client.post(
        review_url,
        data={
            'action': 'reject',
            'status': 'pending',
            'admin_notes': 'Screenshot does not match the submitted amount.',
        },
        follow=False,
    )

    assert response.status_code == 302

    pending_payment.refresh_from_db()
    assert pending_payment.status == 'rejected'
    assert pending_payment.admin_notes == 'Screenshot does not match the submitted amount.'
    assert pending_payment.reviewed_by.is_staff is True


@pytest.mark.django_db
@pytest.mark.integration
def test_staff_can_keep_payment_pending(staff_client, pending_payment):
    review_url = reverse('staff:payment_review', kwargs={'pk': pending_payment.pk})

    response = staff_client.post(
        review_url,
        data={
            'action': 'pending',
            'status': 'pending',
            'admin_notes': 'Need a clearer proof before final review.',
        },
        follow=False,
    )

    assert response.status_code == 302

    pending_payment.refresh_from_db()
    assert pending_payment.status == 'pending'
    assert pending_payment.admin_notes == 'Need a clearer proof before final review.'
    assert pending_payment.reviewed_by.is_staff is True
    assert pending_payment.reviewed_at is not None


@pytest.mark.django_db
@pytest.mark.integration
def test_staff_payment_history_lists_reviewed_payments(staff_client, pending_payment):
    pending_payment.approve_payment(pending_payment.user)

    response = staff_client.get(reverse('staff:payment_history'))

    assert response.status_code == 200
    assert pending_payment.transaction_id.encode() in response.content
