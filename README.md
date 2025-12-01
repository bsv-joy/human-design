# Human Designs Project

This project is a web application built using Next.js (Frontend) and FastAPI (Backend) that allows users to create, view, edit, and delete their own "human designs" or manifestos. It leverages the structure and conventions of the `bsv_music` project as a template.

## Technologies Used

### Frontend
-   **Framework**: Next.js (React)
-   **Language**: TypeScript
-   **Styling**: Tailwind CSS, `@tailwindcss/typography`, `tailwindcss-animate`
-   **Routing**: Next.js App Router

### Backend
-   **Framework**: FastAPI
-   **Language**: Python
-   **Database**: SQLite (file-based database)
-   **ORM**: SQLAlchemy
-   **Migrations**: Alembic
-   **Environment Management**: `uv` (for Python dependencies)
-   **ASGI Server**: Uvicorn

## Getting Started

Follow these steps to set up and run the project locally.

### 1. Clone the Repository (if not already done)
```bash
# Assuming you are in your personal code directory
git clone <repository-url>
cd human-designs
```

### 2. Backend Setup

Navigate to the `backend` directory:
```bash
cd backend
```

**a. Create and Activate Virtual Environment**
The project uses `uv` for Python dependency management.
```bash
uv venv
source .venv/bin/activate
```

**b. Install Python Dependencies**
```bash
uv pip install -r requirements.txt
```

**c. Configure Environment Variables**
Create a `.env.local` file in the `backend` directory based on the `.env.example` in the project root.
```bash
cp ../.env.example .env.local
```
Then, edit `.env.local` and ensure `DATABASE_URL` is set for SQLite (e.g., `DATABASE_URL=sqlite:///./sql_app.db`). A `SECRET_KEY` will also be needed, which you can generate.

**d. Run Database Migrations**
Apply the database migrations to create the necessary tables. Make sure your virtual environment is activated before running alembic commands.
```bash
alembic upgrade head
```

**e. Run the Backend Server**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
The backend API will be available at `http://localhost:8000`.

### 3. Frontend Setup

Open a new terminal and navigate to the project root:
```bash
cd human-designs
```

**a. Install Node.js Dependencies**
The project uses `npm` for Node.js dependency management.
```bash
npm install
```

**b. Run the Frontend Development Server**
```bash
npm run dev
```
The frontend application will be available at `http://localhost:3000`.

## Key Features

-   **Create Designs**: Users can create new "human designs" (manifestos) using a simple text editor.
-   **View Designs**: Browse a list of all created designs and view individual designs.
-   **Edit Designs**: Modify existing designs.
-   **Delete Designs**: Remove unwanted designs.
-   **Themed UI**: Uses Tailwind CSS with a custom theme derived from `bsv_music` for a visually consistent experience.

## Project Structure

-   `app/`: Next.js frontend application, including UI components, pages, and styling.
    -   `app/components/`: Reusable React components (`ManifestoEditor`, `ManifestoContent`, `Navigation`, `Mascot`).
    -   `app/manifesto/`: Page for creating/viewing/editing a single manifesto.
    -   `app/manifestos/`: Page for listing all manifestos.
-   `backend/`: Python FastAPI backend services.
    -   `backend/main.py`: FastAPI application entry point and API routes.
    -   `backend/database.py`: SQLAlchemy database setup and session management.
    -   `backend/models.py`: SQLAlchemy ORM models (e.g., `UserManifesto`).
    -   `backend/alembic/`: Alembic migration scripts and environment.
    -   `backend/requirements.txt`: Python dependencies.
-   `.env.example`: Template for environment variables.
-   `tailwind.config.ts`, `postcss.config.mjs`: Tailwind CSS configuration.

## Next Steps / Future Enhancements

-   **Rich Text Editor**: Integrate a more robust rich text editor (e.g., TinyMCE, Slate, Quill) in `ManifestoEditor`.
-   **User Authentication**: Implement user registration, login, and associate manifestos with authenticated users.
-   **Error Handling**: Enhance error displays and user feedback in the frontend.
-   **Deployment Automation**: Develop full deployment scripts for production environments (e.g., using Docker, Caddy, systemd).
-   **Backend Tests**: Add unit and integration tests for the FastAPI endpoints.
-   **Frontend Tests**: Implement end-to-end tests for the user interface.
-   **Search/Filtering**: Add functionality to search and filter manifestos.
-   **Pagination**: Implement pagination for the list of manifestos.