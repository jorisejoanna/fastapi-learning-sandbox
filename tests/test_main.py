"""
Using FastAPI's TestClient (built on httpx) alongside pytest to test your API routes automatically with Python code
-Up until now we've been testing the APIs manually (start the server, open Swagger UI, click "Try it out", type JSON, hit "Execute", look at the response)
-Manual testing works when you have 2 endpoints
-But what happens when the app has 50 endpoints and one line of database code is changed? We can't manually test all 50!
-Automated testing runs a script that stimulates 50 user reequests in 0.5 seconds and tells you if anything broke with a single command: pytest
"""

from fastapi.testclient import TestClient

#1. import the FastAPI app instance to be tested
from main import app
from day11_main import app as signup_app
from day12_main import app as auth_app

#2. create TestClient instances (simulates a browser or HTTP client)
client = TestClient(app)
signup_client = TestClient (signup_app)
auth_client = TestClient(auth_app)

#----------TEST 1: Test Root Endpoint (Status 200)----------
def test_read_main():
    response = client.get("/")              #send a GET request to "/"
    assert response.status_code == 200      #assert that the HTTP status code is 200 OK
    assert "message" in response.json()     #assert that the JSON response contains the expected message

#----------TEST 2: Test Protected Route Without Token (Expect 401 Unauthorized)----------
def test_read_users_me_unauthenticated():   
    response = auth_client.get("/users/me")                         #attempt to visit /users/me without an Authorization header
    assert response.status_code == 401                              #assert that the API correctly blocks the user with 401
    assert response.json() == {"detail": "Not authenticated"}       

#----------TEST 3: Test Validation Error on Invalid Data (Expect 422)----------
def test_create_user_invalid_payload():
    response = signup_client.post("/users/", json={"email": "notanemail"})        #send an invalid payload (missing required "password" field)
    assert response.status_code == 422                                          #FastAPI & Pydantic should catch this and reject it with 422


