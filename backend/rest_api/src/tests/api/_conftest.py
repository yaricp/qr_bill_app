import os
import sys
import uuid
import pytest
from hashlib import sha256
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


print(f"path:  {os.getcwd()}")
sys.path.append("..")


from fastapi.testclient import TestClient

from src.api import app     # Import your FastAPI app
from src.infra.database.connection import DATABASE_URL
from src.infra.database.models import (
    Model as Base,
    Seller,
    User
)      # Import the necessary models




# Setup a test database (in-memory SQLite or a test-specific database)
SQLALCHEMY_DATABASE_URL = DATABASE_URL  # In-memory SQLite for testing

# Create engine and sessionmaker for test database
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)


# Create a fixture to provide the test client and database session
@pytest.fixture(scope="function")
def db_session():
    # Create a new session for each test function
    session = SessionLocal()

    # Yield the session to the test function
    yield session

    # After the test function runs, clean up by closing the session
    session.close()


@pytest.fixture(scope="function")
def test_client(db_session):
    # Create test client that uses the app and DB session
    app.dependency_overrides[SessionLocal] = lambda: db_session  # Override the DB dependency
    client = TestClient(app)
    return client


# Fixture to create some test data (sellers)
@pytest.fixture(scope="function")
def create_sellers(db_session):
    # Create test seller data in the database before each test
    seller_data = [
        {
            "id": uuid.uuid4(),
            "name": "Seller One",
            "official_name": "Official Seller One",
            "address": "123 Test St",
            "city": "Test City"
        },
        {
            "id": uuid.uuid4(),
            "name": "Seller Two",
            "official_name": "Official Seller Two",
            "address": "456 Test Ave",
            "city": "Test City"
        }
    ]

    # Add sellers to the database session
    sellers = [Seller(**data) for data in seller_data]
    db_session.add_all(sellers)
    db_session.commit()

    # Return the created sellers for use in the tests
    return sellers


# Fixture to clean up the database after tests
@pytest.fixture(scope="function", autouse=True)
def cleanup(db_session):
    # Clean up the database after each test function
    yield
    db_session.query(Seller).delete()
    db_session.commit()


# New fixture for authenticating users and obtaining an OAuth2 token
@pytest.fixture(scope="function")
def oauth2_token(test_client):

    reg_data = {
        "login": "test_user",
        "password": "test"
    }
    reg_url = "/api/v1/auth/register"

    response = test_client.post(reg_url, json=reg_data)

    # Assert the response and get the access token
    assert response.status_code == 200, "Register failed"

    # Replace with the real login URL for OAuth2 login (your FastAPI app's login URL)
    login_url = "/api/v1/auth/login"

    # Replace these with the actual credentials required for login
    login_payload = {
        "username": "test_user",  # Replace with valid test credentials
        "password": "test"  # Replace with valid test credentials
    }
    
    # Make a POST request to the login endpoint to obtain a token
    response = test_client.post(login_url, data=login_payload)

    # Assert the response and get the access token
    assert response.status_code == 200, "Login failed"
    token = response.json().get("access_token")
    assert token, "Access token not found in response"
    logger.info(f"Access Token: {token}")
    return token


# Fixture to include the authorization header in the request for authenticated endpoints
@pytest.fixture(scope="function")
def auth_headers(oauth2_token):
    # Prepare the authorization header using the OAuth2 token
    return {
        "Authorization": f"Bearer {oauth2_token}"
    }
