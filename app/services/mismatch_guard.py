from __future__ import annotations

from app.core.config import get_settings
from app.services.subject_rules import subjects_compatible


class GuardDecision:
    def __init__(self, accepted: bool, reason_code: str | None = None, reason: str | None = None, similarity: float | None = None, confidence: float | None = None):
        self.accepted = accepted
        self.reason_code = reason_code
        self.reason = reason
        self.similarity = similarity
        self.confidence = confidence

    def to_dict(self) -> dict[str, object]:
        return {
            "accepted": self.accepted,
            "reason_code": self.reason_code,
            "reason": self.reason,
            "similarity": self.similarity,
            "confidence": self.confidence,
        }


class MismatchGuard:
    def __init__(self, settings=None):
        self.settings = settings or get_settings()

    def evaluate(self, *, expected_subject: str | None, actual_subject: str | None, similarity: float, confidence: float | None) -> GuardDecision:
        if not subjects_compatible(expected_subject, actual_subject):
            return GuardDecision(
                accepted=False,
                reason_code="SUBJECT_MISMATCH",
                reason=f"Expected {expected_subject or 'related'} content but detected {actual_subject or 'an unrelated subject'}.",
                similarity=similarity,
                confidence=confidence,
            )

        if similarity < self.settings.match_similarity_threshold:
            return GuardDecision(
                accepted=False,
                reason_code="SIMILARITY_TOO_LOW",
                reason=f"Semantic similarity {similarity:.3f} is below the configured threshold of {self.settings.match_similarity_threshold:.3f}.",
                similarity=similarity,
                confidence=confidence,
            )

        if confidence is None or confidence < self.settings.vision_confidence_threshold:
            return GuardDecision(
                accepted=False,
                reason_code="LOW_CONFIDENCE",
                reason=f"Vision confidence {confidence if confidence is not None else 'missing'} is below the required threshold of {self.settings.vision_confidence_threshold:.3f}.",
                similarity=similarity,
                confidence=confidence,
            )

        return GuardDecision(
            accepted=True,
            reason_code="OK",
            reason="Candidate passes subject compatibility, similarity, and confidence checks.",
            similarity=similarity,
            confidence=confidence,
        )
