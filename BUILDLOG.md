# Build log

## Milestone 1: repository setup and architecture
- Confirmed the repo was effectively empty apart from the project skeleton.
- Established the Python package layout and configuration management.
- Set up the FastAPI application entrypoint and health endpoint.

## Milestone 2: database and schema foundation
- Created the SQLAlchemy models for images, posts, suggestions, reviews, jobs, and AI usage.
- Added Alembic migration support.
- Validated the database setup with PostgreSQL in Docker.

## Milestone 3: AI safety and validation
- Added strict structured vision metadata validation.
- Implemented confidence thresholding logic.
- Added semantic similarity utilities.
- Implemented subject compatibility and mismatch guard logic.

## Milestone 4: worker and API layer
- Implemented the batch image-processing worker.
- Added API routes for posts, suggestions, jobs, and cost summary.
- Added review endpoints for approval and rejection flows.

## Milestone 5: verification and documentation
- Reproduced the stale database-port issue caused by an old environment variable.
- Fixed the config to normalize stale localhost:5432 values to the active Docker port 5433.
- Verified the project passes the unit suite in a live PostgreSQL-backed environment.
- Wrote the final repository documentation.
