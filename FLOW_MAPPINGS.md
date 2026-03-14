# MedPrep Integration Flow Mappings

## Public Flows (Student/General Users)

### 1. Authentication Flow

| Feature | Route | View Class | Template | Form | Models | GET Behavior | POST Behavior | Success Redirect | Failure | Tests |
|---------|-------|-----------|----------|------|--------|--------------|--------------|-----------------|---------|-------|
| **Login** | `/login/` | `CustomLoginView` | `core/auth/login.html` | `CustomAuthenticationForm` | User, UserProfile | Show login form | Authenticate, create profile | `core:dashboard` | Error message | ✅ `test_auth_and_profile.py` |
| **Signup** | `/signup/` | `RegisterView` | `core/auth/register.html` | `UserRegistrationForm` | User, UserProfile | Show registration form | Create user, auto-login | `core:dashboard` | Form errors | ✅ `test_auth_and_profile.py` |
| **Logout** | `/logout/` | `CustomLogoutView` | `core/auth/logout.html` | None | User | Show confirmation | Clear session | `core:login` | None | ✅ `test_auth_and_profile.py` |
| **Profile** | `/profile/` | `ProfileView` | `core/auth/profile.html` | None | UserProfile, QuizSession | Display stats, quiz history | N/A | N/A | N/A | ✅ `test_auth_and_profile.py` |
| **Profile Edit** | `/profile/edit/` | `ProfileEditView` | `core/auth/profile_edit.html` | `UserProfileForm` | UserProfile | Show edit form | Update profile | `core:profile` | Form errors | ✅ `test_auth_and_profile.py` |

### 2. Dashboard & Home

| Feature | Route | View Class | Template | Form | Models | Context Data | Tests |
|---------|-------|-----------|----------|------|--------|--------------|-------|
| **Home** | `/` | `HomeView` | `core/home.html` | None | Subject, Question, UserProfile | total_subjects, total_questions, featured_subjects | ✅ Smoke tests |
| **Dashboard** | `/dashboard/` | `DashboardView` | `core/dashboard.html` | None | QuizSession, Subject | recent_quizzes, avg_score, subjects_progress | ✅ Smoke tests |
| **Leaderboard** | `/leaderboard/` | `LeaderboardView` | `core/leaderboard.html` | None | UserProfile, QuizSession | top_users (50), weekly_leaders (20) | ✅ Smoke tests |

### 3. Question Bank Flow

| Feature | Route | View Class | Template | Models | Filters | Auth | Tests |
|---------|-------|-----------|----------|--------|---------|------|-------|
| **Question Bank** | `/questions/` | `QuestionBankView` | `core/question_bank.html` | Subject, Topic, Question | subject, topic, difficulty, year | No | ✅ `test_question_bank_flow.py` |
| **Subject Detail** | `/subjects/<id>/` | `SubjectDetailView` | `core/subject_detail.html` | Subject, Topic | N/A | No | ✅ Included |
| **Topic Detail** | `/topics/<id>/` | `TopicDetailView` | `core/topic_detail.html` | Topic, Question, Note, Flashcard | Premium content | No | ✅ Included |

### 4. Quiz Flow ⚠️ **PARTIAL - Missing Question View**

| Feature | Route | View Class | Template | Form | Models | Status | Tests |
|---------|-------|-----------|----------|------|--------|--------|-------|
| **Quiz List** | `/quiz/` | `QuizListView` | `core/quiz/quiz_list.html` | `QuizSettingsForm` | QuizSession, Topic | ✅ WORKING | ✅ `test_quiz_flow.py` |
| **Start Quiz** | `/quiz/topic/<id>/` | `StartQuizView` | `core/quiz/start_quiz.html` | None | Topic, Question | ✅ WORKING | ✅ `test_quiz_flow.py` |
| **Quiz Session** | `/quiz/session/<id>/` | `QuizSessionView` | `core/quiz/quiz_session.html` | None | QuizSession | ✅ WORKING | ✅ `test_quiz_flow.py` |
| **Quiz Question** | `/quiz/session/<id>/question/<qid>/` | `QuizQuestionView` | `?` | None | Question, UserAnswer | ❌ BROKEN - View not implemented | ❌ No test |
| **Submit Quiz** | `/quiz/session/<id>/submit/` | `SubmitQuizView` | `core/quiz/take_quiz.html` | None | QuizSession, UserAnswer | ✅ WORKING | ✅ `test_quiz_flow.py` |
| **Quiz Result** | `/quiz/result/<id>/` | `QuizResultView` | `core/quiz/quiz_result.html` | None | QuizSession, UserAnswer | ✅ WORKING | ✅ `test_quiz_flow.py` |
| **Results History** | `/results/` | `QuizResultsListView` | `core/quiz/results.html` | None | QuizSession | ✅ WORKING | ✅ `test_quiz_flow.py` |

### 5. Resources Flow

| Feature | Route | View Class | Template | Models | Filters | Auth | Tests |
|---------|-------|-----------|----------|--------|---------|------|-------|
| **Resources Hub** | `/resources/` | `ResourcesView` | `core/resources/resources.html` | N/A | N/A | No | ✅ `test_resource_flow.py` |
| **Notes List** | `/resources/notes/` | `NotesListView` | `core/resources/notes_list.html` | Note | is_active, premium | No | ✅ `test_resource_flow.py` |
| **Note Detail** | `/resources/notes/<id>/` | `NoteDetailView` | `core/resources/note_detail.html` | Note | N/A | No | ✅ `test_resource_flow.py` |
| **Videos List** | `/resources/videos/` | `VideosListView` | `core/resources/videos_list.html` | VideoResource | is_active, premium | No | ✅ `test_resource_flow.py` |
| **Video Detail** | `/resources/videos/<id>/` | `VideoDetailView` | `core/resources/video_detail.html` | VideoResource | N/A | No | ✅ `test_resource_flow.py` |
| **Flashcards List** | `/resources/flashcards/` | `FlashcardsListView` | `core/resources/flashcards_list.html` | Flashcard | By Topic, premium | No | ✅ `test_resource_flow.py` |
| **Flashcard Study** | `/resources/flashcards/<topic_id>/` | `FlashcardStudyView` | `core/resources/flashcard_study.html` | Flashcard, UserProgress | N/A | Optional | ✅ `test_resource_flow.py` |

### 6. Subscription & Payment Flow

| Feature | Route | View Class | Template | Form | Models | GET Behavior | POST Behavior | Success Redirect | Tests |
|---------|-------|-----------|----------|------|--------|--------------|--------------|-----------------|-------|
| **Plans** | `/subscribe/` | `SubscriptionView` | `core/subscription/subscription.html` | None | SubscriptionPlan | Show active plans | N/A | N/A | ✅ `test_payment_flow.py` |
| **Payment** | `/subscription/payment/<id>/` | `PaymentView` | `core/subscription/payment.html` | `PaymentProofForm` | SubscriptionPlan, PaymentProof | Show payment form, check duplicates | N/A | N/A | ✅ `test_payment_flow.py` |
| **Upload Proof** | `/subscription/payment/proof/` | `PaymentProofUploadView` | `core/subscription/payment_proof_upload.html` | `PaymentProofForm` | PaymentProof | Show form | Save proof, validate duplicate | `core:payment_status` | Duplicate warning | ✅ `test_payment_flow.py` |
| **Payment Status** | `/subscription/payment/status/` | `PaymentStatusView` | `core/subscription/payment_status.html` | None | PaymentProof | Show payment history + stats | N/A | N/A | ✅ `test_payment_flow.py` |

---

## Staff Flows (73 routes total)

### 1. Staff Authentication

| Feature | Route | View Class | Template | Auth | Tests |
|---------|-------|-----------|----------|------|-------|
| **Staff Login** | `/staff/login/` | `AdminLoginView` | `staff/auth/login.html` | is_staff=True | ✅ `test_staff_user_flow.py` |
| **Staff Logout** | `/staff/logout/` | `AdminLogoutView` | `staff/auth/logout.html` | is_staff=True | ✅ `test_staff_user_flow.py` |

### 2. User Management (6 routes)

| Feature | Route | View Class | Template | Form | GET | POST | Redirect | Bulk | Tests |
|---------|-------|-----------|----------|------|-----|------|----------|------|-------|
| **List** | `/staff/users/` | `UserListView` | `staff/users/user_list.html` | `UserSearchForm` | Paginated (20pp), filters | N/A | N/A | N/A | ✅ `test_staff_user_flow.py` |
| **Create** | `/staff/users/create/` | `UserCreateView` | `staff/users/user_add.html` | `UserCreateForm` | Form | Create user | `/staff/users/` | N/A | ✅ `test_staff_user_flow.py` |
| **Detail** | `/staff/users/<id>/` | `UserDetailView` | `staff/users/user_detail.html` | None | View profile + stats | N/A | N/A | N/A | ✅ `test_staff_user_flow.py` |
| **Edit** | `/staff/users/<id>/edit/` | `UserEditView` | `staff/users/user_edit.html` | `UserEditForm` | Edit form | Update user | `/staff/users/` | N/A | ✅ `test_staff_user_flow.py` |
| **Bulk Upload** | `/staff/users/bulk-upload/` | `BulkUserUploadView` | `staff/users/bulk_upload.html` | `BulkUserUploadForm` | Form | Parse CSV, create users | `/staff/users/` | ✅ CSV | ✅ `test_staff_user_flow.py` |
| **Export** | `/staff/users/export/` | `UserExportView` | N/A (download) | None | N/A | Download CSV | N/A | ✅ CSV download | ✅ `test_staff_user_flow.py` |

### 3. Question Management (8 routes)

| Feature | Route | View Class | Template | Form | Search | Filters | Pagination | Tests |
|---------|-------|-----------|----------|------|--------|---------|------------|-------|
| **List** | `/staff/questions/` | `QuestionListView` | `staff/questions/question_list.html` | None | Yes (text, tags) | subject, topic, difficulty, status, premium | 20pp | ✅ `test_staff_question_and_topic_flows.py` |
| **Create** | `/staff/questions/create/` | `QuestionCreateView` | `staff/questions/question_form.html` | `QuestionForm` + `OptionFormSet` | N/A | N/A | N/A | ✅ Test |
| **Edit** | `/staff/questions/<id>/edit/` | `QuestionEditView` | `staff/questions/question_edit.html` | `QuestionForm` + `OptionFormSet` | N/A | N/A | N/A | ✅ Test |
| **Delete** | `/staff/questions/<id>/delete/` | `QuestionDeleteView` | `staff/questions/question_confirm_delete.html` | None | N/A | N/A | N/A | ✅ Test |
| **Bulk Upload** | `/staff/questions/bulk-upload/` | `BulkQuestionUploadView` | `staff/questions/bulk_upload.html` | `BulkQuestionUploadForm` | N/A | N/A | N/A | ✅ CSV support |
| **Bulk Actions** | `/staff/questions/bulk-action/` | `QuestionBulkActionView` | N/A (AJAX) | None | N/A | N/A | N/A | ✅ AJAX |
| **Export** | `/staff/questions/export/` | `QuestionExportView` | N/A (download) | None | N/A | N/A | N/A | ✅ CSV download |
| **Toggle Status** | `/staff/questions/toggle-status/` | `QuestionToggleStatusView` | N/A (AJAX) | None | N/A | N/A | N/A | ✅ AJAX |

### 4. Subject Management (7 routes)

| Feature | Route | View Class | Type | Form | Endpoint | Tests |
|---------|-------|-----------|------|------|----------|-------|
| **List** | `/staff/subjects/` | `SubjectListView` | Standard | None | HTML page | ✅ `test_staff_subject_crud.py` |
| **Create** | `/staff/subjects/create/` | `SubjectCreateView` | Standard | ModelForm | HTML form | ✅ Test |
| **Edit** | `/staff/subjects/<id>/edit/` | `SubjectEditView` | Standard | ModelForm | HTML form | ✅ Test |
| **AJAX Create** | `/staff/subjects/ajax/add/` | `SubjectCreateAjaxView` | AJAX | JSON | POST JSON, response JSON | ✅ AJAX test |
| **AJAX Edit** | `/staff/subjects/ajax/<id>/edit/` | `SubjectEditAjaxView` | AJAX | JSON | POST JSON, response JSON | ✅ AJAX test |
| **Toggle Status** | `/staff/subjects/toggle-status/` | `SubjectToggleStatusView` | AJAX | JSON | POST toggle, response JSON | ✅ AJAX test |
| **Get Topics** | `/staff/subjects/<id>/topics/` | `GetSubjectTopicsView` | AJAX | None | GET, returns topic list JSON | ✅ AJAX test |

### 5. Topic Management (10 routes) - ⚠️ **Duplicate Views**

| Feature | Route | View Class | Type | Implementation | Tests |
|---------|-------|-----------|------|----------------|-------|
| **List** | `/staff/topics/` | `TopicListEnhancedView` | Standard | HTML list + pagination | ✅ `test_staff_question_and_topic_flows.py` |
| **Create** | `/staff/topics/create/` | `TopicCreateView` | Standard | HTML form | ✅ Test |
| **Edit** | `/staff/topics/<id>/edit/` | `TopicEditView` | Standard | HTML form | ✅ Test |
| **Delete** | `/staff/topics/<id>/delete/` | `TopicDeleteView` | AJAX | JSON response | ✅ AJAX test |
| **AJAX Create** | `/staff/topics/ajax/add/` | `TopicCreateAjaxEnhancedView` | AJAX | JSON POST | ✅ AJAX test |
| **AJAX Edit** | `/staff/topics/ajax/<id>/edit/` | `TopicEditAjaxEnhancedView` | AJAX | JSON POST | ✅ AJAX test |
| **Toggle Status** | `/staff/topics/toggle-status/` | `TopicToggleStatusView` | AJAX | JSON toggle | ✅ AJAX test |
| **Bulk Upload** | `/staff/topics/bulk-upload/` | `TopicBulkUploadView` | Standard | CSV upload form | ✅ CSV support |
| **Template Download** | `/staff/topics/bulk-template/` | `TopicBulkUploadTemplateView` | Download | CSV file download | ✅ Template test |

### 6. Tag & Subtag Management (14 routes) - ⚠️ **Duplicate ajax/create Routes**

| Feature | Route | View Class | Type | Response | Tests |
|---------|-------|-----------|------|----------|-------|
| **List** | `/staff/tags/` | `TagListView` | Standard | HTML list | ✅ Test |
| **Create** | `/staff/tags/create/` | `TagCreateView` | Standard | HTML form | ✅ Test |
| **Edit** | `/staff/tags/<id>/edit/` | `TagEditView` | Standard | HTML form | ✅ Test |
| **Delete** | `/staff/tags/<id>/delete/` | `TagDeleteView` | Standard | HTML delete confirm | ✅ Test |
| **AJAX Get** | `/staff/tags/ajax/<id>/` | `TagGetAjaxView` | AJAX | JSON tag data | ✅ AJAX test |
| **AJAX Create** | `/staff/tags/ajax/create/` | `TagCreateAjaxView` | AJAX | JSON (tag_id + success) | ⚠️ Duplicate: `tag_create_ajax` AND `ajax_tag_create` |
| **AJAX Update** | `/staff/tags/ajax/<id>/update/` | `TagUpdateAjaxView` | AJAX | JSON success | ✅ AJAX test |
| **Toggle Status** | `/staff/tags/ajax/toggle-status/` | `TagToggleStatusView` | AJAX | JSON toggle | ✅ AJAX test |
| **Bulk Actions** | `/staff/tags/ajax/bulk-action/` | `TagBulkActionView` | AJAX | JSON result | ✅ AJAX test |
| **Get Subtags** | `/staff/tags/<id>/subtags/` | `GetTagSubtagsView` | AJAX | JSON subtag array | ✅ AJAX test |
| **Subtag Create** | `/staff/subtags/ajax/add/` | `SubtagCreateAjaxView` | AJAX | JSON (subtag_id + success) | ✅ AJAX test |
| **Subtag Update** | `/staff/subtags/ajax/<id>/update/` | `SubtagUpdateAjaxView` | AJAX | JSON success | ✅ AJAX test |
| **Subtag Toggle** | `/staff/subtags/ajax/toggle-status/` | `SubtagToggleStatusView` | AJAX | JSON toggle | ✅ AJAX test |
| **Subtag Delete** | `/staff/subtags/ajax/delete/` | `SubtagDeleteView` | AJAX | JSON delete result | ✅ AJAX test |

### 7. Quiz Management (2 routes)

| Feature | Route | View Class | Template | Pagination | Tests |
|---------|-------|-----------|----------|-----------|-------|
| **Quiz Attempts** | `/staff/quizzes/` | `QuizAttemptListView` | `staff/quizzes/quiz_list.html` | Yes | ✅ Test |
| **Leaderboard** | `/staff/leaderboard/` | `LeaderboardView` | `staff/quizzes/leaderboard.html` | Yes | ✅ Test |

### 8. Resource Management (9 routes)

| Feature | Route | View Class | Template | Form | CRUD | Tests |
|---------|-------|-----------|----------|------|------|-------|
| **Resources Hub** | `/staff/resources/` | `ResourceListView` | `staff/resources/resource_list.html` | None | List | ✅ Test |
| **Notes List** | `/staff/notes/` | `NoteListView` | `staff/resources/note_list.html` | None | List | ✅ Test |
| **Note Create** | `/staff/notes/create/` | `NoteCreateView` | `staff/resources/note_form.html` | ModelForm | Create | ✅ Test |
| **Note Edit** | `/staff/notes/<id>/edit/` | `NoteEditView` | `staff/resources/note_form.html` | ModelForm | Update | ✅ Test |
| **Videos List** | `/staff/videos/` | `VideoListView` | `staff/resources/video_list.html` | None | List | ✅ Test |
| **Video Create** | `/staff/videos/create/` | `VideoCreateView` | `staff/resources/video_form.html` | ModelForm | Create | ✅ Test |
| **Video Edit** | `/staff/videos/<id>/edit/` | `VideoEditView` | `staff/resources/video_form.html` | ModelForm | Update | ✅ Test |
| **Flashcard List** | `/staff/flashcards/` | `FlashcardListView` | `staff/resources/flashcard_list.html` | None | List | ✅ Test |
| **Flashcard Create** | `/staff/flashcards/create/` | `FlashcardCreateView` | `staff/resources/flashcard_form.html` | ModelForm | Create | ✅ Test |
| **Flashcard Edit** | `/staff/flashcards/<id>/edit/` | `FlashcardEditView` | `staff/resources/flashcard_form.html` | ModelForm | Update | ✅ Test |

### 9. Payment Management (3 routes)

| Feature | Route | View Class | Template | Filters | GET | POST | Tests |
|---------|-------|-----------|----------|---------|-----|------|-------|
| **List** | `/staff/payments/` | `PaymentListView` | `staff/payments/payment_list.html` | status, date, user | Paginated list | N/A | ✅ `test_payment_flow.py` |
| **Review** | `/staff/payments/<id>/review/` | `PaymentReviewView` | `staff/payments/payment_review.html` | N/A | Show form | Approve/reject, send email | ✅ Test |
| **History** | `/staff/payments/history/` | `PaymentHistoryView` | `staff/payments/payment_history.html` | date range, status | Stats + timeline | N/A | ✅ Test |

### 10. Support Management (2 routes) - ⚠️ **Second Route Incomplete**

| Feature | Route | View Class | Template | Implementation | Tests |
|---------|-------|-----------|----------|-----------------|-------|
| **Inbox** | `/staff/support/` | `SupportInboxView` | `staff/support/inbox.html` | ✅ List support messages | ✅ Test |
| **Message Detail** | `/staff/support/<id>/` | `SupportMessageView` | `staff/support/message_detail.html` | ❌ TemplateView without context | ❌ No test |

### 11. Settings & Logs (2 routes) - ⚠️ **Second Route Broken**

| Feature | Route | View Class | Template | Implementation | Tests |
|---------|-------|-----------|----------|-----------------|-------|
| **Settings** | `/staff/settings/` | `SettingsView` | `staff/settings/settings.html` | ✅ Template rendering | ✅ Test |
| **Activity Logs** | `/staff/logs/` | `ActivityLogsView` | `staff/settings/logs.html` | ❌ Empty view | ❌ No test |

---

## Issue Summary Table

| Issue | Severity | Location | Component | Impact | Evidence |
|-------|----------|----------|-----------|--------|----------|
| Quiz Question View Missing | 🔴 CRITICAL | `/core/urls.py:33` | Quiz submission | Flow breaks on question answer | View not in core/views/ |
| Support Message Incomplete | 🔴 CRITICAL | `/staff/urls.py:98` | Support detail | Staff can't view messages properly | TemplateView without context |
| Activity Logs Empty | 🔴 CRITICAL | `/staff/urls.py:102` | Audit trail | No action logging | Empty implementation |
| Duplicate Tag Routes | 🟡 WARNING | `/staff/urls.py:61-62` | URL routing | Confusion about which URL to use | Two names: ajax_tag_create + tag_create_ajax |
| Duplicate Topic Views | 🟡 WARNING | `/staff/urls.py:43+49` | Code quality | Maintenance burden | TopicListView vs TopicListEnhancedView |

---

## Quick Navigation Reference

### By Feature
- [Auth Flows](#1-authentication-flow)
- [Dashboard](#2-dashboard--home)
- [Questions](#question-bank-flow)
- [Quiz](#4-quiz-flow)
- [Resources](#5-resources-flow)
- [Payments](#6-subscription--payment-flow)
- [Staff Users](#2-user-management-6-routes)
- [Staff Questions](#3-question-management-8-routes)
- [Staff Subjects](#4-subject-management-7-routes)
- [Staff Topics](#5-topic-management-10-routes)
- [Staff Tags](#6-tag--subtag-management-14-routes)
- [Staff Payments](#9-payment-management-3-routes)

### By Status
- ✅ **Fully Working** - Most flows (40+)
- ⚠️ **Partial** - Quiz question view, Support, Logs
- ❌ **Broken** - 3 critical issues

### By Test Coverage
- ✅ **Tested** - 12 test suites covering main flows
- ❌ **Untested** - Support detail, Logs, Quiz question

