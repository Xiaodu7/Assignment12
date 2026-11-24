from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.user import User


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def registered_user(client):
    unique_id = uuid4().hex[:10]

    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "username": f"user_{unique_id}",
        "email": f"user_{unique_id}@example.com",
        "password": "TestPassword123!",
        "confirm_password": "TestPassword123!"
    }

    response = client.post("/users/register", json=user_data)
    assert response.status_code == 201

    return user_data


@pytest.fixture
def auth_headers(client, registered_user):
    response = client.post(
        "/users/login",
        json={
            "username": registered_user["username"],
            "password": registered_user["password"]
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


def test_user_registration(registered_user, db_session):
    user = db_session.query(User).filter(
        User.username == registered_user["username"]
    ).first()

    assert user is not None
    assert user.email == registered_user["email"]
    assert user.password != registered_user["password"]
    assert user.verify_password(registered_user["password"])


def test_user_login(auth_headers):
    assert auth_headers["Authorization"].startswith("Bearer ")


def test_invalid_login(client, registered_user):
    response = client.post(
        "/users/login",
        json={
            "username": registered_user["username"],
            "password": "WrongPassword123!"
        }
    )

    assert response.status_code == 401


def test_calculation_bread(client, auth_headers):
    # Add
    response = client.post(
        "/calculations",
        json={"type": "addition", "inputs": [10, 5]},
        headers=auth_headers
    )

    assert response.status_code == 201

    calculation = response.json()
    calculation_id = calculation["id"]

    assert calculation["result"] == 15

    # Browse
    response = client.get(
        "/calculations",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert any(
        item["id"] == calculation_id
        for item in response.json()
    )

    # Read
    response = client.get(
        f"/calculations/{calculation_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["result"] == 15

    # Edit
    response = client.put(
        f"/calculations/{calculation_id}",
        json={"inputs": [20, 10]},
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["result"] == 30

    # Delete
    response = client.delete(
        f"/calculations/{calculation_id}",
        headers=auth_headers
    )

    assert response.status_code == 204

    # Verify deletion
    response = client.get(
        f"/calculations/{calculation_id}",
        headers=auth_headers
    )

    assert response.status_code == 404


def test_invalid_calculation(client, auth_headers):
    response = client.post(
        "/calculations",
        json={"type": "division", "inputs": [10, 0]},
        headers=auth_headers
    )

    assert response.status_code == 422


def test_unauthorized_calculation(client):
    response = client.get("/calculations")

    assert response.status_code == 401