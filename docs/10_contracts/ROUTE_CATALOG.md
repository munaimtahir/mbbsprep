# Route Catalog

This document records the most important active route categories and the expectations attached to them.

## Public / Student Route Categories

### Authentication
Typical expectations:
- signup route is public
- login route is public
- successful auth state should redirect into a valid dashboard or intended next step

### Dashboard
Expectation:
- authenticated users can access a dashboard without runtime failures

### Profile
Expectation:
- authenticated users can view and edit profile
- year-of-study values must align with current field choices

### Question Bank
Expectation:
- authenticated users can browse active question-bank content
- filtering/search behavior must not break route or queryset integrity

### Quiz
Expectation:
- start page renders
- quiz session/answer submission works
- result page resolves correctly

### Resources
Expectation:
- active categories such as notes/videos/flashcards should resolve through valid templates where active

### Subscription / Payment
Expectation:
- users can access payment-related pages in scope
- proof upload and payment status display should function coherently

## Staff Route Categories

### Staff Dashboard
Expectation:
- loads without broken counts or invalid filters

### Academic Content Management
Expectation:
- staff subject/topic/question pages in scope should remain coherent

### Payment Review / History
Expectation:
- staff users can load review/history screens
- payment branching logic remains consistent with status constants

### Bulk User Upload
Expectation:
- preview -> confirm -> import workflow remains coherent

### Support Placeholder
Expectation:
- placeholder pages may be limited, but must not crash
