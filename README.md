# AI Image Understanding and Content Matching Engine

A backend system for matching image content to blog or article text using AI-driven image understanding, structured validation, semantic embeddings, and explicit trust checks.

## What this project does

The engine can:

- ingest or seed an image corpus
- analyze images with a vision provider
- validate model output against a strict metadata schema
- reject low-confidence or semantically incompatible matches
- create embeddings for posts and image-derived metadata
- rank candidate matches by semantic similarity
- track background processing jobs and job progress
- support review decisions on accepted or rejected suggestions
- evaluate matching quality with a labeled dataset

The core principle is safety-first matching: the system does not accept a match just because a model output looks plausible. It checks confidence, compatibility, and similarity before accepting a recommendation.

## Architecture

- FastAPI application layer
- SQLAlchemy + PostgreSQL persistence
- Alembic migrations
- provider abstractions for vision and embeddings
- safety guard for subject mismatch and low-confidence cases
- background image-processing workers
- review flow for suggestion approvals or rejections
- evaluation script for repeatable scoring

## Stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pydantic / pydantic-settings
- Pytest
- Docker Compose

## Quick start

1. Create a virtual environment and install dependencies:

   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -U pip
   python -m pip install -e .

2. Start the Postgres container:

   docker compose up -d db

3. Apply database migrations:

   python -m alembic upgrade head

4. Seed example data:

   python -m scripts.seed_data

5. Run the app:

   uvicorn app.main:app --host 0.0.0.0 --port 8000

## Important configuration note

The project expects PostgreSQL on localhost:5433 in local development because the Docker Compose setup maps that host port. The runtime config sanitizes stale localhost:5432 values automatically so older local environment variables do not break startup.

## Endpoints

- GET /health
- GET /posts
- GET /posts/{post_id}
- POST /posts
- GET /posts/{post_id}/images
- GET /jobs
- GET /jobs/{job_id}
- POST /jobs/run
- POST /jobs/images/process
- GET /suggestions
- POST /suggestions/{suggestion_id}/approve
- POST /suggestions/{suggestion_id}/reject
- GET /costs

## Validation and evaluation

Run the project checks:

- python -m pytest tests/unit/test_vision_schema.py tests/unit/test_thresholds.py tests/unit/test_similarity.py tests/unit/test_guard.py tests/unit/test_batch_job.py -q

Run the evaluation script:

- python -m scripts.evaluate_matching

## Production-minded notes

This implementation is intentionally conservative:

- every vision payload is validated
- confidence thresholds are enforced
- mismatched subjects are rejected before a suggestion is accepted
- the job layer tracks progress and failure state separately
- the system avoids blindly trusting AI output

The project is designed as a backend engine rather than a full frontend product; its goal is correctness, auditability, and repeatable evaluation.

## Repository status

The project has reached a verified working state for the implemented backend and matching logic with the supporting documentation included in the repository.
