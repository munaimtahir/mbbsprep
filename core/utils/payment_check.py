"""
Payment verification utilities for subscription management
"""
import os
from datetime import timedelta
from django.utils import timezone
from core.models import PaymentProof, UserProfile


def verify_payment_proof(payment_proof):
    """
    Verify payment proof submission (basic validation)
    """
    if not payment_proof.payment_screenshot:
        return False, "No payment proof image provided"
    
    # Check file size (max 5MB)
    if payment_proof.payment_screenshot.size > 5 * 1024 * 1024:
        return False, "File size too large (max 5MB)"
    
    # Check file extension
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
    file_ext = os.path.splitext(payment_proof.payment_screenshot.name)[1].lower()
    if file_ext not in allowed_extensions:
        return False, "Invalid file format. Only JPG, PNG, and PDF files are allowed"
    
    return True, "Payment proof submitted successfully"


def process_payment_verification(payment_proof, admin_user):
    """
    Process payment verification by admin
    """
    if payment_proof.status == 'approved':
        payment_proof.approve_payment(admin_user)
        expiry_date = payment_proof.user.userprofile.premium_expires_at
        return True, f"Premium subscription activated until {expiry_date.strftime('%Y-%m-%d')}"

    if payment_proof.status == 'rejected':
        return False, "Payment proof rejected. Please contact support or resubmit with correct information."
    
    return None, "Payment verification pending"


def check_subscription_status(user):
    """
    Check if user's subscription is active
    """
    try:
        profile = user.userprofile
        if profile.is_premium_active:
            days_remaining = (profile.premium_expires_at - timezone.now()).days
            latest_approved_payment = PaymentProof.objects.filter(
                user=user,
                status='approved',
            ).select_related('subscription_plan').order_by('-reviewed_at', '-submitted_at').first()
            return {
                'is_active': True,
                'expires_at': profile.premium_expires_at,
                'days_remaining': max(0, days_remaining),
                'plan': latest_approved_payment.subscription_plan if latest_approved_payment else None,
            }
        return {
            'is_active': False,
            'expires_at': None,
            'days_remaining': 0,
            'plan': None,
        }
    except UserProfile.DoesNotExist:
        return {
            'is_active': False,
            'expires_at': None,
            'days_remaining': 0,
            'plan': None,
        }


def get_pending_payments():
    """
    Get all pending payment proofs for admin review
    """
    return PaymentProof.objects.filter(
        status='pending'
    ).order_by('-submitted_at')


def auto_expire_subscriptions():
    """
    Utility function to automatically expire subscriptions
    Can be run as a cron job or management command
    """
    expired_profiles = UserProfile.objects.filter(
        premium_expires_at__lt=timezone.now(),
        is_premium=True,
    )
    
    count = 0
    for profile in expired_profiles:
        profile.is_premium = False
        profile.premium_expires_at = None
        profile.save(update_fields=['is_premium', 'premium_expires_at', 'updated_at'])
        count += 1
    
    return count  # Number of subscriptions expired
