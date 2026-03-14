# Backend-Frontend Integration Truth Map

Date: 2026-03-14  
Scope: Current code truth only (`core/`, `staff/`, `templates/`, `static/`, `tests/automated/`)

## Classification and Coverage Legend

- Classifications: `FULLY_INTEGRATED`, `WORKING_MINIMAL`, `PARTIALLY_INTEGRATED`, `FRONTEND_ONLY`, `BACKEND_ONLY`, `STUBBED_TRUTHFULLY`, `DRIFT_BROKEN`, `UNREACHABLE`
- Test coverage labels: `COVERED_HAPPY_PATH`, `COVERED_PARTIAL`, `SMOKE_ONLY`, `NOT_COVERED`

---

## Public / Student Flows

### P01 Home / Landing
- Entry URL/name: `/` (`core:home`)
- Navigation source: navbar brand, footer
- View/controller: `core.views.main_views.HomeView`
- Form/input contract: none
- Models touched: `Subject`, `Question`, `UserProfile`
- Template/assets: `templates/core/home.html`
- Methods/actions: `GET`
- Success path: landing renders featured subjects and stats
- Failure path: no explicit fallback UI if stats queries fail
- Tests: `tests/automated/test_smoke_routes.py`
- Classification: `WORKING_MINIMAL`
- Coverage: `SMOKE_ONLY`

### P02 Signup
- Entry URL/name: `/signup/` (`core:signup`)
- Navigation source: navbar auth button
- View/controller: `core.views.auth_views.RegisterView`
- Form/input contract: registration form (name/email/username/password + profile fields)
- Models touched: `User`, `UserProfile`
- Template/assets: `templates/core/auth/register.html`
- Methods/actions: `GET`, `POST`
- Success path: user + profile created, redirect to `core:dashboard`
- Failure path: form errors re-render
- Tests: `tests/automated/test_auth_and_profile.py`
- Classification: `FULLY_INTEGRATED`
- Coverage: `COVERED_HAPPY_PATH`

### P03 Login / Logout
- Entry URL/name: `/login/` (`core:login`), `/logout/` (`core:logout`)
- Navigation source: navbar auth button, user dropdown
- View/controller: `CustomLoginView`, `CustomLogoutView`
- Form/input contract: username/email + password
- Models touched: `User`
- Template/assets: `templates/core/auth/login.html`, logout success template
- Methods/actions: `GET`, `POST`
- Success path: login redirects dashboard; logout clears session
- Failure path: invalid credentials shown in form/messages
- Tests: `tests/automated/test_auth_and_profile.py`, `test_smoke_routes.py`
- Classification: `FULLY_INTEGRATED`
- Coverage: `COVERED_HAPPY_PATH`

### P04 Profile View/Edit
- Entry URL/name: `/profile/` (`core:profile`), `/profile/edit/` (`core:profile_edit`)
- Navigation source: navbar user dropdown
- View/controller: `ProfileView`, `ProfileEditView`
- Form/input contract: profile fields (`year_of_study`, `province`, `college_type`, etc.)
- Models touched: `UserProfile`
- Template/assets: `templates/core/profile/profile.html`, `profile_edit.html`
- Methods/actions: `GET`, `POST` (edit)
- Success path: profile updates and redirects
- Failure path: form validation errors
- Tests: `tests/automated/test_auth_and_profile.py`
- Classification: `FULLY_INTEGRATED`
- Coverage: `COVERED_HAPPY_PATH`

### P05 Dashboard
- Entry URL/name: `/dashboard/` (`core:dashboard`)
- Navigation source: navbar, post-login redirect
- View/controller: `core.views.main_views.DashboardView`
- Form/input contract: none
- Models touched: `QuizSession`, `Subject`
- Template/assets: `templates/core/dashboard.html`
- Methods/actions: `GET`
- Success path: stats, recent quizzes, action links render
- Failure path: login-required redirect when anonymous
- Tests: `tests/automated/test_auth_and_profile.py`, `test_smoke_routes.py`
- Classification: `WORKING_MINIMAL`
- Coverage: `COVERED_PARTIAL`

### P06 Question Bank
- Entry URL/name: `/questions/` (`core:question_bank`)
- Navigation source: navbar, dashboard quick action
- View/controller: `core.views.main_views.QuestionBankView`
- Form/input contract: query params (`year`, `subject`, `topic`, `difficulty`)
- Models touched: `Subject`, `Topic`, `Question`
- Template/assets: `templates/core/question_bank.html`
- Methods/actions: `GET`
- Success path: filtered subjects/topics render
- Failure path: invalid subject id returns 404
- Tests: `tests/automated/test_question_bank_flow.py`
- Classification: `WORKING_MINIMAL`
- Coverage: `COVERED_PARTIAL`

### P07 Subject Detail
- Entry URL/name: `/subjects/<pk>/` (`core:subject_detail`)
- Navigation source: question bank cards
- View/controller: `core.views.main_views.SubjectDetailView`
- Form/input contract: none
- Models touched: `Subject`, `Topic`, `Question`, resource models via annotations
- Template/assets: `templates/core/subject_detail.html`
- Methods/actions: `GET`
- Success path: topic grid and subject stats render
- Failure path: no critical runtime break; quick-start CTA is now guarded when subject has zero topics
- Tests: `tests/automated/test_integration_repair_flows.py`
- Classification: `WORKING_MINIMAL`
- Coverage: `COVERED_PARTIAL`

### P08 Topic Detail
- Entry URL/name: `/topics/<pk>/` (`core:topic_detail`)
- Navigation source: quiz center/topic cards, subject detail
- View/controller: `core.views.main_views.TopicDetailView`
- Form/input contract: none
- Models touched: `Topic`, `Question`, `Note`, `Video`, `Flashcard`, `UserProgress`
- Template/assets: `templates/core/topic_detail.html`
- Methods/actions: `GET`
- Success path: topic details render from current view contract with real quiz/resource links
- Failure path: no active broken route references in template; non-existent comment/bookmark endpoints removed
- Tests: `tests/automated/test_integration_repair_flows.py`
- Classification: `WORKING_MINIMAL`
- Coverage: `COVERED_PARTIAL`

### P09 Quiz Lifecycle (start/session/answer/submit/result/history)
- Entry URL/name: `core:start_quiz`, `core:quiz_session`, `core:quiz_question`, `core:submit_quiz`, `core:quiz_result`, `core:results`
- Navigation source: quiz center topic cards, dashboard links
- View/controller: `core.views.quiz_views.*`
- Form/input contract: `QuizStartForm`; answer POST `selected_option`, `time_taken`
- Models touched: `QuizSession`, `UserAnswer`, `Question`, `UserProfile`
- Template/assets: `templates/core/quiz/*.html`
- Methods/actions: `GET`, `POST`, JSON response on answer POST
- Success path: session created -> answers saved -> submit computes score -> result/history
- Failure path: invalid options/unauthorized session guarded in view logic
- Tests: `tests/automated/test_quiz_flow.py`, smoke/protected-route checks
- Classification: `FULLY_INTEGRATED`
- Coverage: `COVERED_HAPPY_PATH`

### P10 Quiz Center Shell
- Entry URL/name: `/quiz/` (`core:quiz`)
- Navigation source: dashboard and protected routes
- View/controller: `core.views.quiz_views.QuizListView`
- Form/input contract: quick-start form posts to `core:start_quiz` with placeholder URL arg `0`
- Models touched: `Topic`, `QuizSession`
- Template/assets: `templates/core/quiz/quiz_list.html`
- Methods/actions: `GET`, embedded POST action for quick start
- Success path: topic cards start quizzes correctly
- Failure path: quick-start form action uses `/quiz/topic/0/`, fragile if topic not selected/invalid
- Tests: route/auth smoke only
- Classification: `PARTIALLY_INTEGRATED`
- Coverage: `SMOKE_ONLY`

### P11 Resources Hub
- Entry URL/name: `/resources/` (`core:resources`)
- Navigation source: navbar resources dropdown, dashboard
- View/controller: `core.views.resource_views.ResourcesView`
- Form/input contract: filter UI is mostly client-side
- Models touched: `Subject`, `Note`, `Video`, `Flashcard`
- Template/assets: `templates/core/resources/resources.html`, `static/core/js/resources.js`
- Methods/actions: `GET` + client JS actions
- Success path: page and featured cards render
- Failure path: now server-rendered without dead AJAX runtime assumptions from `resources.js`
- Tests: `tests/automated/test_smoke_routes.py`, `tests/automated/test_integration_repair_flows.py`
- Classification: `WORKING_MINIMAL`
- Coverage: `COVERED_PARTIAL`

### P12 Notes / Videos / Flashcards
- Entry URL/name: `core:notes_list`, `core:note_detail`, `core:videos_list`, `core:video_detail`, `core:flashcards_list`, `core:flashcard_study`
- Navigation source: resources hub and navbar dropdown
- View/controller: `core.views.resource_views.*`
- Form/input contract: mostly read-only GET pages
- Models touched: `Note`, `Video`, `Flashcard`, `Topic`
- Template/assets: `templates/core/resources/*`
- Methods/actions: `GET`
- Success path: list/detail/study pages render and show model data
- Failure path: premium-gating edge paths rely on model flags; limited test depth
- Tests: `tests/automated/test_resource_flow.py`
- Classification: `WORKING_MINIMAL`
- Coverage: `COVERED_PARTIAL`

### P13 Leaderboard
- Entry URL/name: `/leaderboard/` (`core:leaderboard`)
- Navigation source: navbar, dashboard/resource CTAs
- View/controller: `core.views.main_views.LeaderboardView`
- Form/input contract: none (server-rendered list)
- Models touched: `UserProfile`, `QuizSession`
- Template/assets: `templates/core/leaderboard.html`, `static/core/js/leaderboard.js`
- Methods/actions: `GET`
- Success path: server-rendered overall/weekly rankings display
- Failure path: now server-rendered without dead AJAX endpoint calls from `leaderboard.js`
- Tests: `tests/automated/test_integration_repair_flows.py` (runtime script contract), plus route smoke
- Classification: `WORKING_MINIMAL`
- Coverage: `COVERED_PARTIAL`

### P14 Subscription Plans
- Entry URL/name: `/subscribe/` (`core:subscription`)
- Navigation source: navbar upgrade, dashboard
- View/controller: `core.views.payment_views.SubscriptionView`
- Form/input contract: none on listing page
- Models touched: `SubscriptionPlan`, `UserProfile`
- Template/assets: `templates/core/subscription/subscription.html`
- Methods/actions: `GET`
- Success path: active plans and user premium status render
- Failure path: user profile lookup wrapped broadly (silent null fallback)
- Tests: smoke route coverage
- Classification: `WORKING_MINIMAL`
- Coverage: `SMOKE_ONLY`

### P15 Payment Instructions + Proof Upload + Status
- Entry URL/name: `core:payment`, `core:payment_proof_upload`, `core:payment_status`
- Navigation source: subscription page and profile/subscription menu
- View/controller: `PaymentView`, `PaymentProofUploadView`, `PaymentStatusView`
- Form/input contract: `PaymentProofForm`
- Models touched: `SubscriptionPlan`, `PaymentProof`, `UserProfile`
- Template/assets: `templates/core/subscription/payment*.html`
- Methods/actions: `GET`, `POST` (multipart upload)
- Success path: pending proof created; staff review updates status; user sees status/history
- Failure path: duplicate-pending check, form validation, auth gates
- Tests: `tests/automated/test_payment_flow.py`, smoke/protected-route tests
- Classification: `FULLY_INTEGRATED`
- Coverage: `COVERED_HAPPY_PATH`

### P16 Contact Page (UI Path)
- Entry URL/name: `/contact/` (`core:contact`)
- Navigation source: navbar/footer/static links
- View/controller: `core.views.static_views.ContactView`
- Form/input contract used by template: `ContactForm` (`name`, `email`, `subject`, `message`)
- Models touched: none
- Template/assets: `templates/core/static/contact.html`
- Methods/actions: `GET`, `POST`
- Success path: valid form POST reaches backend handler and returns success message
- Failure path: invalid form re-renders with field errors
- Tests: `tests/automated/test_smoke_routes.py`, `tests/automated/test_integration_repair_flows.py`
- Classification: `WORKING_MINIMAL`
- Coverage: `COVERED_PARTIAL`

### P17 Contact Backend Handler (server POST branch)
- Entry URL/name: `/contact/` POST in `ContactView.post`
- Navigation source: active contact template form submit
- View/controller: `core.views.static_views.ContactView.post`
- Form/input contract: `core.forms.payment_forms.ContactForm` (`name`, `email`, `subject`, `message`)
- Models touched: none
- Template/assets: `templates/core/static/contact.html` and server-side messages
- Methods/actions: `POST`
- Success path: message success feedback on valid form
- Failure path: form-invalid re-render
- Tests: `tests/automated/test_integration_repair_flows.py`
- Classification: `WORKING_MINIMAL`
- Coverage: `COVERED_PARTIAL`

### P18 Static Policy/Info Pages
- Entry URL/name: `core:about`, `core:faq`, `core:terms`, `core:privacy`
- Navigation source: navbar/footer
- View/controller: `AboutView`, `FAQView`, `TermsView`, `PrivacyView`
- Form/input contract: none
- Models touched: `AboutView` reads counts; others static data
- Template/assets: `templates/core/static/*.html`
- Methods/actions: `GET`
- Success path: pages render
- Failure path: minimal dynamic dependencies
- Tests: `tests/automated/test_smoke_routes.py`
- Classification: `WORKING_MINIMAL`
- Coverage: `SMOKE_ONLY`

---

## Staff / Admin Flows

### S01 Staff Login / Logout
- Entry URL/name: `/staff/login/` (`staff:login`), `/staff/logout/` (`staff:logout`)
- Navigation source: direct staff URL, topbar dropdown logout
- View/controller: `staff.views.auth_views.AdminLoginView/AdminLogoutView`
- Form/input contract: admin credentials
- Models touched: `User`
- Template/assets: `templates/staff/auth/login.html`
- Methods/actions: `GET`, `POST`
- Success path: staff session and dashboard redirect
- Failure path: auth errors
- Tests: `tests/automated/test_smoke_routes.py` (login route)
- Classification: `WORKING_MINIMAL`
- Coverage: `SMOKE_ONLY`

### S02 Staff Dashboard
- Entry URL/name: `/staff/` (`staff:dashboard`)
- Navigation source: sidebar/dashboard link
- View/controller: `staff.views.dashboard_views.DashboardView`
- Form/input contract: none
- Models touched: `User`, `Question`, `PaymentProof`, `QuizSession`
- Template/assets: `templates/staff/dashboard.html`
- Methods/actions: `GET`
- Success path: admin metrics and quick actions render
- Failure path: auth gate via `StaffRequiredMixin`
- Tests: smoke protected-route checks
- Classification: `WORKING_MINIMAL`
- Coverage: `SMOKE_ONLY`

### S03 User List / Search / Bulk Actions
- Entry URL/name: `/staff/users/` (`staff:user_list`)
- Navigation source: sidebar + dashboard quick action
- View/controller: `staff.views.user_views.UserListView`
- Form/input contract: search GET + bulk POST (`action`, `user_ids`)
- Models touched: `User`, `UserProfile`
- Template/assets: `templates/staff/users/user_list.html`, `static/staff/js/user_list.js`
- Methods/actions: `GET`, `POST`
- Success path: list/search and activate/deactivate/premium/export selected work
- Failure path: unknown/invalid actions return messages
- Tests: indirect via user flow; no deep bulk-action assertions
- Classification: `WORKING_MINIMAL`
- Coverage: `COVERED_PARTIAL`

### S04 User Create
- Entry URL/name: `/staff/users/create/` (`staff:user_create`)
- Navigation source: user list header action
- View/controller: `staff.views.user_views.UserCreateView`
- Form/input contract: user + profile fields and role flags
- Models touched: `User`, `UserProfile`
- Template/assets: `templates/staff/users/user_create.html`
- Methods/actions: `GET`, `POST`
- Success path: user/profile created, redirect list
- Failure path: validation errors
- Tests: `tests/automated/test_staff_user_flow.py`
- Classification: `FULLY_INTEGRATED`
- Coverage: `COVERED_HAPPY_PATH`

### S05 User Detail Actions
- Entry URL/name: `/staff/users/<pk>/` (`staff:user_detail`)
- Navigation source: user list row action
- View/controller: `UserDetailView` (AJAX action POST)
- Form/input contract: POST `action` (`toggle_status`, `toggle_premium`, `send_welcome_email`, `reset_password`)
- Models touched: `User`, `UserProfile`
- Template/assets: `templates/staff/users/user_detail.html`
- Methods/actions: `GET`, `POST` JSON
- Success path: status/premium toggles and export action reachable
- Failure path: broad exception wrapper in view can hide root-cause details
- Tests: no dedicated automated tests for these AJAX actions
- Classification: `PARTIALLY_INTEGRATED`
- Coverage: `NOT_COVERED`

### S06 Bulk User Upload
- Entry URL/name: `/staff/users/bulk-upload/` (`staff:bulk_user_upload`)
- Navigation source: user list header action
- View/controller: `BulkUserUploadView`
- Form/input contract: CSV upload + preview/confirm actions
- Models touched: `User`, `UserProfile`
- Template/assets: `templates/staff/users/bulk_upload.html`
- Methods/actions: `GET`, `POST`
- Success path: preview -> confirm creates users
- Failure path: confirm without preview returns back with message
- Tests: `tests/automated/test_staff_user_flow.py`
- Classification: `FULLY_INTEGRATED`
- Coverage: `COVERED_HAPPY_PATH`

### S07 Subject Management
- Entry URL/name: `/staff/subjects/` and related AJAX/toggle endpoints
- Navigation source: sidebar Subjects
- View/controller: `staff.views.subject_views.*`
- Form/input contract: `SubjectForm` + JSON payload for AJAX create/edit
- Models touched: `Subject`, `Topic` (counts/listing)
- Template/assets: `templates/staff/subjects/subject_list_new.html`
- Methods/actions: `GET`, `POST`
- Success path: create/edit/toggle/list functional in new JS-driven page
- Failure path: standard validation errors on duplicate names/codes; CSRF now enforced on mutating AJAX endpoints
- Tests: `test_staff_subject_crud.py`, `test_staff_management_routes.py`, `test_integration_repair_flows.py`
- Classification: `WORKING_MINIMAL`
- Coverage: `COVERED_PARTIAL`

### S08 Topic Management + Topic Bulk Upload
- Entry URL/name: `/staff/topics/`, `/staff/topics/bulk-upload/`
- Navigation source: subjects page topic actions; direct topic menu routes
- View/controller: `TopicListEnhancedView`, `TopicCreate/EditAjaxEnhancedView`, `TopicBulkUploadView`
- Form/input contract: topic form + CSV fields (`LOs`, `Sub-Topic`, `Topic`, `Subject`, ...)
- Models touched: `Topic`, `Subject`, `Tag`, `SubTag`
- Template/assets: `templates/staff/topics/topic_list_new.html`, bulk upload template
- Methods/actions: `GET`, `POST`
- Success path: topic CRUD and bulk topic creation work
- Failure path: limited validation/testing on AJAX edge cases
- Tests: `tests/automated/test_staff_question_and_topic_flows.py`, `test_staff_management_routes.py`
- Classification: `WORKING_MINIMAL`
- Coverage: `COVERED_PARTIAL`

### S09 Question CRUD
- Entry URL/name: `staff:question_list`, `question_create`, `question_edit`, `question_delete`
- Navigation source: sidebar Questions, dashboard quick action
- View/controller: `staff.views.question_views.*`
- Form/input contract: question form + dynamic option fields
- Models touched: `Question`, `Option`, `Topic`
- Template/assets: `templates/staff/questions/*.html`
- Methods/actions: `GET`, `POST`
- Success path: create/edit/list paths render and create valid options
- Failure path: incomplete direct coverage for delete and bulk actions
- Tests: `test_staff_question_and_topic_flows.py`, `test_staff_management_routes.py`
- Classification: `WORKING_MINIMAL`
- Coverage: `COVERED_PARTIAL`

### S10 Question Bulk Upload
- Entry URL/name: `/staff/questions/bulk-upload/` (`staff:bulk_question_upload`)
- Navigation source: dashboard quick action
- View/controller: `BulkQuestionUploadView`
- Form/input contract: CSV-derived options and correct answer mapping
- Models touched: `Question`, `Option`
- Template/assets: `templates/staff/questions/bulk_upload.html`
- Methods/actions: `GET`, `POST`
- Success path: CSV rows map to current `Option` schema with deterministic option ordering and correct-answer mapping
- Failure path: invalid CSV column contracts fail via form validation
- Tests: `tests/automated/test_integration_repair_flows.py`
- Classification: `WORKING_MINIMAL`
- Coverage: `COVERED_PARTIAL`

### S11 Tag/Subtag Management
- Entry URL/name: `/staff/tags/` + AJAX endpoints
- Navigation source: sidebar Tags
- View/controller: `staff.views.tag_views.*`
- Form/input contract: AJAX payloads and legacy form routes
- Models touched: `Tag`, `SubTag`
- Template/assets: `templates/staff/tags/tag_list.html`
- Methods/actions: `GET`, `POST`
- Success path: AJAX list/add/edit/toggle intended from tag management page
- Failure path: mixed legacy + AJAX surfaces with weak automated coverage
- Tests: limited smoke (`staff:tag_delete`) only
- Classification: `PARTIALLY_INTEGRATED`
- Coverage: `SMOKE_ONLY`

### S12 Resource Management (staff)
- Entry URL/name: `staff:resource_list`, `note_*`, `video_*`, `flashcard_*`
- Navigation source: sidebar Resources
- View/controller: `staff.views.resource_views.*`
- Form/input contract: model forms for note/video/flashcard
- Models touched: `Note`, `Video`, `Flashcard`, `Topic`
- Template/assets: `templates/staff/resources/*.html`
- Methods/actions: `GET`, `POST`
- Success path: management pages render and CRUD paths exist
- Failure path: mostly render-tested; low behavior assertions
- Tests: `tests/automated/test_staff_management_routes.py`
- Classification: `WORKING_MINIMAL`
- Coverage: `COVERED_PARTIAL`

### S13 Payment Review Queue and History
- Entry URL/name: `staff:payment_list`, `staff:payment_review`, `staff:payment_history`
- Navigation source: sidebar Payments, dashboard quick action
- View/controller: `staff.views.payment_views.*`
- Form/input contract: `staff.forms.payment_forms.PaymentReviewForm`
- Models touched: `PaymentProof`, `UserProfile`, `SubscriptionPlan`
- Template/assets: `templates/staff/payments/*.html`
- Methods/actions: `GET`, `POST`
- Success path: approve/reject/pending updates status and premium access
- Failure path: invalid review payload handled by form validation
- Tests: `tests/automated/test_payment_flow.py`, smoke routes
- Classification: `FULLY_INTEGRATED`
- Coverage: `COVERED_HAPPY_PATH`

### S14 Support Inbox/Message
- Entry URL/name: `staff:support_inbox`, `staff:support_message`
- Navigation source: sidebar Support Inbox
- View/controller: `staff.views.support_views.*`
- Form/input contract: none
- Models touched: none (`get_queryset` returns empty list intentionally)
- Template/assets: `templates/staff/support/inbox.html`, `message_detail.html`
- Methods/actions: `GET`
- Success path: explicit placeholder text explains missing model
- Failure path: none (truthful placeholder rendering)
- Tests: `tests/automated/test_smoke_routes.py` placeholder assertions
- Classification: `STUBBED_TRUTHFULLY`
- Coverage: `COVERED_HAPPY_PATH`

### S15 Settings / Logs
- Entry URL/name: `staff:settings`, `staff:logs`
- Navigation source: sidebar + topbar dropdown
- View/controller: `SettingsView`, `ActivityLogsView`
- Form/input contract: none
- Models touched: none
- Template/assets: `templates/staff/settings/settings.html`, `logs.html`
- Methods/actions: `GET`
- Success path: stable placeholder pages render
- Failure path: no functional admin settings/logs yet
- Tests: none
- Classification: `STUBBED_TRUTHFULLY`
- Coverage: `NOT_COVERED`

### S16 Staff Quiz Attempts
- Entry URL/name: `/staff/quizzes/` (`staff:quiz_list`)
- Navigation source: dashboard recent-quiz card action
- View/controller: `QuizAttemptListView`
- Form/input contract: none
- Models touched: `QuizSession`
- Template/assets: `templates/staff/quizzes/quiz_list.html`
- Methods/actions: `GET`
- Success path: route renders clean placeholder card through `QuizAttemptListView`
- Failure path: no list implementation yet (truthful placeholder only)
- Tests: `tests/automated/test_integration_repair_flows.py`
- Classification: `STUBBED_TRUTHFULLY`
- Coverage: `COVERED_PARTIAL`

### S17 Staff Leaderboard
- Entry URL/name: `/staff/leaderboard/` (`staff:leaderboard`)
- Navigation source: direct route (not primary sidebar item)
- View/controller: `staff.views.quiz_views.LeaderboardView`
- Form/input contract: none
- Models touched: `QuizSession`
- Template/assets: `templates/staff/quizzes/leaderboard.html`
- Methods/actions: `GET`
- Success path: route renders "coming soon" placeholder
- Failure path: queryset exists but template does not expose data
- Tests: none
- Classification: `STUBBED_TRUTHFULLY`
- Coverage: `NOT_COVERED`

### S18 User Export Endpoint
- Entry URL/name: `/staff/users/<pk>/export/` (`staff:user_export_single`), `/staff/users/export/`
- Navigation source: user detail "Export User Data" button; no obvious list-level direct link
- View/controller: `staff.views.user_views.UserExportView`
- Form/input contract: `GET` download
- Models touched: `User`, `UserProfile`, `QuizSession`
- Template/assets: triggered from `templates/staff/users/user_detail.html` JS helper
- Methods/actions: `GET`
- Success path: single-user and multi-user CSV responses both download with correct branch-specific structure
- Failure path: no critical drift found in active export logic after repair
- Tests: `tests/automated/test_integration_repair_flows.py`
- Classification: `WORKING_MINIMAL`
- Coverage: `COVERED_PARTIAL`

---

## Unreachable / Drifted Runtime Artifacts

### U01 Legacy Quiz JS
- Entry: `static/core/js/quiz.js`
- Status: retired from active source; quiz templates do not include a legacy standalone quiz JS asset
- Classification: `RETIRED`

### U02 Legacy Tag Route Aliases/Form Entry
- Entry: retired aliases/routes (`staff:tag_add`, `staff:ajax_tag_create`, `staff:subtag_create`, `staff:subtag_edit`, `staff:tag_create`, `staff:tag_edit`)
- Status: canonical staff tag runtime is `staff:tag_list` plus AJAX endpoints (`tag_create_ajax`, `tag_update_ajax`, `subtag_create_ajax`, `subtag_update_ajax`, etc.)
- Classification: `RETIRED_TO_REMOVE_AMBIGUITY`
