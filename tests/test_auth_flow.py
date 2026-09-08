"""
to test the entire authentication journey
notice: 'client' is injected automatically from conftest.py fixture!!
"""

#----------TEST 1: Test Root Endpoint (Status 200)----------
def test_signup(client):
    response = client.post(
        "/users/",
        json={"email": "tester@example.com", "password": "supersecretpassword"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "tester@example.com"
    assert "id" in data
    assert "hashed_password" not in data    #never expose hashed passwords in response!!

#----------TEST 2: Duplicate Email Protection----------
def test_signup_duplicate_email(client):
    #register once
    client.post(
        "/users/",
        json={"email": "duplicate@example.com", "password": "password123"},
    )

    #try registering again with the exact same email
    response = client.post(
        "/users/",
        json={"email": "duplicate@example.com", "password": "password123"},
    )

    print("\n SERVER RESPONSE DETAIL:", response.json()["detail"])  #print statement
    assert response.status_code == 400
    assert response.json() ["detail"] 

#----------TEST 3: Login & Get JWT Token----------
def test_login_success(client):
    #1. create the user
    client.post(
        "/users/",
        json={"email": "loginuser@example.com", "password": "correctpassword"},
    )

    #2. log in via/token/ (OAuth2 expects form-data: username & password)
    response = client.post(
        "/token/",
        data={"username": "loginuser@example.com", "password": "correctpassword"},
    )

    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

#----------TEST 4: Full End-to-End Protected Route Access----------
def test_access_protected_route_with_token(client):
    #1. signup
    client.post(
        "/users/",
        json={"email": "vip@example.com", "password": "vippasword"},
    )

    #2. login to get token
    login_res = client.post(
        "/token/",
        data={"username": "vip@example.com", "password": "vippasword"},
    )
    token = login_res.json()["access_token"]

    #3. access protected/users/me using the token in Authorization header!
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == "vip@example.com"

