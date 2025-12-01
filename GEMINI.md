# Human Designs Project - Gemini CLI Agent Documentation

This document provides context and guidelines for the Gemini CLI agent when interacting with the `human-designs` project.

## Project Scope and Overview

The `human-designs` project is a web application that enables users to create, view, edit, and delete their own long-form text content, referred to as "human designs" or "manifestos". It serves as a template for a production-ready web app, built using a Next.js frontend and a FastAPI Python backend, with styling inspired by the `bsv_music` project.

## Project Structure

The project follows a modular structure:

-   `app/`: Next.js frontend application, including UI components, pages, and styling.
    -   `app/components/`: Reusable React components (`ManifestoEditor`, `ManifestoContent`, `Navigation`, `Mascot`).
    -   `app/manifesto/`: Page for creating, viewing, and editing a single manifesto.
    -   `app/manifestos/`: Page for listing all manifestos.
-   `backend/`: Python FastAPI backend services.
    -   `backend/main.py`: FastAPI application entry point, API routes, and Pydantic models.
    -   `backend/database.py`: SQLAlchemy database engine, session management, and `get_db` dependency.
    -   `backend/models.py`: SQLAlchemy ORM models (e.g., `UserManifesto`).
    -   `backend/alembic/`: Alembic migration scripts and environment configuration.
    -   `backend/requirements.txt`: Python dependencies.
-   `lib/`: Shared utility functions for the frontend (e.g., `utils.ts`).
-   `public/`: Static assets (currently minimal).
-   `scripts/`: Contains setup scripts (currently minimal, with `06_setup_postgres.sh` removed for SQLite).
-   `.env.example`: Template for environment variables.
-   `tailwind.config.ts`, `postcss.config.mjs`: Tailwind CSS and PostCSS configuration.

## Key Technologies

### Frontend
-   **Framework**: Next.js (React)
-   **Language**: TypeScript
-   **Styling**: Tailwind CSS (`@tailwindcss/typography`, `tailwindcss-animate`)
-   **Routing**: Next.js App Router
-   **Package Manager**: `npm` (used for installation, `bun` was originally intended as per `bsv_music` template but not universally available).

### Backend
-   **Framework**: FastAPI
-   **Language**: Python
-   **Database**: SQLite (file-based, defined in `backend/.env.local` as `sqlite:///./sql_app.db`)
-   **ORM**: SQLAlchemy
-   **Migrations**: Alembic
-   **Dependency Management**: `uv` (for Python packages)
-   **Server**: Uvicorn
-   **Libraries**: `python-dotenv` for environment variable management.

## Core Functionality

1.  **Human Design Management**:
    -   Users can create a new design via the `/manifesto` page (if no ID is provided) using `ManifestoEditor`.
    -   Existing designs can be viewed at `/manifesto?id={id}`.
    -   Existing designs can be edited at `/manifesto?id={id}&edit=true` using `ManifestoEditor`.
    -   A list of all designs is available at `/manifestos`.
    -   Designs can be deleted from the `/manifestos` list.
2.  **API Endpoints**: The backend provides standard RESTful CRUD endpoints for `UserManifesto` objects:
    -   `POST /generate-design` (Create)
    -   `GET /manifestos` (Read all)
    -   `GET /manifestos/{manifesto_id}` (Read one)
    -   `PATCH /manifestos/{manifesto_id}` (Update)
    -   `DELETE /manifestos/{manifesto_id}` (Delete)
3.  **Database Migrations**: Alembic is configured to manage schema changes for the SQLite database.

## Development & Operations

#### Frontend
-   **Run Dev Server**: `npm run dev` (from project root)
-   **Build**: `npm run build` (from project root)

#### Backend
-   **Setup**:
    1.  `cd backend`
    2.  `uv venv`
    3.  `source .venv/bin/activate`
    4.  `uv pip install -r requirements.txt`
    5.  Ensure `.env.local` exists with `DATABASE_URL=sqlite:///./sql_app.db` and a `SECRET_KEY`.
-   **Run Migrations**: `source .venv/bin/activate && alembic upgrade head` (from `backend` directory)
-   **Run Server**: `source .venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000 --reload` (from `backend` directory)

## Gemini-specific Notes

-   **Adhere to Conventions**: When making changes, please adhere to the existing code style, formatting, and conventions (TypeScript for frontend, Python for backend, Tailwind CSS for styling).
-   **Testing**: While explicit tests are pending, consider how new features or bug fixes can be verified.
-   **Shell Commands**: Explain the purpose of shell commands before execution.
-   **Database**: The project currently uses SQLite for simplicity. Do not attempt to reconfigure for PostgreSQL without explicit instruction.
-   **Alembic**: If making model changes, remember to generate and apply new Alembic migrations (`alembic revision --autogenerate -m "description"` followed by `alembic upgrade head`).
-   **Frontend Package Manager**: Prefer `npm` for frontend package management if `bun` is not available.
-   **Modular Backend**: The backend is structured with `database.py`, `models.py`, and `main.py` for clarity and maintainability.

## Future TODOs (from `README.md`)

-   **Rich Text Editor**: Integrate a more robust rich text editor (e.g., TinyMCE, Slate, Quill) in `ManifestoEditor`.
-   **User Authentication**: Implement user registration, login, and associate manifestos with authenticated users.
-   **Error Handling**: Enhance error displays and user feedback in the frontend.
-   **Deployment Automation**: Develop full deployment scripts for production environments (e.g., using Docker, Caddy, systemd).
-   **Backend Tests**: Add unit and integration tests for the FastAPI endpoints.
-   **Frontend Tests**: Implement end-to-end tests for the user interface.
-   **Search/Filtering**: Add functionality to search and filter manifestos.
-   **Pagination**: Implement pagination for the list of manifestos.
