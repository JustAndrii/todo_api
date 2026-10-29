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

def test_tasks_empty_title(client):
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
        json = {"title": ""},
    )

    assert create_task.status_code == 400
    assert "Task title cannot be empty" in create_task.json()["detail"]


def test_tasks_other_user_access(client):
    # 1. Register two users
    register_user1 = client.post(
        "/register",
        json={
            "email": "pytest_user@example.com",
            "password": "test123456",
        },
    )

    register_user2 = client.post(
        "/register",
        json={
            "email": "pytest_user2@example.com",
            "password": "test1234567",
        },
    )

    assert register_user1.status_code == 200
    assert register_user2.status_code == 200

    # 2. Login both users
    login_user1 = client.post(
        "/login",
        data={
            "username": "pytest_user@example.com",
            "password": "test123456",
        },
    )

    login_user2 = client.post(
        "/login",
        data={
            "username": "pytest_user2@example.com",
            "password": "test1234567",
        },
    )

    assert login_user1.status_code == 200
    assert login_user2.status_code == 200

    # 3. Get JWT tokens
    token_user1 = login_user1.json()["access_token"]
    token_user2 = login_user2.json()["access_token"]

    headers_user1 = {
        "Authorization": f"Bearer {token_user1}"
    }

    headers_user2 = {
        "Authorization": f"Bearer {token_user2}"
    }

    # 4. User 1 creates a private task
    create_task = client.post(
        "/tasks",
        headers=headers_user1,
        json={"title": "Private task"},
    )

    assert create_task.status_code == 201

    task_id = create_task.json()["id"]

    # 5. User 1 can access their own task
    get_own_task = client.get(
        f"/tasks/{task_id}",
        headers=headers_user1,
    )

    assert get_own_task.status_code == 200
    assert get_own_task.json()["id"] == task_id
    assert get_own_task.json()["title"] == "Private task"

    # 6. User 2 cannot access User 1's task
    get_other_user_task = client.get(
        f"/tasks/{task_id}",
        headers=headers_user2,
    )

    assert get_other_user_task.status_code == 404