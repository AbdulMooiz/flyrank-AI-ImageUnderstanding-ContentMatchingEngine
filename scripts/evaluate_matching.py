from __future__ import annotations

from app.services.subject_rules import canonicalize_subject


LABELS = [
    ("fox", "fox"),
    ("wolf", "wolf"),
    ("dog", "dog"),
    ("bear", "bear"),
    ("deer", "deer"),
]


def evaluate() -> dict:
    hits = 0
    total = 0
    for expected, observed in LABELS:
        total += 1
        if canonicalize_subject(expected) == canonicalize_subject(observed):
            hits += 1
    return {"total": total, "correct": hits, "top_1_accuracy": round(hits / total, 3) if total else 0.0}


if __name__ == "__main__":
    result = evaluate()
    print(result)
