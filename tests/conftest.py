from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from database import DATABASE_URL
from sqlalchemy.orm import sessionmaker
import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db
from sqlalchemy import text

main_url = make_url(DATABASE_URL)

assert main_url.database == "todo_db"

test_url = main_url.set(database="todo_api_alembic_test")

test_engine = create_engine(test_url)

TestSessionLocal = sessionmaker(bind=test_engine)


@pytest.fixture
def client():
    with test_engine.connect() as connection:
        transaction = connection.begin()

        database_name = connection.execute(
            text("SELECT current_database()")
        ).scalar_one()

        assert database_name == "todo_api_alembic_test"

        def override_get_db():
            db = TestSessionLocal(
                bind=connection,
                join_transaction_mode="create_savepoint"
            )
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db

        try:
            with TestClient(app) as test_client:
                yield test_client
        finally:
            app.dependency_overrides.pop(get_db, None)
            transaction.rollback()