from __future__ import annotations


def confidence_is_acceptable(confidence: float | None, threshold: float | None) -> bool:
    if confidence is None or threshold is None:
        return False
    if not isinstance(confidence, (int, float)) or not isinstance(threshold, (int, float)):
        return False
    if confidence < 0 or threshold < 0:
        return False
    return float(confidence) >= float(threshold)


def normalize_confidence(value: object) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
