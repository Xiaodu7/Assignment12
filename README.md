# IS601 Assignment 12 - User & Calculation Routes

## Project Overview

This project is a FastAPI-based calculator application with user registration, login, JWT authentication, PostgreSQL database integration, and calculation BREAD operations.

The project is based on the instructor's Module 12 code, with additional API routes, integration tests, dependency updates, and CI/CD configuration.

## Features

- User registration and login
- Secure password hashing with bcrypt
- JWT authentication
- Calculation BREAD operations
- Pydantic data validation
- PostgreSQL database integration
- Unit, integration, and end-to-end testing
- Docker containerization
- GitHub Actions CI/CD
- Automated security scanning with Trivy

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /users/register | Register a user |
| POST | /users/login | Login a user |
| GET | /calculations | Browse calculations |
| GET | /calculations/{calc_id} | Read a calculation |
| PUT | /calculations/{calc_id} | Edit a calculation |
| POST | /calculations | Add a calculation |
| DELETE | /calculations/{calc_id} | Delete a calculation |
| GET | /health | Check application health |

## Local Setup

Python 3.11 and Docker are required.

```bash
git clone https://github.com/Xiaodu7/Assignment12.git
cd Assignment12

python3.11 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python -m playwright install --with-deps chromium
```

## Running the Application

```bash
docker compose up -d --build
```

Open the following URL in your browser:

http://localhost:8000/docs

## Running Tests

Start the PostgreSQL database:

```bash
docker compose up -d db
```

Configure the test database:

```bash
export DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5432/fastapi_test_db
export TEST_DATABASE_URL=$DATABASE_URL
```

Run unit and integration tests:

```bash
python -m pytest tests/unit/ tests/integration/ -v
```

Run end-to-end tests:

```bash
python -m pytest tests/e2e/ -v
```

## Local Test Results

- Unit and Integration Tests: 93 passed, 1 skipped
- End-to-End Tests: 12 passed
- Total: 105 passed, 0 failed
- Unit and Integration Code Coverage: 86%

## Manual API Testing

Open http://localhost:8000/docs to access Swagger UI.

1. Register a new user.
2. Login with the registered username and password.
3. Click Authorize to authenticate.
4. Create a calculation using POST.
5. Browse and retrieve calculations using GET.
6. Update a calculation using PUT.
7. Delete a calculation using DELETE.
8. Verify that the deleted calculation returns 404.

All manual API operations were tested successfully.

## CI/CD Pipeline

GitHub Actions is configured to:

- Run automated tests with PostgreSQL 17
- Build the Docker image
- Perform Trivy security scanning
- Push the Docker image to Docker Hub after successful checks

## Docker Hub

https://hub.docker.com/r/xdu7/assignment12

Pull the image after successful deployment:

```bash
docker pull xdu7/assignment12:latest
```

## GitHub Repository

https://github.com/Xiaodu7/Assignment12

## Acknowledgments

Original Module 12 code provided by the course instructor:

https://github.com/kaw393939/module12_is601