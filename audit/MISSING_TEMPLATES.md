# MISSING_TEMPLATES.md
## MedPrep — Missing Templates Report

Templates referenced by views but **not found** on disk.

---

## Core App — 11 Missing Templates

### Auth

| Template Path | View | URL |
|--------------|------|-----|
| `core/auth/profile_edit.html` | `ProfileEditView` | `/profile/edit/` |

### Quiz

| Template Path | View | URL |
|--------------|------|-----|
| `core/quiz/start_quiz.html` | `StartQuizView` | `/quiz/topic/<topic_id>/` |

### Resources

| Template Path | View | URL |
|--------------|------|-----|
| `core/resources/notes_list.html` | `NotesListView` | `/resources/notes/` |
| `core/resources/note_detail.html` | `NoteDetailView` | `/resources/notes/<pk>/` |
| `core/resources/flashcards_list.html` | `FlashcardsListView` | `/resources/flashcards/` |
| `core/resources/flashcard_study.html` | `FlashcardStudyView` | `/resources/flashcards/<topic_id>/` |
| `core/resources/videos_list.html` | `VideosListView` | `/resources/videos/` |
| `core/resources/video_detail.html` | `VideoDetailView` | `/resources/videos/<pk>/` |

### Subscription / Payment

| Template Path | View | URL |
|--------------|------|-----|
| `core/subscription/payment.html` | `PaymentView` | `/subscription/payment/<plan_id>/` |
| `core/subscription/payment_proof_upload.html` | `PaymentProofUploadView` | `/subscription/payment/proof/` |
| `core/subscription/payment_status.html` | `PaymentStatusView` | `/subscription/payment/status/` |

---

## Staff App — 4 Missing Templates

### Payments

| Template Path | View | URL |
|--------------|------|-----|
| `staff/payments/payment_review.html` | `PaymentReviewView` | `/staff/payments/<pk>/review/` |
| `staff/payments/payment_history.html` | `PaymentHistoryView` | `/staff/payments/history/` |

### Support (Stubbed)

| Template Path | View | URL |
|--------------|------|-----|
| `staff/support/inbox.html` | `SupportInboxView` | `/staff/support/` |
| `staff/support/message_detail.html` | `SupportMessageView` | `/staff/support/<pk>/` |

---

## Django Built-in Password Reset — 2 Missing Custom Overrides

Django's built-in auth views at `/accounts/` require these templates which are NOT present
(Django uses its own defaults if `django.contrib.admin` is installed, but custom styling will be missing):

| Template Path | View |
|--------------|------|
| `registration/password_reset_form.html` | PasswordResetView |
| `registration/password_reset_done.html` | PasswordResetDoneView |

**Note:** `registration/password_reset_confirm.html` and `registration/password_reset_complete.html` **do exist** as custom templates.

---

## Redundant / Stale Templates (Not Missing, But Duplicated)

| Template | Issue |
|----------|-------|
| `core/login.html` | Duplicate of `core/auth/login.html`; no view points to it |
| `core/signup.html` | Duplicate of `core/auth/register.html`; no view points to it |
| `staff/subjects/subject_list_new.html` | Appears to be a revision artifact; verify if still referenced |
| `staff/topics/topic_list_new.html` | Appears to be a revision artifact; verify if still referenced |

---

## Summary

| Category | Count |
|----------|-------|
| Core missing templates | 11 |
| Staff missing templates | 4 |
| Django built-in missing overrides | 2 |
| **Total broken template paths** | **17** |
| Stale/unused templates | 4 |
