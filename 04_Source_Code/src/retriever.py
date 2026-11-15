import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from src.config import EMBEDDING_MODEL, CHROMA_PATH, RETRIEVAL_TOP_K


class DocumentRetriever:
    def __init__(
        self,
        docs_path: str = "data/documentation.json",
        persist_directory: str = CHROMA_PATH,
        collection_name: str = "cloudserve_docs",
        embedding_model_name: str = EMBEDDING_MODEL,
    ):
        self.docs_path = Path(docs_path)
        self.persist_directory = persist_directory
        self.collection_name = collection_name

        # Local embedding model (no API key needed)
        self.embedding_model = SentenceTransformer(embedding_model_name)

        # Chroma persistent client
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def _chunk_article(self, doc: Dict[str, Any], max_chars: int = 800) -> List[Dict[str, Any]]:
        """
        Simple but effective chunking:
        - Keep title + category as context
        - Split content on headings / paragraphs
        """
        doc_id = doc["doc_id"]
        title = doc.get("title", "")
        category = doc.get("category", "")
        content = doc.get("content", "")

        # Split by double newlines or markdown headings
        import re
        parts = re.split(r'\n#{1,3} |\n\n+', content)
        parts = [p.strip() for p in parts if p.strip()]

        chunks = []
        for i, part in enumerate(parts):
            # Keep chunks reasonably sized
            if len(part) > max_chars:
                # further split long sections
                for j in range(0, len(part), max_chars):
                    chunk_text = part[j:j + max_chars]
                    chunks.append({
                        "id": f"{doc_id}_{i}_{j}",
                        "doc_id": doc_id,
                        "title": title,
                        "category": category,
                        "text": f"{title}\n\n{chunk_text}"
                    })
            else:
                chunks.append({
                    "id": f"{doc_id}_{i}",
                    "doc_id": doc_id,
                    "title": title,
                    "category": category,
                    "text": f"{title}\n\n{part}"
                })
        return chunks

    def build_index(self, force_rebuild: bool = False):
        """Load documentation, chunk, embed and store in Chroma."""
        if self.collection.count() > 0 and not force_rebuild:
            print(f"Index already exists with {self.collection.count()} chunks. Skipping build.")
            return

        with open(self.docs_path, "r", encoding="utf-8") as f:
            docs = json.load(f)

        all_chunks = []
        for doc in docs:
            all_chunks.extend(self._chunk_article(doc))

        print(f"Total chunks to index: {len(all_chunks)}")

        texts = [c["text"] for c in all_chunks]
        ids = [c["id"] for c in all_chunks]
        metadatas = [
            {
                "doc_id": c["doc_id"],
                "title": c["title"],
                "category": c["category"]
            }
            for c in all_chunks
        ]

        # Embed in batches
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True).tolist()

        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Indexed {len(all_chunks)} chunks into Chroma.")

    def retrieve(self, query: str, top_k: int = RETRIEVAL_TOP_K) -> List[Dict[str, Any]]:
        """
        Retrieve the most relevant passages for a query.
        Returns list of dicts with: text, doc_id, title, category, distance
        """
        if self.collection.count() == 0:
            raise RuntimeError("Index is empty. Call build_index() first.")

        query_embedding = self.embedding_model.encode([query]).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        retrieved = []
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ):
            retrieved.append({
                "text": doc,
                "doc_id": meta["doc_id"],
                "title": meta["title"],
                "category": meta["category"],
                "distance": dist
            })
        return retrieved


# Convenience function
def get_retriever() -> DocumentRetriever:
    retriever = DocumentRetriever()
    retriever.build_index()
    return retriever