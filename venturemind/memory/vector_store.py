"""Chroma vector store wrapper for VentureMind."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any
from uuid import uuid4

import chromadb


@dataclass
class VectorStore:
    """Manage persistence and similarity search in Chroma."""

    persist_path: str
    collection_name: str = "venturemind"
    _client: chromadb.PersistentClient = field(init=False, repr=False)
    _collection: chromadb.api.models.Collection.Collection = field(
        init=False, repr=False
    )

    def __post_init__(self) -> None:
        self._client = chromadb.PersistentClient(path=self.persist_path)
        self._collection = self._client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_documents(
        self, documents: List[str], metadatas: List[Dict[str, Any]] | None = None
    ) -> None:
        """Store documents alongside metadata for later retrieval."""

        if not documents:
            return

        metadatas = metadatas or [{} for _ in documents]
        ids = [str(uuid4()) for _ in documents]
        self._collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
        )

    def similarity_search(self, query: str, k: int = 4) -> List[Dict[str, Any]]:
        """Retrieve the closest matching documents for a query."""

        if not query:
            return []

        results = self._collection.query(query_texts=[query], n_results=k)
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        scores = results.get("distances", [[]])[0]

        payload: List[Dict[str, Any]] = []
        for content, metadata, score in zip(documents, metadatas, scores):
            payload.append(
                {
                    "content": content,
                    "metadata": metadata,
                    "score": score,
                }
            )
        return payload
