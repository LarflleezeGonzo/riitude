from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from ..api.dependencies import get_db
from ..main import app
from ..models import Base

client = TestClient(app)

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    database = TestingSessionLocal()
    yield database
    database.close()


app.dependency_overrides[get_db] = override_get_db


def setup() -> None:
    Base.metadata.create_all(bind=engine)


def teardown() -> None:
    Base.metadata.drop_all(bind=engine)


def test_create_book():
    setup()
    try:
        response = client.post(
            "/books",
            json={
                "title": "Test Book 1",
                "author": "Test Author 1",
                "publication_year": 2022,
            },
        )
        assert response.status_code == 201
        assert response.json()["message"] == "Book created"
        assert "data" in response.json()
    finally:
        teardown()


def test_create_review():
    setup()
    try:
        create_book_response = client.post(
            "/books",
            json={
                "title": "Test Book",
                "author": "Test Author",
                "publication_year": 2022,
            },
        )
        assert create_book_response.status_code == 201
        book_id = create_book_response.json()["data"]["id"]

        response = client.post(
            f"/books/{book_id}/reviews",
            json={"text": "Test Review", "rating": 5},
            params={"book_id": book_id},
        )
        assert response.status_code == 201
        assert response.json()["message"] == "Review created"
        assert "data" in response.json()
    finally:
        teardown()


def test_get_books():
    setup()
    try:
        client.post(
            "/books",
            json={"title": "Book 1", "author": "Author 1", "publication_year": 2022},
        )
        client.post(
            "/books",
            json={"title": "Book 2", "author": "Author 2", "publication_year": 2022},
        )

        response = client.get("/books")
        assert response.status_code == 200
        assert response.json()["message"] == "Retrieved all books"
        assert "data" in response.json()
    finally:
        teardown()


def test_get_reviews():
    setup()
    try:
        create_book_response = client.post(
            "/books",
            json={
                "title": "Test Book",
                "author": "Test Author",
                "publication_year": 2022,
            },
        )
        assert create_book_response.status_code == 201
        book_id = create_book_response.json()["data"]["id"]

        response = client.get(f"/books/{book_id}/reviews")
        assert response.status_code == 200
        assert response.json()["message"] == "Retrieved reviews"
        assert "data" in response.json()
    finally:
        teardown()
