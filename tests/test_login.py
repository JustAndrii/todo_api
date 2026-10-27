from urllib import response


def test_login(client):
    response = client.post(
        "/register",
        json={
            "email": "pytest_user@example.com",
            "password": "test123456"
        }
    )
    login_response = client.post(
        "/login",
        data={
            "username": "pytest_user@example.com",
            "password": "test123456"
        }
    )



    assert response.status_code == 200
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    assert login_response.json()["token_type"] == "bearer"


def test_login_wrong_password(client):
    response = client.post(
        "/register",
        json={
            "email": "pytest_user@example.com",
            "password": "test123456"
        }
    )
    login_response = client.post(
        "/login",
        data={
            "username": "pytest_user@example.com",
            "password": "test"
        }
    )

    assert response.status_code == 200
    assert login_response.status_code == 401
    assert "access_token" not in login_response.json()