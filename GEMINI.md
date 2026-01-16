# GEMINI.md - Project Context & Rules

## 🏗️ Architecture Overview
- `./climb`: **Active Development.** Contains the backend and business logic.
- `./data`: **PRIVATE.** Contains raw climbing logs. (Do not scan/read).
- `./frontend`: **PROTOTYPE.** Streamlit experiment. (Read-only, do not modify).

## 🛡️ Critical Rules (Boundaries)
- **Data Privacy:** Do NOT look into or index the `./data` folder. I will provide schema definitions manually when needed.
- **Scope:** Do not refactor the `./frontend` folder unless explicitly asked.

## 🗺️ Project Vision (Roadmap)
*Note: These are strategic goals. Do not implement unless instructed.*
- **Refactoring:** Future migration to a **FastAPI** middle layer (Backend) and **Streamlit** (Frontend).
- **Data Source:** Exploring API/Scraping integration with the "Kilter Board" app.
- **Infrastructure:** Future Dockerization and pre-commit hook integration.
- **Mapping:** Separate the mapping files `grades.csv` to `grades.json` into a separate folder.

## 🧪 Engineering Standards
- **Unit Testing:** All new functions in `./climb` require unit tests.
- **Data Pipeline:** We favor manual triggers from the UI over automated cron jobs for now.

## ✍️ Style Preferences
- **Language:** Python 3.12+
- **Docstrings:** Use **Numpy-style** documentation.
- **Formatting:** Use `f-strings` over `.format()`.
- **Typing:** (Optional Suggestion) Use Python type hints for better AI code generation.