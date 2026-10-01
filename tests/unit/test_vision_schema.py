import pytest

from app.schemas.vision import VisionMetadata


def test_valid_vision_metadata() -> None:
    payload = {
        "subject": "red fox",
        "category": "animal",
        "attributes": ["orange fur", "wild", "forest"],
        "caption": "A red fox standing in a forest",
        "confidence": 0.94,
    }

    parsed = VisionMetadata.model_validate(payload)
    assert parsed.subject == "red fox"
    assert parsed.confidence == 0.94


def test_invalid_confidence() -> None:
    with pytest.raises(ValueError):
        VisionMetadata.model_validate({
            "subject": "wolf",
            "category": "animal",
            "attributes": ["wild"],
            "caption": "A wolf in a forest",
            "confidence": 1.5,
        })


def test_missing_confidence() -> None:
    with pytest.raises(ValueError):
        VisionMetadata.model_validate({
            "subject": "wolf",
            "category": "animal",
            "attributes": ["wild"],
            "caption": "A wolf in a forest",
        })


def test_invalid_payload_rejected() -> None:
    with pytest.raises(ValueError):
        VisionMetadata.model_validate({"subject": "fox"})
