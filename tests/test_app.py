import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_chat_success(client):
    response = client.post(
        "/api/chat",
        json={"message": "How can I manage my monthly budget?"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "response" in data
    assert isinstance(data["response"], str)
    assert len(data["response"]) > 0


def test_chat_empty_message(client):
    response = client.post("/api/chat", json={"message": "   "})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_chat_missing_message(client):
    response = client.post("/api/chat", json={"text": "Hello"})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_chat_invalid_json(client):
    response = client.post(
        "/api/chat",
        data="{invalid-json",
        content_type="application/json"
    )
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_chat_excessively_long_message(client):
    long_msg = "A" * 501
    response = client.post("/api/chat", json={"message": long_msg})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_chat_unexpected_input_type(client):
    response = client.post("/api/chat", json={"message": ["list", "instead", "of", "str"]})
    assert response.status_code == 400
    assert "error" in response.get_json()