# Integration Gap Register

Date: 2026-03-14  
Basis: Static code+template+route audit and `tests/automated` coverage mapping.

| ID | Area | Flow | Gap description | Type | Severity | Recommended action | Suggested phase |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GAP-001 | Public content | Topic detail (`core:topic_detail`) | Template references missing routes/context (`core:add_comment`, `core:bookmark_topic`, `question_stats`, `related_topics`, etc.) | stale route | critical | Align template to actual view contract or implement missing endpoints explicitly | Phase 1 |
| GAP-002 | Public support | Contact form (`core:contact`) | UI intercepts submit and simulates success; backend `ContactForm` contract is bypassed and mismatched | frontend fake placeholder | critical | Either wire frontend to backend form contract or mark page explicitly as non-submitting placeholder | Phase 1 |
| GAP-003 | Public resources | Resources hub JS | `resources.js` calls non-existent endpoints (`/resources/bookmark/...`, tracking/recommendations/download APIs) | stale route | major | Remove/replace dead JS endpoint calls with implemented URLs | Phase 1 |
| GAP-004 | Public leaderboard | Leaderboard JS | `leaderboard.js` calls non-existent `/leaderboard/filter|subject|time-range|refresh/` APIs | stale route | major | Keep leaderboard server-rendered or add matching backend endpoints; avoid dead AJAX calls | Phase 2 |
| GAP-005 | Staff questions | Bulk question upload | Upload code sets `Option.option_label` but model has no `option_label` field | stale field | critical | Fix mapping to existing `Option` schema and add automated test for bulk question upload | Phase 1 |
| GAP-006 | Staff quizzes | Quiz attempts page | `templates/staff/quizzes/quiz_list.html` contains malformed duplicated template content | broken by drift | major | Repair template and add route/render test | Phase 1 |
| GAP-007 | Public subject detail | Subject quick action | `subject_detail.html` builds quiz URL from `topics.first.pk`; subjects with zero topics can break rendering | incomplete POST / stale assumption | major | Guard quick-start action when no topics exist | Phase 1 |
| GAP-008 | Public quiz center | Quick start quiz form | Quick start now posts to canonical `core:quiz` and server-side form handling gracefully covers missing/invalid topic input | repaired route contract | resolved | Keep `QuizListView.post` and template action aligned with `QuizSettingsForm` contract | Completed (Phase 1) |
| GAP-009 | Staff user export | CSV export logic | Export uses `quiz_sessions.filter(completed=True)` despite status-driven model; single-user fields leak into multi-user export branch | broken by drift | major | Correct export query/branching and add automated export assertions | Phase 1 |
| GAP-010 | Staff subject/topic APIs | AJAX management endpoints | Multiple active AJAX mutators are `@csrf_exempt` despite CSRF token usage in frontend | missing permissions handling | major | Re-enable CSRF protection on authenticated mutating endpoints | Phase 2 |
| GAP-011 | Public contact page | Help Center CTA | Hardcoded `/help/` link has no URL route | unreachable page | moderate | Replace link with a real route or remove CTA | Phase 2 |
| GAP-012 | Public quiz assets | Legacy quiz JS | Legacy `static/core/js/quiz.js` retired from active source; quiz runtime templates do not include it | stale asset retired | resolved | Keep quiz runtime server-driven and avoid reintroducing dead save APIs | Completed (Phase 1) |
| GAP-013 | Coverage | Multiple active flows | No automated behavior tests for topic detail, leaderboard behavior, contact POST path, staff quiz pages, settings/logs | missing tests | major | Add targeted integration tests for active/visible flows and known drift points | Phase 2 |
| GAP-014 | Staff tags | Legacy form routes | Canonicalized to `staff:tag_list` + AJAX endpoints; duplicate alias and legacy form route names retired | ambiguous navigation removed | resolved | Keep tag UI bound to canonical AJAX route names only | Completed (Phase 1) |
| GAP-015 | Staff support | Support/contact surfaces | Public/support messaging tightened to match runtime truth; staff support remains explicit placeholder by design | placeholder truth contract | resolved | Preserve truthful placeholder copy until a real support model is intentionally introduced | Completed (Phase 1) |

## Repair Status Update (2026-03-14)

### Resolved in this integration repair pass

- `GAP-001` Topic detail drift fixed by aligning template with active `TopicDetailView` context and routes.
- `GAP-002` Contact flow unified to backend `ContactForm` contract; fake submit path removed.
- `GAP-003` Resources dead AJAX assumptions removed from active runtime template.
- `GAP-004` Leaderboard dead AJAX assumptions removed from active runtime template.
- `GAP-005` Bulk question upload schema drift fixed (`Option` mapping aligned to `option_text` + `order` + `is_correct`).
- `GAP-006` Staff quiz attempts template repaired as truthful placeholder.
- `GAP-007` Subject detail quick-start guarded for zero-topic subjects.
- `GAP-009` User export single/multi branching and completion query logic corrected to status-based filtering.
- `GAP-010` CSRF exemptions removed from active subject/topic mutating AJAX endpoints.
- `GAP-011` Dead `/help/` contact link removed from active contact UI.
- `GAP-013` Targeted integration tests added for repaired visible flows.

### Deferred (still open)

- No open deferred items from the current GAP register set after the Phase 1 stabilization pass.

## Top Priority Risk Order (implementation-focused)

1. `GAP-001` topic detail drift
2. `GAP-002` contact fake submission path
3. `GAP-005` staff question bulk upload model mismatch
4. `GAP-006` staff quiz attempts malformed template
5. `GAP-009` user export logic drift
6. `GAP-003` resources dead JS endpoints
7. `GAP-004` leaderboard dead JS endpoints
8. `GAP-007` subject quick-start zero-topic break risk
9. `GAP-010` CSRF exemptions on authenticated mutators
10. `GAP-013` missing targeted tests in visible flows
