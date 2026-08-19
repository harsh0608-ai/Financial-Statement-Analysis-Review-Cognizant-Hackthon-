from __future__ import annotations

from functools import lru_cache

from config import EMBEDDING_MODEL


class LocalEmbedder:
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self.model_name = model_name
        self._model = None

    def _load(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def encode(self, texts: list[str]) -> list[list[float]]:
        model = self._load()
        vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        return vectors.tolist()

    def dimension(self) -> int:
        return int(self._load().get_sentence_embedding_dimension())
