# Form-Flow Contracts

This document records major active form/view/template chains that should remain coherent.

## Authentication Forms

### Signup
Expected chain:
- route loads signup view
- form validates user creation inputs
- successful submission creates user/account state as designed

### Login
Expected chain:
- route loads login view
- valid credentials enter authenticated flow
- invalid credentials fail gracefully

## Profile Forms

### Profile edit
Expected chain:
- authenticated user opens profile edit page
- current values render correctly
- posted values validate against model choices
- valid submission persists

Critical contract:
- year-of-study handling must remain aligned with model constraints

## Quiz Forms / Submission Flow

Expected chain:
- quiz start page renders
- quiz session accepts answer submission
- submission processes without stale relation lookups
- result endpoint resolves correctly

## Payment Forms

### Payment proof submission
Expected chain:
- payment/proof page renders
- form accepts allowed evidence/data
- submission stores proof state coherently
- user can later see status

## Staff Review Forms

### Payment review branching
Expected chain:
- authorized staff user opens payment review screen
- action can mark approve/reject/pending as implemented

## Staff User Creation

Expected chain:
- `staff:user_create` renders the add-user form
- the form owns password, role, profile, and premium-access validation
- a valid submission creates the Django user plus `UserProfile` in one coherent save path
- `user_role` maps to Django staff/superuser flags without view-only hidden assumptions

## Bulk User Upload Forms

Expected chain:
- upload form accepts a valid file
- preview step renders safely
- confirmation step preserves necessary upload state
- import step completes and routes correctly
