def test_tasks_create(client):
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

    token = login_response.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}

    create_task = client.post(

        "/tasks",
        headers=headers,

        json={
            "title": "Learn pytest"
        }
    )

    assert create_task.status_code == 201
    assert create_task.json()["title"] == "Learn pytest"


def test_tasks_get(client):
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

    token = login_response.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}

    create_task = client.post(
        "/tasks",
        headers=headers,
        json={"title": "Learn Python"},
    )

    assert create_task.status_code == 201

    create_task2 = client.post(
        "/tasks",
        headers=headers,
        json={"title": "Learn SQL"},
    )

    assert create_task2.status_code == 201

    get_task = client.get(
        "/tasks",
        headers=headers
    )

    assert get_task.status_code == 200

    tasks = get_task.json()

    titles = []

    for task in tasks:
        titles.append(task["title"])

    assert "Learn Python" in titles
    assert "Learn SQL" in titles
