from app.utils.thresholds import confidence_is_acceptable, normalize_confidence


def test_high_confidence() -> None:
    assert confidence_is_acceptable(0.95, 0.72) is True


def test_low_confidence() -> None:
    assert confidence_is_acceptable(0.5, 0.72) is False


def test_exact_threshold() -> None:
    assert confidence_is_acceptable(0.72, 0.72) is True


def test_invalid_confidence() -> None:
    assert confidence_is_acceptable(None, 0.72) is False


def test_normalize_confidence() -> None:
    assert normalize_confidence("0.81") == 0.81
