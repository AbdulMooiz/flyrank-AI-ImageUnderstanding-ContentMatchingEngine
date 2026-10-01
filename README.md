# AI Image Understanding and Content Matching Engine

This repository contains a backend system for image understanding, semantic matching, and trust-aware recommendation.

## Purpose

The objective is to build an AI-backed image matching system that can:

- ingest an image corpus
- classify images with a vision model
- validate structured outputs with Pydantic
- embed descriptions and blog posts into a shared semantic space
- retrieve and rank candidate images for a post
- reject unsafe or low-quality matches with a human-readable explanation
- provide review and evaluation workflows

The central design principle is that the application should not blindly trust the model. The model is treated as an input source, and the backend applies validation, thresholds, and a mismatch guard before accepting a suggestion.

## Planned architecture

- FastAPI application layer
- SQLAlchemy models and Alembic migrations
- provider abstractions for vision and embeddings
- background processing for image jobs
- semantic similarity ranking with explicit guard logic
- review workflow and evaluation pipeline

## Technology stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Pytest
- HTTPX
- Docker and Docker Compose

## Repository status

This repository is in active implementation. The initial design and project scaffolding are in place, and the system will be completed in the planned phases.

## Next steps

The project will be built in milestone commits and then verified with the project tests and evaluation script.
