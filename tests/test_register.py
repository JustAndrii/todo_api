def test_register(client):
    response = client.post(
        "/register",
        json={
            "email": "pytest_user@example.com",
            "password": "test123456"
        }
    )

    assert response.status_code == 200
    assert response.json()["email"] == "pytest_user@example.com"


def test_register2(client):
    response = client.post(
        "/register",
        json={
            "email": "pytest_user@example.com",
            "password": "test123456"
        }
    )
    response2 = client.post(
        "/register",
        json={
            "email": "pytest_user@example.com",
            "password": "test123456"
        }
    )


    assert response.status_code == 200
    assert response.json()["email"] == "pytest_user@example.com"
    assert response2.status_code == 400



def test_tasks(client):
    response = client.get("/tasks")

    assert response.status_code == 401
