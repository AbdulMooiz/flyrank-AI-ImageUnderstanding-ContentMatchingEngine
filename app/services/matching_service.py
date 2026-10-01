from __future__ import annotations

from app.core.config import get_settings
from app.services.mismatch_guard import MismatchGuard
from app.utils.similarity import cosine_similarity


class MatchingService:
    def __init__(self, settings=None, guard=None):
        self.settings = settings or get_settings()
        self.guard = guard or MismatchGuard(self.settings)

    def rank_candidates(self, post_vector: list[float], image_vectors: list[tuple[int, list[float], str, float | None]]) -> list[dict]:
        scored = []
        for image_id, vector, subject, confidence in image_vectors:
            score = cosine_similarity(post_vector, vector)
            scored.append({
                "image_id": image_id,
                "subject": subject,
                "similarity": score,
                "confidence": confidence,
            })

        scored.sort(key=lambda item: item["similarity"], reverse=True)
        return scored

    def build_suggestions(self, post_subject: str, post_vector: list[float], image_candidates: list[tuple[int, list[float], str, float | None]]) -> list[dict]:
        ranked = self.rank_candidates(post_vector, image_candidates)
        suggestions = []
        for rank, candidate in enumerate(ranked, start=1):
            decision = self.guard.evaluate(
                expected_subject=post_subject,
                actual_subject=candidate["subject"],
                similarity=float(candidate["similarity"]),
                confidence=candidate["confidence"],
            )
            suggestions.append({
                "image_id": candidate["image_id"],
                "similarity": candidate["similarity"],
                "rank": rank,
                "guard_decision": decision.accepted,
                "guard_reason": decision.reason,
                "guard_reason_code": decision.reason_code,
                "confidence": candidate["confidence"],
            })
        return suggestions
