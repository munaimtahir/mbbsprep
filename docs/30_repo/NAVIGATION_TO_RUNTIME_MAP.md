# Navigation to Runtime Map

Date: 2026-03-14

This map traces visible navigation items/buttons to actual runtime handlers and current integration state.

## Public Navigation

| Appears in | Nav item/button | Route target | View handler | Runtime destination status | Permission handling |
| --- | --- | --- | --- | --- | --- |
| `templates/base.html` navbar | Home | `core:home` | `HomeView` | real (`WORKING_MINIMAL`) | public |
| `templates/base.html` navbar (anon) | Login | `core:login` | `CustomLoginView` | real (`FULLY_INTEGRATED`) | public |
| `templates/base.html` navbar (anon) | Register | `core:signup` | `RegisterView` | real (`FULLY_INTEGRATED`) | public |
| `templates/base.html` navbar (auth) | Dashboard | `core:dashboard` | `DashboardView` | real (`WORKING_MINIMAL`) | `LoginRequiredMixin` |
| `templates/base.html` navbar (auth) | Question Bank | `core:question_bank` | `QuestionBankView` | real (`WORKING_MINIMAL`) | auth-gated via nav visibility |
| `templates/base.html` navbar (auth) | Study Resources | `core:resources` | `ResourcesView` | real (`WORKING_MINIMAL`) | auth-gated via nav visibility |
| `templates/base.html` navbar (auth) | Notes | `core:notes_list` | `NotesListView` | real (`WORKING_MINIMAL`) | public route; auth via nav context |
| `templates/base.html` navbar (auth) | Flashcards | `core:flashcards_list` | `FlashcardsListView` | real (`WORKING_MINIMAL`) | public route; auth via nav context |
| `templates/base.html` navbar (auth) | Videos | `core:videos_list` | `VideosListView` | real (`WORKING_MINIMAL`) | public route; auth via nav context |
| `templates/base.html` navbar (auth) | Leaderboard | `core:leaderboard` | `LeaderboardView` | real (`WORKING_MINIMAL`) | public route; auth via nav context |
| `templates/base.html` navbar (auth) | Upgrade | `core:subscription` | `SubscriptionView` | real (`WORKING_MINIMAL`) | auth-aware context |
| `templates/base.html` user dropdown | Profile | `core:profile` | `ProfileView` | real (`FULLY_INTEGRATED`) | `LoginRequiredMixin` |
| `templates/base.html` user dropdown | Subscription | `core:payment_status` | `PaymentStatusView` | real (`FULLY_INTEGRATED`) | `LoginRequiredMixin` |
| `templates/base.html` user dropdown | Logout | `core:logout` | `CustomLogoutView` | real (`FULLY_INTEGRATED`) | session-based |
| `templates/base.html` footer | About | `core:about` | `AboutView` | real (`WORKING_MINIMAL`) | public |
| `templates/base.html` footer | Contact | `core:contact` | `ContactView` | real (`WORKING_MINIMAL`) | public |
| `templates/base.html` footer | FAQ | `core:faq` | `FAQView` | real (`WORKING_MINIMAL`) | public |
| `templates/base.html` footer | Terms | `core:terms` | `TermsView` | real (`WORKING_MINIMAL`) | public |
| `templates/base.html` footer | Privacy | `core:privacy` | `PrivacyView` | real (`WORKING_MINIMAL`) | public |

## Public Dashboard and Page-level CTAs

| Appears in | Nav item/button | Route target | View handler | Runtime destination status | Permission handling |
| --- | --- | --- | --- | --- | --- |
| `templates/core/dashboard.html` | Start New Quiz | `core:question_bank` | `QuestionBankView` | real (`WORKING_MINIMAL`) | authenticated page |
| `templates/core/dashboard.html` | Continue Last Quiz | `core:quiz_result` | `QuizResultView` | real (`FULLY_INTEGRATED`) | `LoginRequiredMixin` on quiz views |
| `templates/core/dashboard.html` | Browse Study Materials | `core:resources` | `ResourcesView` | real (`WORKING_MINIMAL`) | authenticated page |
| `templates/core/dashboard.html` | View Leaderboard | `core:leaderboard` | `LeaderboardView` | real (`WORKING_MINIMAL`) | authenticated page |
| `templates/core/dashboard.html` | Upgrade Plan | `core:subscription` | `SubscriptionView` | real (`WORKING_MINIMAL`) | authenticated page |
| `templates/core/resources/resources.html` | Quick tools (Practice MCQs) | `core:question_bank` | `QuestionBankView` | real (`WORKING_MINIMAL`) | inherited auth context |
| `templates/core/resources/resources.html` | Quick tools (Leaderboard) | `core:leaderboard` | `LeaderboardView` | real (`WORKING_MINIMAL`) | inherited auth context |
| `templates/core/quiz/quiz_list.html` | Topic “Start Quiz” | `core:start_quiz` | `StartQuizView` | real (`FULLY_INTEGRATED`) | `LoginRequiredMixin` |
| `templates/core/quiz/quiz_list.html` | Quick Start form submit | `core:quiz` (POST) | `QuizListView.post` | real (`FULLY_INTEGRATED`) | `LoginRequiredMixin` |

## Staff Sidebar and Topbar Navigation

| Appears in | Nav item/button | Route target | View handler | Runtime destination status | Permission handling |
| --- | --- | --- | --- | --- | --- |
| `templates/staff/base_admin.html` sidebar | Dashboard | `staff:dashboard` | `DashboardView` | real (`WORKING_MINIMAL`) | `StaffRequiredMixin` |
| `templates/staff/base_admin.html` sidebar | Users | `staff:user_list` | `UserListView` | real (`WORKING_MINIMAL`) | `StaffRequiredMixin` |
| `templates/staff/base_admin.html` sidebar | Questions | `staff:question_list` | `QuestionListView` | real (`WORKING_MINIMAL`) | `StaffRequiredMixin` |
| `templates/staff/base_admin.html` sidebar | Payments | `staff:payment_list` | `PaymentListView` | real (`FULLY_INTEGRATED`) | `StaffRequiredMixin` |
| `templates/staff/base_admin.html` sidebar | Subjects | `staff:subject_list` | `SubjectListView` | real (`WORKING_MINIMAL`) | `StaffRequiredMixin` |
| `templates/staff/base_admin.html` sidebar | Tags | `staff:tag_list` | `TagListView` | real (`WORKING_MINIMAL`) | `StaffRequiredMixin` |
| `templates/staff/base_admin.html` sidebar | Resources | `staff:resource_list` | `ResourceListView` | real (`WORKING_MINIMAL`) | `StaffRequiredMixin` |
| `templates/staff/base_admin.html` sidebar | Support Inbox | `staff:support_inbox` | `SupportInboxView` | truthful stub (`STUBBED_TRUTHFULLY`) | `StaffRequiredMixin` |
| `templates/staff/base_admin.html` sidebar | Settings | `staff:settings` | `SettingsView` | truthful stub (`STUBBED_TRUTHFULLY`) | `StaffRequiredMixin` |
| `templates/staff/base_admin.html` sidebar | Logs | `staff:logs` | `ActivityLogsView` | truthful stub (`STUBBED_TRUTHFULLY`) | `StaffRequiredMixin` |
| `templates/staff/base_admin.html` topbar | Logout | `staff:logout` | `AdminLogoutView` | real (`WORKING_MINIMAL`) | CSRF-protected POST form |

## Staff Dashboard Quick Actions / Cards

| Appears in | Nav item/button | Route target | View handler | Runtime destination status | Permission handling |
| --- | --- | --- | --- | --- | --- |
| `templates/staff/dashboard.html` | Add Question | `staff:question_create` | `QuestionCreateView` | real (`WORKING_MINIMAL`) | `StaffRequiredMixin` |
| `templates/staff/dashboard.html` | Bulk Upload | `staff:bulk_question_upload` | `BulkQuestionUploadView` | real (`WORKING_MINIMAL`) | `StaffRequiredMixin` |
| `templates/staff/dashboard.html` | Review Payments | `staff:payment_list` | `PaymentListView` | real (`FULLY_INTEGRATED`) | `StaffRequiredMixin` |
| `templates/staff/dashboard.html` | Manage Users | `staff:user_list` | `UserListView` | real (`WORKING_MINIMAL`) | `StaffRequiredMixin` |
| `templates/staff/dashboard.html` | View All Attempts | `staff:quiz_list` | `QuizAttemptListView` | truthful stub (`STUBBED_TRUTHFULLY`) | `StaffRequiredMixin` |
