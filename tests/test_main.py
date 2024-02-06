import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, mock_open
from main import app

client = TestClient(app)


# @pytest.fixture
# def mock_open_file():
#     with patch('builtins.open', new_callable=mock_open, read_data='''[
#         {"customer_id": 123, "event_type": "email_click", "timestamp": "2023-10-23T14:30:00", "email_id": 1234,
#          "clicked_link": "https://example.com/some-link"},
#         {"customer_id": 123, "event_type": "purchase", "timestamp": "25-10-2023T15:33:00", "email_id": 1234,
#          "product_id": 357, "amount": 49.99}
#     ]'''):
#         yield


def test_get_event_with_valid_customer_id():
    response = client.get("/events/123")
    assert response.status_code == 200
    assert response.json() == [
        {"customer_id": 123, "event_type": "email_click", "timestamp": "2023-10-23T14:30:00", "email_id": 1234, "clicked_link": "https://example.com/some-link"},
        {"customer_id": 123, "event_type": "purchase", "timestamp": "25-10-2023T15:33:00", "email_id": 1234, "product_id": 357, "amount": 49.99}
    ]


def test_get_event_with_invalid_customer_id():
    response = client.get("/events/999")
    assert response.status_code == 204
    assert response.json() == {'message': 'No events for the event provided'}