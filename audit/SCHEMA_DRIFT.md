# SCHEMA_DRIFT.md
## MedPrep — Database Schema vs Model Drift Analysis

Comparison between `core/models/` (Django model definitions) and the live `db.sqlite3` schema.

All migrations through `0009` have been applied. Overall drift is **minimal** — the schema is well-synchronized.

---

## No Drift Found — Models Match DB

The following models match their DB tables exactly:

| Model | DB Table | Status |
|-------|----------|--------|
| `UserProfile` | `core_userprofile` | ✅ Match |
| `Subject` | `core_subject` | ✅ Match |
| `Topic` | `core_topic` | ✅ Match |
| `Question` | `core_question` | ✅ Match |
| `Option` | `core_option` | ✅ Match |
| `QuizSession` | `core_quizsession` | ✅ Match |
| `UserAnswer` | `core_useranswer` | ✅ Match |
| `Note` | `core_note` | ✅ Match |
| `Flashcard` | `core_flashcard` | ✅ Match |
| `VideoResource` | `core_videoresource` | ✅ Match |
| `UserProgress` | `core_userprogress` | ✅ Match |
| `SubscriptionPlan` | `core_subscriptionplan` | ✅ Match |
| `PaymentProof` | `core_paymentproof` | ✅ Match |
| `Tag` | `core_tag` | ✅ Match |
| `Subtag` | `core_subtag` | ✅ Match |

---

## M2M Through Tables — All Present

| Through Table | Status |
|--------------|--------|
| `core_userprofile_tags` | ✅ Present |
| `core_topic_tags` | ✅ Present |
| `core_question_tags` | ✅ Present |
| `core_note_tags` | ✅ Present |
| `core_flashcard_tags` | ✅ Present |
| `core_videoresource_tags` | ✅ Present |
| `core_quizsession_questions` | ✅ Present |
| `core_userprogress_notes_read` | ✅ Present |
| `core_userprogress_flashcards_reviewed` | ✅ Present |
| `core_userprogress_videos_watched` | ✅ Present |

---

## Minor Notes (Not Drift, But Worth Tracking)

### 1. `Tag` Model — `apply_to_all_resources` Logic Is Inverted in DB Default

The model defines `apply_to_all_resources = models.BooleanField(default=True)` while `apply_to_mcq`, `apply_to_videos`, `apply_to_notes` default to `False`. This is semantically odd — if `apply_to_all_resources=True` is the default, the specific flags (`apply_to_mcq`, etc.) are never consulted.  
**No schema drift** — values are stored correctly — but the flag logic may produce unintended filtering behaviour if code checks individual flags while the `apply_to_all_resources` flag is always True.

### 2. `PaymentProof.status` Has `'submitted'` Referenced in Code But Not in Choices

The model defines `STATUS_CHOICES` as: `pending`, `approved`, `rejected`, `expired`.  
`staff/views/dashboard_views.py` references `status='submitted'` in a filter. This is not a schema drift issue but a **code logic bug** (see BROKEN_REFERENCES.md #3).

### 3. No Unapplied Migrations

```
django_migrations table shows all 9 core migrations applied:
  0001_initial
  0002_userprofile_college_type_userprofile_province_and_more
  0003_tag_flashcard_tags_note_tags_question_tags_and_more
  0004_userprofile_tags
  0005_add_tags_to_userprofile
  0006_update_userprofile_choices
  0007_question_reference
  0008_alter_tag_options_remove_tag_parent_and_more
  0009_topic_tags
```

No pending migrations detected.

---

## Full DB Table Inventory

All tables present in `db.sqlite3`:

```
auth_group
auth_group_permissions
auth_permission
auth_user
auth_user_groups
auth_user_user_permissions
core_flashcard
core_flashcard_tags
core_note
core_note_tags
core_option
core_paymentproof
core_question
core_question_tags
core_quizsession
core_quizsession_questions
core_subject
core_subscriptionplan
core_subtag
core_tag
core_topic
core_topic_tags
core_useranswer
core_userprofile
core_userprofile_tags
core_userprogress
core_userprogress_flashcards_reviewed
core_userprogress_notes_read
core_userprogress_videos_watched
core_videoresource
core_videoresource_tags
django_admin_log
django_content_type
django_migrations
django_session
```

Total: **35 tables** — all expected, none missing, none unexpected.

---

## Verdict

**Schema drift: NONE.** The database is fully synchronized with the current model definitions.  
All 9 migrations are applied. All M2M through tables are present.
