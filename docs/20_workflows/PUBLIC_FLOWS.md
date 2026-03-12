# Public Flows

## Authentication Flow

### Stable expectation
- signup page renders
- login page renders
- valid authentication transitions into an authenticated state
- logout exits that state cleanly

## Dashboard Flow

### Stable expectation
- dashboard loads without template/runtime failure

## Profile Flow

### Stable expectation
- profile view loads
- profile edit page loads
- valid updates are accepted and persisted

## Question Bank Flow

### Stable expectation
- question bank loads without route failure
- filtering/searching in current scope behaves coherently

## Quiz Flow

### Stable expectation
1. start page renders
2. active quiz/session page renders
3. answers can be submitted
4. result page resolves correctly

## Resources Flow

### Stable expectation
- active resource category pages resolve to valid templates
- detail pages render where the feature is active

## Subscription / Payment Flow

### Stable expectation
- user can view payment instructions or relevant subscription page
- user can submit payment proof where enabled
- user can view payment review status
