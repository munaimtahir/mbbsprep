# Model Contracts

This document records the practical assumptions around major active data entities.

## UserProfile

### Purpose
Stores extended user-facing profile information beyond the base user record.

### Key Assumptions
- each active user should have one coherent profile
- year-of-study values must match the current allowed set
- profile edit workflows must not write invalid choice values

## Subject

### Purpose
Represents a primary academic classification level used to group content.

### Key Assumptions
- subject names should remain meaningful
- subject CRUD is part of staff operational stability

## Topic

### Purpose
Represents content groupings inside a subject.

### Key Assumptions
- topics belong coherently to subjects
- topic management should preserve taxonomy consistency

## Question / MCQ Entity

### Purpose
Stores quizable academic items.

### Key Assumptions
- question records must align with the quiz/session logic currently in use
- import utilities must reference the correct option/question structures
- quiz flow must not rely on stale relation names or invalid M2M assumptions

## Resource Entity

### Purpose
Represents educational content such as notes, videos, or flashcards where active.

### Key Assumptions
- public-facing resource routes depend on valid templates and coherent query logic
- staff aggregation/views must not crash due to missing helper logic

## Payment Submission / Payment Review Entity

### Purpose
Stores user payment proof and review state.

### Key Assumptions
- status values must be consistent across model, view, form, and template layers
- staff review branching must support approve/reject/pending semantics correctly
