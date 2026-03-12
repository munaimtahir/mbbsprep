# BROKEN_REFERENCES.md
## MedPrep — Broken References & Logic Errors

---

## 1. Invalid `year_of_study` Default in `ProfileView` and `ProfileEditView`

**File:** `core/views/auth_views.py`  
**Severity:** 🔴 Bug (silent data corruption)

`ProfileView.get_context_data()` creates a new `UserProfile` with:
```python
UserProfile.objects.create(user=user, year_of_study='1st', college_name='Not specified')
```

`ProfileEditView.get_object()` also uses:
```python
defaults={'year_of_study': '1st', 'college_name': 'Not specified'}
```

**Problem:** The valid `YEAR_CHOICES` for `year_of_study` are:
`'1st_year'`, `'2nd_year'`, `'3rd_year'`, `'4th_year'`, `'final_year'`, `'graduate'`

`'1st'` is not a valid choice — it will save an invalid value to the database and break any template display that relies on `get_year_of_study_display()`.

**Fix:** Change `'1st'` to `'1st_year'` in both locations.

---

## 2. Incorrect M2M Reverse Lookup in `QuizQuestionView`

**File:** `core/views/quiz_views.py`  
**Severity:** 🔴 Bug (500 error at runtime)

```python
question = get_object_or_404(
    Question,
    pk=question_id,
    quizsession=quiz_session   # ← WRONG
)
```

The `QuizSession.questions` field is a `ManyToManyField` to `Question` with `related_name='quiz_sessions'`. The correct reverse lookup is:

```python
question = get_object_or_404(
    Question,
    pk=question_id,
    quiz_sessions=quiz_session  # ← CORRECT
)
```

Django will raise a `FieldError: Cannot resolve keyword 'quizsession' into field` at runtime.

**Fix:** Change `quizsession=quiz_session` to `quiz_sessions=quiz_session`.

---

## 3. Invalid `PaymentProof.status` Value in `DashboardView`

**File:** `staff/views/dashboard_views.py`  
**Severity:** 🟡 Warning (query returns wrong count)

```python
pending_payments = PaymentProof.objects.filter(
    Q(status='pending') | Q(status='submitted')
).count()
```

**Problem:** `PaymentProof.STATUS_CHOICES` does NOT include `'submitted'`. Valid values are:
`'pending'`, `'approved'`, `'rejected'`, `'expired'`

The `Q(status='submitted')` clause matches nothing and silently produces an incorrect count.

**Fix:** Remove `Q(status='submitted')` or replace with a valid status if the intent was different.

---

## 4. `Tag.get_resource_count()` and `Subtag.get_resource_count()` Are Placeholders

**File:** `core/models/tag_models.py`  
**Severity:** 🟡 Warning (incomplete feature)

Both methods contain a comment placeholder and always return `0`:
```python
def get_resource_count(self):
    """Returns the count of resources associated with this tag"""
    # This is a placeholder - implement based on actual relationships
    return 0
```

Despite the `Tag` model having M2M relationships to `Question`, `Note`, `Flashcard`, `VideoResource`, `Topic`, and `UserProfile`, neither `get_resource_count()` method aggregates across them.

**Fix:** Implement proper cross-relation counts using `annotate()` or summing related querysets.

---

## 5. `ResourceListView` Returns `None` Queryset

**File:** `staff/views/resource_views.py`  
**Severity:** 🟡 Warning (broken aggregate resource view)

```python
class ResourceListView(StaffRequiredMixin, ListView):
    template_name = 'staff/resources/resource_list.html'

    def get_queryset(self):
        return None  # Will be implemented with combined resources
```

Returning `None` from `get_queryset()` on a `ListView` will raise a `TypeError` at runtime when Django's `ListView` attempts to paginate or iterate the queryset.

**Fix:** Return an empty queryset (e.g., `Note.objects.none()`) or implement a combined aggregate.

---

## 6. `SupportInboxView` and `SupportMessageView` Are Stubs Without Models

**File:** `staff/views/support_views.py`  
**Severity:** 🟡 Warning (routes are broken)

```python
class SupportInboxView(StaffRequiredMixin, ListView):
    template_name = 'staff/support/inbox.html'
    context_object_name = 'messages'
    paginate_by = 25

    def get_queryset(self):
        return []  # Will be implemented when contact model is available

class SupportMessageView(StaffRequiredMixin, DetailView):
    template_name = 'staff/support/message_detail.html'
    context_object_name = 'message'
```

- **Templates don't exist** (`staff/support/inbox.html`, `staff/support/message_detail.html`)
- `SupportMessageView` has no `model` or `get_object()` — will 500 on access
- `SupportInboxView` returns `[]` which breaks Django's `ListView` pagination (needs a queryset, not a list)

**Fix:** Either create a `ContactMessage` model + templates and wire them up, or mark these routes 404 until implemented.

---

## 7. `results` URL Duplicate / Misrouted

**File:** `core/urls.py`  
**Severity:** 🟠 Medium (usability bug)

```python
path('results/', views.QuizResultView.as_view(), name='results'),
```

`QuizResultView` is a `DetailView` expecting a `pk` kwarg:
```python
class QuizResultView(LoginRequiredMixin, DetailView):
    model = QuizSession
    ...
    def get_queryset(self):
        return QuizSession.objects.filter(user=self.request.user)
```

Calling `/results/` without a `pk` will trigger a `AttributeError` or 404 since `DetailView.get_object()` requires `pk` or `slug`. This URL only works if called as `/quiz/result/<pk>/` which has its own named route `quiz_result`.

**Fix:** Remove the `/results/` route, or map it to a different list/summary view.

---

## 8. `core/models.py` Root File vs `core/models/__init__.py` Package

**File:** `core/models.py`  
**Severity:** 🟡 Warning (confusing dual definition)

Both `core/models.py` (a stale file) and `core/models/__init__.py` (the active package) exist.  
Python resolves the package (`core/models/`) over the module file (`core/models.py`) so functionally `models.py` is never loaded, but its existence can mislead developers into editing the wrong file.

**Fix:** Delete `core/models.py` to eliminate confusion.

---

## 9. `core/views.py` Root File vs `core/views/__init__.py` Package

**File:** `core/views.py`  
**Severity:** 🟡 Warning (same as above — dual definition)

Same issue: both `core/views.py` (stale) and `core/views/` (active package) exist. The package wins. The root file is dead code.

**Fix:** Delete `core/views.py`.

---

## 10. `staff/forms.py` Root File vs `staff/forms/` Package

**File:** `staff/forms.py`  
**Severity:** 🟡 Warning (stale artifact per AGENTS.md)

Both `staff/forms.py` (stale) and `staff/forms/` (active package) exist. The package is used by views. The root file is a stale duplicate.

**Fix:** Delete `staff/forms.py` after verifying nothing imports from it directly.

---

## 11. `UserProfile.year_of_study` Default Choices Mismatch in Academic Models

**File:** `core/models/academic_models.py` (`Subject.year_applicable`)  
**Severity:** ℹ️ Info (inconsistency)

`Subject.year_applicable` choices are: `'1st'`, `'2nd'`, `'3rd'`, `'4th'`, `'5th'`, `'all'`  
`UserProfile.year_of_study` choices are: `'1st_year'`, `'2nd_year'`, etc.

These two representations are inconsistent and any code trying to match them will need explicit mapping.

---

## Summary Table

| # | Location | Issue | Severity |
|---|----------|-------|----------|
| 1 | `auth_views.py` | Invalid `year_of_study='1st'` default | 🔴 Bug |
| 2 | `quiz_views.py` | `quizsession=quiz_session` reverse M2M lookup crash | 🔴 Bug |
| 3 | `dashboard_views.py` | Invalid `status='submitted'` filter | 🟡 Warning |
| 4 | `tag_models.py` | `get_resource_count()` placeholder returns 0 | 🟡 Warning |
| 5 | `resource_views.py` | `ResourceListView` returns `None` | 🟡 Warning |
| 6 | `support_views.py` | Stub views with no model/templates | 🟡 Warning |
| 7 | `core/urls.py` | `/results/` missing pk — DetailView will 500 | 🟠 Medium |
| 8 | `core/models.py` | Stale root file shadowed by package | 🟡 Warning |
| 9 | `core/views.py` | Stale root file shadowed by package | 🟡 Warning |
| 10 | `staff/forms.py` | Stale root file shadowed by package | 🟡 Warning |
| 11 | `academic_models.py` | year_applicable vs year_of_study inconsistency | ℹ️ Info |
