"""Small, dependency-free local document search for the chat interface."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


# Start with the repository's human-written documentation.  Indexing every
# generated/source file in large repositories makes an interactive local chat
# unresponsive; code search can be added later as a separate indexed feature.
SUPPORTED_SUFFIXES = {".md", ".txt"}
WORD_PATTERN = re.compile(r"[a-zA-Z0-9_]{2,}")


@dataclass(frozen=True)
class SearchResult:
    path: Path
    excerpt: str
    score: int


def _words(text: str) -> set[str]:
    return set(WORD_PATTERN.findall(text.lower()))


def search_documents(root: Path, question: str, limit: int = 3) -> list[SearchResult]:
    """Return the most relevant snippets from locally stored source documents."""
    if not root.exists():
        return []

    query_words = _words(question)
    if not query_words:
        return []

    results: list[SearchResult] = []
    for path in root.rglob("*"):
        if path.suffix.lower() not in SUPPORTED_SUFFIXES or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        for paragraph in re.split(r"\n\s*\n", text):
            score = len(query_words & _words(paragraph))
            if score:
                excerpt = " ".join(paragraph.split())[:700]
                results.append(SearchResult(path=path, excerpt=excerpt, score=score))

    return sorted(results, key=lambda item: item.score, reverse=True)[:limit]


def answer_from_documents(root: Path, question: str) -> tuple[str, list[SearchResult]]:
    """Create an honest retrieval answer without claiming to generate model knowledge."""
    matches = search_documents(root, question)
    if not matches:
        return (
            "I could not find that in the local knowledge folder yet. "
            "Add permitted source files, then try again.",
            [],
        )

    answer = "Here is what the local source material says:\n\n" + "\n\n".join(
        f"{match.excerpt}" for match in matches
    )
    return answer, matches
