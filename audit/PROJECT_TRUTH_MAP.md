# PROJECT_TRUTH_MAP.md
## MedPrep — Final Project Truth Map

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Django Project: medprep                  │
│                    (medprep/settings.py)                     │
└───────────────────┬──────────────────────────────────────────┘
                    │
        ┌───────────┴──────────────┐
        │                          │
┌───────▼──────────┐    ┌──────────▼───────────┐
│   app: core      │    │    app: staff        │
│  (public-facing) │    │  (CMS backoffice)    │
│                  │    │                      │
│  /               │    │  /staff/             │
│  /signup/        │    │  /staff/users/       │
│  /login/         │    │  /staff/questions/   │
│  /dashboard/     │    │  /staff/subjects/    │
│  /quiz/          │    │  /staff/topics/      │
│  /questions/     │    │  /staff/tags/        │
│  /resources/     │    │  /staff/resources/   │
│  /subscribe/     │    │  /staff/payments/    │
│  /leaderboard/   │    │  /staff/support/     │
│  /profile/       │    │  /staff/settings/    │
└──────────────────┘    └──────────────────────┘
        │                          │
        └───────────┬──────────────┘
                    │
    ┌───────────────▼────────────────┐
    │        Shared Models           │
    │   (core/models/ package)       │
    │                                │
    │  UserProfile   ←── auth.User   │
    │  Subject → Topic → Question    │
    │                    └→ Option   │
    │  QuizSession → UserAnswer      │
    │  Note, Flashcard, VideoResource│
    │  UserProgress                  │
    │  SubscriptionPlan              │
    │  PaymentProof                  │
    │  Tag → Subtag                  │
    └───────────────┬────────────────┘
                    │
    ┌───────────────▼────────────────┐
    │        SQLite Database         │
    │       (db.sqlite3)             │
    │   35 tables — fully migrated   │
    └────────────────────────────────┘
```

---

## Working Modules ✅

These are verified functional based on code analysis:

| Module | Notes |
|--------|-------|
| User registration + login | Full flow with profile auto-creation |
| Custom logout (GET + POST) | Non-standard but functional |
| User dashboard | Stats, recent quizzes, subject progress |
| Question bank with filters | Subject, topic, difficulty, year filters |
| Quiz list | Recent sessions, available topics |
| Quiz session interface | Display and progress tracking |
| Quiz result display | Detailed per-question analysis |
| Subject detail page | Topics with counts |
| Topic detail page | Resources + quiz gating by premium |
| Leaderboard (global + weekly) | Working aggregation |
| Resources overview page | Navigational landing page |
| Subscription plans page | Plans listed from DB |
| Static pages (About/Contact/FAQ/Terms/Privacy) | All templates + views present |
| Password reset (confirm + complete steps) | Custom templates present |
| Staff login/logout | Works |
| Staff dashboard | Stats overview (minor bug in payment count) |
| Staff user management | Full CRUD + bulk upload + export |
| Staff question management | Full CRUD + bulk CSV upload + AJAX |
| Staff subject management | Full CRUD + AJAX inline edit |
| Staff topic management | Full CRUD + AJAX + bulk upload |
| Staff tag/subtag management | Full CRUD + AJAX toggle |
| Staff quiz/leaderboard views | List views working |
| Staff notes/videos/flashcards CRUD | All templates + forms present |
| Staff payment list | Template present |
| Staff settings/logs | Static display templates present |

---

## Broken Modules 🔴

These have **hard bugs** causing runtime errors or HTTP 500s:

| Module | Bug | File | Fix |
|--------|-----|------|-----|
| Start Quiz page | Template `core/quiz/start_quiz.html` missing | `quiz_views.py` | Create template |
| Quiz question answering | `quizsession=quiz_session` M2M lookup crash | `quiz_views.py:QuizQuestionView` | Change to `quiz_sessions=quiz_session` |
| Profile edit page | Template `core/auth/profile_edit.html` missing | `auth_views.py` | Create template |
| Profile auto-create | `year_of_study='1st'` is invalid choice (should be `'1st_year'`) | `auth_views.py` | Fix default string |
| `/results/` route | `DetailView` without `pk` → 500 | `core/urls.py` | Remove or remap route |
| Staff resource aggregate | `ResourceListView.get_queryset()` returns `None` | `resource_views.py` | Return empty queryset |
| Staff support views | No model, no templates, `DetailView` with no `get_object()` | `support_views.py` | Implement or guard |

---

## Missing Modules ⬜

These are partially or entirely unimplemented:

| Module | What's Missing |
|--------|---------------|
| Notes list page | Template `core/resources/notes_list.html` |
| Note detail page | Template `core/resources/note_detail.html` |
| Flashcards list page | Template `core/resources/flashcards_list.html` |
| Flashcard study page | Template `core/resources/flashcard_study.html` |
| Videos list page | Template `core/resources/videos_list.html` |
| Video detail page | Template `core/resources/video_detail.html` |
| Payment page | Template `core/subscription/payment.html` |
| Payment proof upload page | Template `core/subscription/payment_proof_upload.html` |
| Payment status page | Template `core/subscription/payment_status.html` |
| Staff payment review | Template `staff/payments/payment_review.html` |
| Staff payment history | Template `staff/payments/payment_history.html` |
| Staff support inbox | Template + model + full implementation |
| Staff support message detail | Template + implementation |
| `Tag.get_resource_count()` | Actual aggregation logic |
| `Subtag.get_resource_count()` | Actual aggregation logic |
| Password reset form/done | Custom templates (using Django admin defaults as fallback) |

---

## Stale / Dead Code ⚠️

| File | Issue |
|------|-------|
| `core/models.py` | Dead root file — shadowed by `core/models/` package |
| `core/views.py` | Dead root file — shadowed by `core/views/` package |
| `staff/forms.py` | Dead root file — shadowed by `staff/forms/` package |
| `templates/core/login.html` | Duplicate — no view points to it |
| `templates/core/signup.html` | Duplicate — no view points to it |
| `templates/staff/subjects/subject_list_new.html` | Revision artifact |
| `templates/staff/topics/topic_list_new.html` | Revision artifact |
| `scripts/` directory | 20+ one-off debug scripts, not production code |
| `tests/` directory | 60+ standalone HTTP test scripts, not `TestCase`-based |
| `debug_*.py` root files | One-off debug scripts at repo root |

---

## Recommended Fixes — Priority Order

### Priority 1 — Crash Bugs (Fix Immediately)

1. **`quiz_views.py` line ~175**: Change `quizsession=quiz_session` → `quiz_sessions=quiz_session`
2. **`auth_views.py`**: Change `year_of_study='1st'` → `year_of_study='1st_year'` in both `ProfileView` and `ProfileEditView`
3. **`core/urls.py`**: Remove or remap `/results/` — it calls `QuizResultView` without a `pk` and will 500
4. **`resource_views.py`**: Change `ResourceListView.get_queryset()` to return `Note.objects.none()` (or implement)

### Priority 2 — Missing Templates (Create to Restore Flow)

5. Create `core/auth/profile_edit.html` (profile editing UI)
6. Create `core/quiz/start_quiz.html` (quiz configuration + launch form)
7. Create `core/subscription/payment.html` (payment instructions)
8. Create `core/subscription/payment_proof_upload.html` (proof upload form)
9. Create `core/subscription/payment_status.html` (payment history + status)
10. Create `staff/payments/payment_review.html` (admin review interface)
11. Create `staff/payments/payment_history.html` (admin payment history)
12. Create resource templates: `notes_list.html`, `note_detail.html`, `flashcards_list.html`, `flashcard_study.html`, `videos_list.html`, `video_detail.html`

### Priority 3 — Logic Fixes

13. **`dashboard_views.py`**: Remove `Q(status='submitted')` from pending payments filter
14. **`tag_models.py`**: Implement `Tag.get_resource_count()` and `Subtag.get_resource_count()` using proper M2M aggregation
15. **`support_views.py`**: Either create a `ContactMessage` model + full implementation, or add a guard raising `NotImplementedError` / HTTP 501

### Priority 4 — Cleanup

16. Delete `core/models.py`, `core/views.py`, `staff/forms.py` (stale root files)
17. Delete `templates/core/login.html`, `templates/core/signup.html` (unused duplicates)
18. Add `registration/password_reset_form.html` and `registration/password_reset_done.html` with project styling
19. Add real `TestCase`-based tests in `core/tests.py` to replace one-off scripts
20. Implement `Tag.get_resource_count()` with actual annotation

---

## Data Quality Notes

- **Database schema**: Fully synchronized with models (no drift)
- **Migrations**: All 9 applied, no pending migrations
- **No orphaned tables**: All 35 tables match expected model definitions
- **No missing tables**: Every model and M2M through-table exists in the DB

---

## Overall Health Score

| Dimension | Score | Notes |
|-----------|-------|-------|
| Model / DB consistency | 10/10 | No drift whatsoever |
| Staff CMS | 8/10 | 2 payment templates, support inbox missing |
| Auth / User flows | 7/10 | Profile edit missing, year_of_study bug |
| Quiz system | 5/10 | Start template + answer-saving crash |
| Resources (public) | 3/10 | 6/7 resource pages missing templates |
| Payments (public) | 4/10 | 3/4 payment pages missing templates |
| Code cleanliness | 6/10 | Stale files, placeholders, no proper tests |
| **Overall** | **6/10** | **Solid foundation, ~17 templates needed** |
