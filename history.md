# History

## v0.1.0 - 2025-09-29

### Added

- Initial project structure with FastAPI.
- Core modules: `core`, `db`, `models`, `schemas`, `routers`, `services`, `tests`.
- User entity with CRUD operations (`/users`).
- Spot entity with CRUD operations (`/spots`).
- SQLite database integration with SQLAlchemy.
- Pydantic models for data validation and serialization.
- Basic service layer to separate business logic.
- Configurable logging with 5 levels.
- Pytest setup with unit and integration tests.
- Simple Leaflet.js frontend to display and create spots.
- `README.md` with full setup and usage instructions.
- `.env` file for configuration.
- User deletion functionality (soft delete).
- User permission levels (admin, user, pending validation).
- Admin approval for new user creation.
- The first user created is now automatically an admin.
- Implemented authentication and authorization using JWT tokens.
- Added a login endpoint to generate access tokens.
- Protected admin-only endpoints with an admin check.

### Other

- Provided guidance on diagnosing 'resource exhausted' errors, including checking system resources, application logs, code inspection for memory leaks, unclosed database connections, file handles, and using profilers.