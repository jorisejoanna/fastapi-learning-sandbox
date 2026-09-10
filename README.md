# FastAPI Learning Sandbox

A backend project built while learning FastAPI and relational databases. It includes REST endpoints, PostgreSQL integration, user authentication with JWT tokens, and automated tests running via GitHub Actions.

## Live Demo

The API is deployed on Render and connected to a Neon PostgreSQL database:
- Interactive API Documentation: https://fastapi-learning-sandbox.onrender.com/docs

## Tech Stack

- **Backend:** FastAPI (Python 3.12)
- **Database:** PostgreSQL (Neon.tech), SQLAlchemy ORM, Alembic
- **Authentication:** PyJWT, bcrypt
- **Testing:** pytest, HTTPX
- **Hosting & CI/CD:** Render, GitHub Actions

## Features

- REST endpoints for managing items and user accounts
- PostgreSQL connection using SQLAlchemy ORM
- Database migrations with Alembic
- User registration and login with bcrypt password hashing
- Protected routes using JWT (JSON Web Tokens) and OAuth2
- Automated integration tests with pytest and an in-memory SQLite database
- Continuous integration pipeline with GitHub Actions running tests on every push
- CORS middleware enabled for frontend integration

## Project Structure

- `day12_main.py`: Main application entry point with authentication routes
- `database.py`: Database engine and session configuration
- `models.py`: SQLAlchemy database models (tables)
- `schemas.py`: Pydantic schemas for request validation and response formatting
- `utils.py`: Password hashing and JWT generation functions
- `config.py`: Environment variable management
- `tests/`: Automated test suite (`test_main.py`, `test_auth_flow.py`)

## Local Development Setup

### Prerequisites

- Python 3.12+
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jorisejoanna/fastapi-learning-sandbox.git
   cd fastapi-learning-sandbox
   ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a .env file in the project root:
    ```bash
    DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
    SECRET_KEY=your_secret_key_here
    ACCESS_TOKEN_EXPIRE_MINUTES=15
    ```

### Running Locally
```bash
fastapi dev day12_main.py
```

### Running Tests
```bash
pytest -v
```

## License
This project is licensed under the MIT License