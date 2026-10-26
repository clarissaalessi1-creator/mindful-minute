# Curated, Redacted Evidence Log — Assignment 3 Part 2

**Project:** Mindful Minute · **Updated:** 2026-10-26

This log summarizes selected development prompts, resulting changes, observations, and decisions. It intentionally omits credentials, user account identifiers, private messages, personal information, research-participant information, and private third-party content. It is not a complete chat export.

| Stage / selected prompt (paraphrased) | Change or decision | Observed evidence and limits |
| --- | --- | --- |
| Design: “Use meditation for Assignment 3 Part 1.” | Chose a fixed 4-second inhale / 6-second exhale skill for six cycles, with neutral language and an independent crisis-support route. | Part 1 `report.md` documents the rationale; design-stage statements are proposals, not implementation tests. |
| Setup: “Walk me through Part 2 using GitHub.” | Created Vue/Vite and FastAPI structure in the existing repository. | User supplied screenshots of repository and Codespaces; starter files were inspected through connected GitHub. |
| **Failed/revised approach:** “Why are there two backends?” | Initial manual file creation produced `backend/backend/requirements.txt` and `backend/main.py Copy`. Instructions were revised to move the dependency file and rename the Python file. | Subsequent screenshot showed one `backend` directory with `main.py` and `requirements.txt`. This is a genuine corrected setup error. |
| Build: “Add the remaining Part 2 files directly to GitHub.” | ChatGPT created `frontend/src/App.vue`, `frontend/vite.config.js`, `backend/.gitignore`, and replaced `backend/main.py`; updated backend requirements. | GitHub tool returned commit identifiers; source exists in repository. These commits do not themselves prove runtime behavior. |
| Browser run: “Start backend and frontend in Codespaces.” | Ran development servers in the user's browser environment. | Screenshot showed Mindful Minute home page with Start Breathing, Session History, Optional AI Chat, and Crisis Support controls. |
| Functional check: “Test Start, Pause/Resume, Exit, History.” | User performed manual browser interactions. | User reported all tested interactions worked, including session history. Precise timing, database inspection, restart persistence, and failure simulation remain unverified. |
| Model check: “Send a fictional exam-related message in Optional AI Chat.” | Observed deterministic fallback; confirmed no `OPENAI_API_KEY` configured in Codespaces. | Screenshot showed “Live AI is not configured” and a fallback response. **Do not label this a live-model result.** |
| Disclosure: “Include AI-USE.md and curated redacted evidence.” | Added this log and a disclosure file, distinguishing observed behavior from pending tests. | Documentation only; outstanding verification remains below. |

## Outstanding evidence before claiming completion

- [ ] Capture a screenshot of the active breathing timer and the visible Pause, Exit, and Crisis Support controls.
- [ ] Measure one uninterrupted 60-second run with a clock; record actual wall-clock time and confirm it stays within the 90-second cap.
- [ ] Confirm Crisis Support is accessible during the exercise and while the backend/model is unavailable; check whether the exercise keeps timing while the support view is open and fix if needed.
- [ ] Inspect the SQLite `sessions`, `conversations`, and `messages` tables and confirm records persist after restart.
- [ ] Test and document a simulated chat/API failure without compromising core exercise and safety access.
- [ ] Connect and test an actual model if required; document model identifier, prompt category, response summary, and result without storing sensitive text or credentials.
- [ ] Review whether all course rubric requirements are satisfied, then record actual test outcomes and screenshot filenames here.

## Evidence-handling rules

Use only fictional test data. Redact usernames, emails, API keys, access tokens, personal health information, research-participant data, and private third-party material from screenshots and notes. Record enough to show the prompt → change → test → decision chain, not an unfiltered chat export. Do not claim a pending test passed.
