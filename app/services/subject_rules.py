from __future__ import annotations


SUBJECT_GROUPS = {
    "fox": {"fox", "red fox", "vulpes vulpes"},
    "wolf": {"wolf", "gray wolf", "timber wolf"},
    "dog": {"dog", "domestic dog", "canis familiaris"},
    "bear": {"bear", "grizzly bear", "black bear"},
    "deer": {"deer", "white-tailed deer", "roe deer"},
}


def canonicalize_subject(value: str | None) -> str:
    if not value:
        return ""
    value = value.strip().lower()
    for canonical, variants in SUBJECT_GROUPS.items():
        if value in variants:
            return canonical
    return value


def subjects_compatible(expected: str | None, actual: str | None) -> bool:
    expected_group = canonicalize_subject(expected)
    actual_group = canonicalize_subject(actual)
    if not expected_group or not actual_group:
        return False
    return expected_group == actual_group
