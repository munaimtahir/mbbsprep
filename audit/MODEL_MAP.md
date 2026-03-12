# MODEL_MAP.md
## MedPrep — Complete Model Map

---

## 1. UserProfile (`core/models/user_models.py`)

**Table:** `core_userprofile`

| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField PK | |
| `user` | OneToOneField → `auth.User` | CASCADE, UNIQUE |
| `year_of_study` | CharField(20) | Choices: 1st_year, 2nd_year, 3rd_year, 4th_year, final_year, graduate |
| `province` | CharField(100) | Choices: Punjab, Sindh, KPK, Balochistan, AJK |
| `college_type` | CharField(20) | Choices: Public, Private |
| `college_name` | CharField(200) | blank=True |
| `phone_number` | CharField(15) | blank=True |
| `profile_picture` | ImageField | upload_to=uploads/profiles/, nullable |
| `is_premium` | BooleanField | default=False |
| `premium_expires_at` | DateTimeField | null=True, blank=True |
| `total_quiz_score` | IntegerField | default=0 |
| `total_quizzes_taken` | IntegerField | default=0 |
| `created_at` | DateTimeField | auto_now_add |
| `updated_at` | DateTimeField | auto_now |
| `tags` | ManyToManyField → `Tag` | through `core_userprofile_tags` |

**Properties:** `average_score`, `is_premium_active`  
**Ordering:** `-created_at`

---

## 2. Subject (`core/models/academic_models.py`)

**Table:** `core_subject`

| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField PK | |
| `name` | CharField(100) | UNIQUE |
| `code` | CharField(10) | UNIQUE |
| `description` | TextField | blank=True |
| `year_applicable` | CharField(3) | Choices: 1st, 2nd, 3rd, 4th, 5th, all |
| `is_active` | BooleanField | default=True |
| `created_at` | DateTimeField | auto_now_add |

**Relationships:** Has many → `Topic` (related_name: `topics`)  
**Ordering:** `['year_applicable', 'name']`

---

## 3. Topic (`core/models/academic_models.py`)

**Table:** `core_topic`

| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField PK | |
| `subject` | ForeignKey → `Subject` | CASCADE, related_name=topics |
| `name` | CharField(200) | |
| `description` | TextField | blank=True |
| `order` | PositiveIntegerField | default=0 |
| `is_active` | BooleanField | default=True |
| `created_at` | DateTimeField | auto_now_add |
| `tags` | ManyToManyField → `Tag` | through `core_topic_tags`, related_name=topics |

**Constraints:** `unique_together = ['subject', 'name']`  
**Indexes:** `core_topic_subject_id_b64ece01`  
**Ordering:** `['subject', 'order', 'name']`

---

## 4. Question (`core/models/academic_models.py`)

**Table:** `core_question`

| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField PK | |
| `topic` | ForeignKey → `Topic` | CASCADE, related_name=questions |
| `question_text` | TextField | |
| `explanation` | TextField | |
| `reference` | CharField(200) | blank=True |
| `difficulty` | CharField(10) | Choices: easy, medium, hard |
| `is_premium` | BooleanField | default=False |
| `is_active` | BooleanField | default=True |
| `created_at` | DateTimeField | auto_now_add |
| `updated_at` | DateTimeField | auto_now |
| `tags` | ManyToManyField → `Tag` | through `core_question_tags`, related_name=questions |

**Indexes:** `core_question_topic_id_aeb94197`  
**Properties:** `correct_option`  
**Ordering:** `-created_at`

---

## 5. Option (`core/models/academic_models.py`)

**Table:** `core_option`

| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField PK | |
| `question` | ForeignKey → `Question` | CASCADE, related_name=options |
| `option_text` | CharField(500) | |
| `is_correct` | BooleanField | default=False |
| `order` | PositiveIntegerField | default=0 |

**Ordering:** `['question', 'order']`

---

## 6. QuizSession (`core/models/quiz_models.py`)

**Table:** `core_quizsession`

| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField PK | |
| `user` | ForeignKey → `auth.User` | CASCADE, related_name=quiz_sessions |
| `topic` | ForeignKey → `Topic` | CASCADE, related_name=quiz_sessions |
| `questions` | ManyToManyField → `Question` | through `core_quizsession_questions` |
| `status` | CharField(15) | Choices: in_progress, completed, abandoned |
| `score` | IntegerField | default=0 |
| `total_questions` | IntegerField | default=0 |
| `time_limit_minutes` | IntegerField | default=30 |
| `time_taken_seconds` | IntegerField | default=0 |
| `started_at` | DateTimeField | auto_now_add |
| `completed_at` | DateTimeField | null=True, blank=True |

**Indexes:** `user_id`, `topic_id`  
**Properties:** `percentage_score`, `time_taken_formatted`, `is_expired`  
**Methods:** `complete_quiz()`  
**Ordering:** `-started_at`

---

## 7. UserAnswer (`core/models/quiz_models.py`)

**Table:** `core_useranswer`

| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField PK | |
| `quiz_session` | ForeignKey → `QuizSession` | CASCADE, related_name=user_answers |
| `question` | ForeignKey → `Question` | CASCADE, related_name=user_answers |
| `selected_option` | ForeignKey → `Option` | CASCADE, related_name=user_selections, null/blank |
| `is_correct` | BooleanField | default=False; auto-set in save() |
| `time_taken_seconds` | IntegerField | default=0 |
| `answered_at` | DateTimeField | auto_now_add |

**Constraints:** `unique_together = ['quiz_session', 'question']`  
**Ordering:** `answered_at`

---

## 8. Note (`core/models/resource_models.py`)

**Table:** `core_note`

| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField PK | |
| `title` | CharField(200) | |
| `topic` | ForeignKey → `Topic` | CASCADE, related_name=notes |
| `content` | TextField | |
| `pdf_file` | FileField | upload_to=uploads/resources/notes/, nullable |
| `is_premium` | BooleanField | default=False |
| `is_active` | BooleanField | default=True |
| `created_by` | ForeignKey → `auth.User` | CASCADE, related_name=created_notes |
| `created_at` | DateTimeField | auto_now_add |
| `updated_at` | DateTimeField | auto_now |
| `tags` | ManyToManyField → `Tag` | through `core_note_tags` |

**Indexes:** `created_by_id`, `topic_id`  
**Ordering:** `-created_at`

---

## 9. Flashcard (`core/models/resource_models.py`)

**Table:** `core_flashcard`

| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField PK | |
| `topic` | ForeignKey → `Topic` | CASCADE, related_name=flashcards |
| `front_text` | CharField(500) | |
| `back_text` | TextField | |
| `is_premium` | BooleanField | default=False |
| `is_active` | BooleanField | default=True |
| `created_by` | ForeignKey → `auth.User` | CASCADE, related_name=created_flashcards |
| `created_at` | DateTimeField | auto_now_add |
| `tags` | ManyToManyField → `Tag` | through `core_flashcard_tags` |

**Indexes:** `created_by_id`, `topic_id`  
**Ordering:** `-created_at`

---

## 10. VideoResource (`core/models/resource_models.py`)

**Table:** `core_videoresource`

| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField PK | |
| `title` | CharField(200) | |
| `topic` | ForeignKey → `Topic` | CASCADE, related_name=videos |
| `description` | TextField | blank=True |
| `video_url` | URLField | |
| `duration_minutes` | PositiveIntegerField | default=0 |
| `thumbnail` | ImageField | upload_to=uploads/resources/thumbnails/, nullable |
| `is_premium` | BooleanField | default=False |
| `is_active` | BooleanField | default=True |
| `created_by` | ForeignKey → `auth.User` | CASCADE, related_name=created_videos |
| `created_at` | DateTimeField | auto_now_add |
| `tags` | ManyToManyField → `Tag` | through `core_videoresource_tags` |

**Indexes:** `created_by_id`, `topic_id`  
**Properties:** `duration_formatted`  
**Ordering:** `-created_at`

---

## 11. UserProgress (`core/models/resource_models.py`)

**Table:** `core_userprogress`

| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField PK | |
| `user` | ForeignKey → `auth.User` | CASCADE, related_name=progress |
| `topic` | ForeignKey → `Topic` | CASCADE, related_name=user_progress |
| `notes_read` | ManyToManyField → `Note` | through `core_userprogress_notes_read` |
| `flashcards_reviewed` | ManyToManyField → `Flashcard` | through `core_userprogress_flashcards_reviewed` |
| `videos_watched` | ManyToManyField → `VideoResource` | through `core_userprogress_videos_watched` |
| `total_quiz_attempts` | IntegerField | default=0 |
| `best_quiz_score` | IntegerField | default=0 |
| `total_time_spent_minutes` | IntegerField | default=0 |
| `last_accessed` | DateTimeField | auto_now |
| `created_at` | DateTimeField | auto_now_add |

**Constraints:** `unique_together = ['user', 'topic']`  
**Indexes:** `topic_id`, `user_id`  
**Properties:** `completion_percentage`  
**Ordering:** `-last_accessed`

---

## 12. SubscriptionPlan (`core/models/subscription_models.py`)

**Table:** `core_subscriptionplan`

| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField PK | |
| `name` | CharField(50) | |
| `plan_type` | CharField(15) | UNIQUE; Choices: free, monthly, quarterly, yearly |
| `price` | DecimalField(10,2) | |
| `duration_days` | IntegerField | |
| `features` | TextField | JSON or text description |
| `is_active` | BooleanField | default=True |
| `created_at` | DateTimeField | auto_now_add |

**Ordering:** `price`

---

## 13. PaymentProof (`core/models/subscription_models.py`)

**Table:** `core_paymentproof`

| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField PK | |
| `user` | ForeignKey → `auth.User` | CASCADE, related_name=payment_proofs |
| `subscription_plan` | ForeignKey → `SubscriptionPlan` | CASCADE |
| `payment_method` | CharField(20) | Choices: jazzcash, easypaisa, bank_transfer, other |
| `transaction_id` | CharField(100) | |
| `amount_paid` | DecimalField(10,2) | |
| `payment_screenshot` | ImageField | upload_to=uploads/payment_proofs/ |
| `status` | CharField(15) | Choices: **pending, approved, rejected, expired** |
| `admin_notes` | TextField | blank=True |
| `submitted_at` | DateTimeField | auto_now_add |
| `reviewed_at` | DateTimeField | null=True, blank=True |
| `reviewed_by` | ForeignKey → `auth.User` | SET_NULL, null/blank, related_name=reviewed_payments |

**Indexes:** `reviewed_by_id`, `user_id`, `subscription_plan_id`  
**Methods:** `approve_payment(admin_user)`, `reject_payment(admin_user, reason="")`  
**Ordering:** `-submitted_at`

---

## 14. Tag (`core/models/tag_models.py`)

**Table:** `core_tag`

| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField PK | |
| `name` | CharField(64) | UNIQUE |
| `description` | TextField | blank=True |
| `color` | CharField(7) | default='#0057A3' |
| `created_at` | DateTimeField | auto_now_add |
| `updated_at` | DateTimeField | auto_now |
| `is_active` | BooleanField | default=True |
| `apply_to_all_resources` | BooleanField | default=True |
| `apply_to_mcq` | BooleanField | default=False |
| `apply_to_videos` | BooleanField | default=False |
| `apply_to_notes` | BooleanField | default=False |

**Relationships:** Has many → `Subtag` (related_name: `subtags`); M2M to Question, Note, Flashcard, VideoResource, Topic, UserProfile  
**Methods:** `get_resource_count()` — **placeholder, returns 0**  
**Ordering:** `name`

---

## 15. Subtag (`core/models/tag_models.py`)

**Table:** `core_subtag`

| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField PK | |
| `tag` | ForeignKey → `Tag` | CASCADE, related_name=subtags |
| `name` | CharField(64) | |
| `description` | TextField | blank=True |
| `color` | CharField(7) | blank=True |
| `created_at` | DateTimeField | auto_now_add |
| `updated_at` | DateTimeField | auto_now |
| `is_active` | BooleanField | default=True |

**Constraints:** `unique_together = ['tag', 'name']`  
**Indexes:** `tag_id`  
**Properties:** `full_path`, `display_color`  
**Methods:** `get_resource_count()` — **placeholder, returns 0**  
**Ordering:** `name`

---

## M2M Through Tables Summary

| Through Table | From | To |
|--------------|------|----|
| `core_userprofile_tags` | UserProfile | Tag |
| `core_topic_tags` | Topic | Tag |
| `core_question_tags` | Question | Tag |
| `core_note_tags` | Note | Tag |
| `core_flashcard_tags` | Flashcard | Tag |
| `core_videoresource_tags` | VideoResource | Tag |
| `core_quizsession_questions` | QuizSession | Question |
| `core_userprogress_notes_read` | UserProgress | Note |
| `core_userprogress_flashcards_reviewed` | UserProgress | Flashcard |
| `core_userprogress_videos_watched` | UserProgress | VideoResource |
