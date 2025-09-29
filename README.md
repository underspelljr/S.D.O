# Spots de Oeiras

Welcome to "Spots de Oeiras," a crowdsourced map application for friends to share interesting spots. This project is built with FastAPI and provides a robust backend API with a simple, interactive map frontend.

## Features

- **Create Spots**: Click anywhere on the map to create a new spot.
- **View Spots**: All existing spots are loaded and displayed as markers on the map.
- **User Management**: Simple user creation to associate spots with a creator.
- **Modern Backend**: Built with FastAPI, Pydantic, and SQLAlchemy.
- **Interactive Frontend**: Uses Leaflet.js for an easy-to-use map interface.
- **Testable**: Comes with a full suite of unit and integration tests using `pytest`.
- **Configurable**: Application settings, database, and logging are easily configured via a `.env` file.

## Project Structure

The project follows a clean, modular architecture to separate concerns:

- `app/main.py`: The main FastAPI application entrypoint.
- `app/core/`: Application configuration and logging.
- `app/db/`: Database session management and base models.
- `app/models/`: SQLAlchemy database models.
- `app/schemas/`: Pydantic data validation schemas.
- `app/routers/`: API endpoint definitions.
- `app/services/`: Business logic.
- `app/templates/` & `app/static/`: Frontend files.
- `tests/`: Automated tests.

---

## 1. Setup Instructions

### Prerequisites

- Python 3.8+
- A virtual environment tool (like `venv`)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd spots-de-oeiras
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure the application:**
    Create a `.env` file in the project root by copying the `.env.example` if it exists, or create it from scratch. The default settings should work out of the box.

    ```
    # .env
    APP_NAME="Spots de Oeiras"
    LOG_LEVEL="DEBUG"
    DATABASE_URL="sqlite:///./spots_de_oeiras.db"
    ```

---

## 2. Running the Server

Once set up, you can run the web server using Uvicorn.

```bash
uvicorn app.main:app --reload