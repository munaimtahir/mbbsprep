# PROJECT_STRUCTURE.md
## MedPrep — Full Project Structure Audit

---

## Apps

| App | Purpose |
|-----|---------|
| `core` | Public-facing student app (auth, quiz, resources, subscriptions) |
| `staff` | Custom CMS backoffice (admin panel for staff users) |
| `medprep` | Django project package (settings, root URLs, wsgi/asgi) |

---

## Models

### core (6 model files under `core/models/`)

| File | Models |
|------|--------|
| `user_models.py` | `UserProfile` |
| `academic_models.py` | `Subject`, `Topic`, `Question`, `Option` |
| `quiz_models.py` | `QuizSession`, `UserAnswer` |
| `resource_models.py` | `Note`, `Flashcard`, `VideoResource`, `UserProgress` |
| `subscription_models.py` | `SubscriptionPlan`, `PaymentProof` |
| `tag_models.py` | `Tag`, `Subtag` |

*(Also a stale `core/models.py` root file — `core/models/__init__.py` is the active package.)*

---

## Views

### core (`core/views/`)

| File | View Classes |
|------|-------------|
| `main_views.py` | `HomeView`, `DashboardView`, `LeaderboardView`, `QuestionBankView`, `SubjectDetailView`, `TopicDetailView` |
| `auth_views.py` | `CustomLoginView`, `CustomLogoutView`, `RegisterView`, `ProfileView`, `ProfileEditView` |
| `quiz_views.py` | `QuizListView`, `StartQuizView`, `QuizSessionView`, `QuizQuestionView`, `SubmitQuizView`, `QuizResultView` |
| `resource_views.py` | `ResourcesView`, `NotesListView`, `NoteDetailView`, `FlashcardsListView`, `FlashcardStudyView`, `VideosListView`, `VideoDetailView` |
| `payment_views.py` | `SubscriptionView`, `PaymentView`, `PaymentProofUploadView`, `PaymentStatusView` |
| `static_views.py` | `AboutView`, `ContactView`, `FAQView`, `TermsView`, `PrivacyView` |

### staff (`staff/views/`)

| File | View Classes |
|------|-------------|
| `auth_views.py` | `AdminLoginView`, `AdminLogoutView` |
| `dashboard_views.py` | `DashboardView` |
| `user_views.py` | `UserListView`, `UserDetailView`, `UserEditView`, `UserCreateView`, `BulkUserUploadView`, `UserExportView`, `StaffRequiredMixin` |
| `question_views.py` | `QuestionListView`, `QuestionCreateView`, `QuestionEditView`, `QuestionDeleteView`, `BulkQuestionUploadView`, `QuestionBulkActionView`, `QuestionExportView`, `QuestionToggleStatusView`, `GetTopicsAjaxView` |
| `subject_views.py` | `SubjectListView`, `SubjectCreateView`, `SubjectEditView`, `SubjectCreateAjaxView`, `SubjectEditAjaxView`, `SubjectToggleStatusView`, `GetSubjectTopicsView`, `TopicListView`, `TopicCreateView`, `TopicEditView`, `TopicListEnhancedView`, `TopicToggleStatusView`, `TopicDeleteView`, `TopicCreateAjaxEnhancedView`, `TopicEditAjaxEnhancedView`, `TopicCreateAjaxView`, `TopicEditAjaxView` |
| `topic_bulk_views.py` | `TopicBulkUploadView`, `TopicBulkUploadTemplateView` |
| `tag_views.py` | `TagListView`, `TagCreateView`, `TagEditView`, `TagDeleteView` |
| `tag_ajax_views.py` | `TagGetAjaxView`, `TagCreateAjaxView`, `TagUpdateAjaxView`, `TagToggleStatusView`, `TagBulkActionView`, `GetTagSubtagsView`, `SubtagCreateAjaxView`, `SubtagUpdateAjaxView`, `SubtagToggleStatusView`, `SubtagDeleteView` |
| `quiz_views.py` | `QuizAttemptListView`, `LeaderboardView` |
| `resource_views.py` | `ResourceListView`, `NoteListView`, `NoteCreateView`, `NoteEditView`, `VideoListView`, `VideoCreateView`, `VideoEditView`, `FlashcardListView`, `FlashcardCreateView`, `FlashcardEditView` |
| `payment_views.py` | `PaymentListView`, `PaymentReviewView`, `PaymentHistoryView` |
| `support_views.py` | `SupportInboxView`, `SupportMessageView` |
| `settings_views.py` | `SettingsView`, `ActivityLogsView` |

---

## Forms

### core (`core/forms/`)

| File | Form Classes |
|------|-------------|
| `user_forms.py` | `CustomAuthenticationForm`, `UserRegistrationForm`, `UserProfileForm`, `QuizSettingsForm`, `PaymentProofForm`, `ContactForm` |
| `quiz_forms.py` | *(QuizSettingsForm is in user_forms.py; this file may be duplicate/empty — verify)* |
| `payment_forms.py` | *(PaymentProofForm is in user_forms.py; this file may be duplicate/empty — verify)* |

### staff (`staff/forms/`)

| File | Form Classes |
|------|-------------|
| `auth_forms.py` | Staff auth forms |
| `question_forms.py` | `QuestionForm`, `OptionForm`, `BulkQuestionUploadForm`, `QuestionSearchForm` |
| `payment_forms.py` | `PaymentReviewForm`, `PaymentSearchForm`, `SubscriptionPlanForm` |
| `resource_forms.py` | `NoteForm`, `VideoResourceForm`, `FlashcardForm`, `ResourceSearchForm` |
| `tag_forms.py` | Tag/Subtag forms |
| `topic_bulk_forms.py` | Topic bulk upload forms |
| `user_forms.py` | `UserSearchForm`, `UserCreateForm`, `UserEditForm`, `BulkUserUploadForm` |

**Note:** `staff/forms.py` (root level) is a **stale duplicate** artifact — `staff/forms/` package is the active source.

---

## Templates

### Existing Templates

```
templates/
├── base.html
├── core/
│   ├── auth/
│   │   ├── login.html        ✓
│   │   ├── logout.html       ✓
│   │   ├── profile.html      ✓
│   │   └── register.html     ✓
│   ├── quiz/
│   │   ├── quiz_list.html    ✓
│   │   ├── quiz_result.html  ✓
│   │   ├── quiz_session.html ✓
│   │   ├── results.html      ✓
│   │   └── take_quiz.html    ✓
│   ├── resources/
│   │   └── resources.html    ✓
│   ├── static/
│   │   ├── about.html        ✓
│   │   ├── contact.html      ✓
│   │   ├── faq.html          ✓
│   │   ├── privacy.html      ✓
│   │   └── terms.html        ✓
│   ├── subscription/
│   │   ├── plans.html        ✓
│   │   ├── subscribe.html    ✓
│   │   └── subscription.html ✓
│   ├── dashboard.html        ✓
│   ├── home.html             ✓
│   ├── leaderboard.html      ✓
│   ├── login.html            ✓  (stale duplicate of core/auth/login.html)
│   ├── question_bank.html    ✓
│   ├── signup.html           ✓  (stale duplicate of core/auth/register.html)
│   ├── subject_detail.html   ✓
│   └── topic_detail.html     ✓
├── emails/
│   ├── welcome_user.html     ✓
│   └── welcome_user.txt      ✓
├── registration/
│   ├── password_reset_complete.html   ✓
│   ├── password_reset_confirm.html    ✓
│   ├── password_reset_email.html      ✓
│   └── password_reset_subject.txt     ✓
└── staff/
    ├── base_admin.html       ✓
    ├── auth/
    │   ├── login.html        ✓
    │   └── logout.html       ✓
    ├── dashboard.html        ✓
    ├── payments/
    │   └── payment_list.html ✓
    ├── questions/
    │   ├── bulk_upload.html  ✓
    │   ├── question_add.html ✓
    │   ├── question_confirm_delete.html ✓
    │   ├── question_edit.html ✓
    │   ├── question_form.html ✓
    │   └── question_list.html ✓
    ├── quizzes/
    │   ├── leaderboard.html  ✓
    │   └── quiz_list.html    ✓
    ├── resources/
    │   ├── flashcard_form.html  ✓
    │   ├── flashcard_list.html  ✓
    │   ├── note_form.html       ✓
    │   ├── note_list.html       ✓
    │   ├── resource_list.html   ✓
    │   ├── video_form.html      ✓
    │   └── video_list.html      ✓
    ├── settings/
    │   ├── logs.html         ✓
    │   └── settings.html     ✓
    ├── subjects/
    │   ├── subject_form.html ✓
    │   ├── subject_list.html ✓
    │   └── subject_list_new.html ✓
    ├── tags/
    │   ├── tag_form.html     ✓
    │   └── tag_list.html     ✓
    ├── topics/
    │   ├── bulk_upload.html  ✓
    │   ├── topic_form.html   ✓
    │   ├── topic_list.html   ✓
    │   └── topic_list_new.html ✓
    └── users/
        ├── bulk_upload.html  ✓
        ├── user_add.html     ✓
        ├── user_detail.html  ✓
        ├── user_edit.html    ✓
        └── user_list.html    ✓
```

---

## URL Files

| File | Namespace | Prefix |
|------|-----------|--------|
| `medprep/urls.py` | root | `/` |
| `core/urls.py` | `core` | `/` |
| `staff/urls.py` | `staff` | `/staff/` |

Django's built-in `django.contrib.auth.urls` is also mounted at `/accounts/`.

---

## Management Commands

| App | Command | Purpose |
|-----|---------|---------|
| `core` | `create_sample_data` | Create sample subjects/topics/questions |
| `core` | `create_test_users` | Create test user accounts |
| `core` | `expire_subscriptions` | Expire overdue subscriptions |
| `core` | `import_questions` | Bulk import questions (CSV/JSON) |

---

## Utility Modules

| File | Purpose |
|------|---------|
| `core/utils/payment_check.py` | Payment and subscription validation helpers |
| `core/utils/ranking.py` | Leaderboard ranking logic |
| `core/utils/scoring.py` | Quiz scoring calculations |
| `core/context_processors.py` | Global template context processors |
| `core/signals.py` | Django signal handlers |

---

## Scripts (Development/Debug — Not Production Code)

Located in `scripts/` and `tests/` — approximately 80+ one-off debug/test scripts covering:
- bulk upload, MCQ editing, user profile, CSS/JS separation, template checking, etc.
- None are standard Django `TestCase`-based tests; all are standalone HTTP request scripts.

---

## Tests

`core/tests.py` — **exists but empty** (no test cases written).  
All testing has been done via standalone scripts in `tests/` and `scripts/` directories.
