# Design

## Problem

A backend needs to match blog content to relevant images while refusing low-confidence or semantically wrong matches.

## Scope

This project focuses on a small, explainable backend system with image ingestion, vision classification, embeddings, semantic ranking, mismatch guarding, background processing, review workflow, and evaluation.

## Data model

Core entities include images, image metadata, image embeddings, posts, post embeddings, suggestions, reviews, AI usage records, and processing jobs.

## API surface

The system exposes health checks, post creation and retrieval, post-to-image matching, suggestion approval/rejection, job status, and cost reporting.

## Layer architecture

The implementation separates HTTP routes, services, database access, AI provider integrations, background jobs, and evaluation logic.

## AI provider design

Vision and embedding providers are isolated behind interfaces so Gemini can be replaced with a local Ollama adapter later without changing the business rules.

## Matching strategy

Candidates are retrieved by embedding similarity, then ranked and filtered by mismatch guard logic.

## Background processing

Batch processing runs asynchronously, tracks job status, retries transient provider failures, and avoids reprocessing successful images.

## Evaluation approach

The project includes a labeled evaluation dataset and a script that computes top-1 precision for the matching engine.

## Explicit non-goal

This is not a large-scale multi-service system, nor is it a frontend-driven product. It is a focused backend system designed for correctness, reliability, and evaluation quality.
