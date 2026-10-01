from app.services.mismatch_guard import MismatchGuard


def test_guard_accepts_matching_subject() -> None:
    guard = MismatchGuard()
    result = guard.evaluate(expected_subject="fox", actual_subject="red fox", similarity=0.8, confidence=0.9)
    assert result.accepted is True


def test_guard_rejects_subject_mismatch() -> None:
    guard = MismatchGuard()
    result = guard.evaluate(expected_subject="fox", actual_subject="wolf", similarity=0.9, confidence=0.95)
    assert result.accepted is False
    assert result.reason_code == "SUBJECT_MISMATCH"


def test_guard_rejects_low_similarity() -> None:
    guard = MismatchGuard()
    result = guard.evaluate(expected_subject="fox", actual_subject="red fox", similarity=0.1, confidence=0.9)
    assert result.accepted is False
    assert result.reason_code == "SIMILARITY_TOO_LOW"


def test_guard_rejects_low_confidence() -> None:
    guard = MismatchGuard()
    result = guard.evaluate(expected_subject="fox", actual_subject="red fox", similarity=0.8, confidence=0.1)
    assert result.accepted is False
    assert result.reason_code == "LOW_CONFIDENCE"
