import json
import tempfile
import unittest
from pathlib import Path

from hurbetai.datasets import import_fxtwitter_export
from hurbetai.knowledge import answer_from_documents


class LocalToolsTests(unittest.TestCase):
    def test_local_search_returns_relevant_excerpt(self) -> None:
        with self.subTest("searches local material"), tempfile.TemporaryDirectory(
            dir=Path(__file__).parent
        ) as directory:
            root = Path(directory) / "knowledge"
            root.mkdir()
            (root / "architecture.md").write_text("The ranker chooses posts for the timeline.")

            answer, sources = answer_from_documents(root, "How does the ranker choose posts?")

            self.assertIn("ranker", answer)
            self.assertEqual(sources[0].path.name, "architecture.md")

    def test_importer_only_writes_text_posts(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            root = Path(directory)
            source = root / "export.json"
            source.write_text(json.dumps({"tweets": [{"id": 1, "text": "Allowed text"}, {"id": 2}]}))
            destination = root / "posts.jsonl"

            self.assertEqual(import_fxtwitter_export(source, destination), 1)
            self.assertEqual(json.loads(destination.read_text()), {
                "text": "Allowed text",
                "source": "user-provided-fxtwitter-export",
                "id": "1",
            })
