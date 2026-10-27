<p align="center">
  <img src="assets/hurbetai-logo.png" alt="HurbetAI mascot — friendly robot logo" width="220" />
</p>

# HurbetAI

**Building a language model from the ground up** 

HurbetAI is a personal learning project: implement the ideas behind modern LLMs in plain Python, understand how tokenization and training actually work, and grow the codebase step by step instead of treating AI as a black box.

---

## Learning path

This repo follows the video series on YouTube:

**[LLM tutorial playlist](https://youtube.com/playlist?list=PLQRyiBCWmqp5twpd8Izmaxu5XRkxd5yC-&si=20wPKSIwRTpqBQWm)**

See [CHANGELOG.md](CHANGELOG.md) for dated updates.

## Goals

- **Understand** how text becomes tokens and how models consume them.
- **Implement** core pieces in readable Python as the tutorial progresses.
- **Document** progress in this repo so future-you (and others) can follow the arc from “split a string” to “run inference.”

## Local interactive chat

HurbetAI now includes a small, local-first chat interface. It searches documents you have saved locally, records the conversation in a local SQLite database, and never sends chat messages to a hosted service.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
git clone https://github.com/twitter/the-algorithm data/knowledge/the-algorithm
streamlit run app.py
```

Open the address Streamlit prints (normally `http://localhost:8501`) and ask questions about the locally cloned source tree.

`twitter/the-algorithm` is a recommendation-system codebase, **not** a tweet dataset or a ready-to-train language model. The chat uses it as a local reference corpus only. The lightweight search interface is deliberately honest about this until HurbetAI has its own trained model checkpoint.

### Local X/FxTwitter data

`import_fxtwitter_export.py` can turn a JSON export you already saved legally and are permitted to retain into `data/datasets/posts.jsonl`:

```powershell
python import_fxtwitter_export.py path\to\your-export.json
```

The importer never calls X or FxTwitter itself, and `data/` is excluded from Git. Do not collect private, deleted, or restricted posts, and only train on material you have the right to use. Before model training, add dataset documentation, provenance, opt-out/deletion handling, and a content-filtering pass.
