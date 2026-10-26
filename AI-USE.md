# AI Use Disclosure — Mindful Minute

**Course:** IST 402 · **Project:** Assignment 3, Mindful Minute · **Updated:** 2026-10-26

## Tools, models, identifiers, and roles

| Tool / model | Version or identifier | Role and scope |
| --- | --- | --- |
| OpenAI ChatGPT | GPT-6 (assistant identified in this project conversation; exact service build not available) | Helped plan Part 1, explain GitHub/Codespaces steps, generate and commit Part 2 Vue, FastAPI, and SQLite implementation, and draft documentation and testing guidance. |
| GitHub and GitHub Codespaces | GitHub repository `clarissaalessi1-creator/mindful-minute`; Codespaces version not recorded | Code hosting, edits, browser-based runtime, and user-observed tests; these are development tools, not AI models. |
| Optional OpenAI API integration | `gpt-4o-mini` is the configured default model identifier in backend source; OpenAI Python SDK dependency currently unpinned | Application code supports model-generated optional chat when an API key is configured. **No live model call has been verified.** The observed response was a deterministic fallback because `OPENAI_API_KEY` was absent. |

**Other AI assistance:** No additional AI tool/model has been confirmed for this repository. Update this document if GitHub Copilot, Gemini, another model, or another tool is actually used. A visible Copilot interface alone is not evidence of use.

## What AI produced and what the student reviewed

ChatGPT generated application scaffolding and source code for the paced-breathing interface, backend endpoints, database tables, optional chat integration, and safety-information view. The student reviewed the GitHub file structure, corrected a nested `backend/backend` directory and renamed `main.py Copy` to `main.py`, ran the application in Codespaces, and reported successful breathing, pause/resume, exit, and history interactions. Screenshots provided in the working conversation showed the running home page and the chat fallback. These observations do not establish full coverage or clinical effectiveness.

## Limits, security, and academic integrity

- No credentials, personal health data, research-participant information, or private third-party content belong in submitted evidence.
- Chat prompts and tests use fictional scenarios. The app is a coursework prototype, not therapy or an emergency service.
- ChatGPT-generated code and guidance must be reviewed, tested, and revised by the student; no claim of full correctness is made.
- The AI model does not control exercise timing, persistence, or the crisis-support route.
- The optional chat's current fallback is **not** a live AI-model demonstration. If a live model is later connected, record its actual model identifier, test, result, and date here.
- This is a curated disclosure, not a full conversation export.

See [docs/evidence-log.md](docs/evidence-log.md) for selected redacted evidence and outstanding verification.
