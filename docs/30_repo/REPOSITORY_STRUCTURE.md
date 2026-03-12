# Repository Structure

## High-Level Layout

### Application code
The repository contains Django app code that is primarily divided between:

- `core` for student/public functionality
- `staff` for internal administrative functionality

### Templates
Templates are organized by feature ownership and app responsibility.

### Tests
Automated tests live under a dedicated tests area and currently focus on critical route and workflow protection.

### Docs
The `docs/` tree now serves as the governance and technical documentation center for the repository.

## Repository Principle

This repository should now be read as:

- **code = runtime truth**
- **docs = governance + shared understanding**
- **archive = historical context, not current authority**
