from app.utils.similarity import cosine_similarity


def test_cosine_similarity_same_vectors() -> None:
    assert cosine_similarity([1.0, 0.0], [1.0, 0.0]) == 1.0


def test_cosine_similarity_opposite_vectors() -> None:
    assert cosine_similarity([1.0, 0.0], [-1.0, 0.0]) == -1.0


def test_zero_vector_safe() -> None:
    assert cosine_similarity([0.0, 0.0], [1.0, 1.0]) == 0.0
