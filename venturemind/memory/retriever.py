"""Retriever utilities built on top of the vector store."""
from __future__ import annotations

from typing import List, Dict, Any

from .vector_store import VectorStore


class Retriever:
    """Convenience wrapper around vector similarity queries."""

    def __init__(self, store: VectorStore, top_k: int = 4) -> None:
        self.store = store
        self.top_k = top_k

    def retrieve(self, query: str) -> List[Dict[str, Any]]:
        """Return the most relevant documents for a query."""

        return self.store.similarity_search(query=query, k=self.top_k)
