import math


class FakeEmbeddingProvider:
    async def embed_text(self, text: str) -> list[float]:
        vector = [0.0] * 8
        words = text.lower().split()
        for idx, token in enumerate(sorted(set(words))):
            if idx >= 8:
                break
            vector[idx] = 1.0 if token in {"fox", "red", "forest", "wild", "wolf", "dog", "bear", "deer"} else 0.3
        return vector
