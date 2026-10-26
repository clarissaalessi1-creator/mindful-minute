# Mindful Minute — IST 402 Assignment 3

A coursework prototype offering a fixed, optional 60-second paced-breathing exercise (4-second inhale, 6-second exhale), session history, and optional AI chat. Not therapy, diagnosis, monitoring, or emergency support.

## Features and current status

- Vue 3 / Vite interface with Start, Pause, Resume, Exit, and low-motion checkbox.
- Static Crisis Support view with US 988 and emergency information, independent of AI.
- FastAPI session and chat endpoints, backed by SQLite.
- Optional OpenAI model call using `OPENAI_API_KEY`; without it, chat returns an explicitly labeled fallback. **Live AI is not yet configured or verified.**
- The student reported successful browser tests of breathing controls and session history. Formal persistence, failure-mode, and end-to-end timing tests are pending.

## Run in Codespaces

Terminal 1:

```sh
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Terminal 2 (from the repository root):

```sh
cd frontend
npm install
npm run dev
```

Open forwarded port 5173. The frontend proxies `/api` to port 8000.

Never commit API keys. If a live model is needed, configure `OPENAI_API_KEY` through a secure Codespaces secret or environment setting and verify the actual response. Do not expose port 8000 or 5173 publicly with sensitive data.

## Submission and disclosure

- [Part 1 design report](report.md)
- [AI-use disclosure](AI-USE.md)
- [Curated, redacted evidence log](docs/evidence-log.md)

Only fictional inputs should be used. Before submission, finish the pending tests in the evidence log and add redacted screenshots and actual outcomes. AI assistance is disclosed, but unverified functionality is not represented as complete.
