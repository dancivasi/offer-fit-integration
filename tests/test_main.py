import pytest
import json
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_there_is_data_in_json_file():
    with open('events.json', 'r') as file:
        data = json.load(file)
    assert len(data) > 0


def test_get_event_with_valid_customer_id():
    response = client.get("/get_event/123")
    assert response.status_code == 200
    assert response.json() == [
        {"customer_id": 123, "event_type": "email_click", "timestamp": "2023-10-23T14:30:00", "email_id": 1234, "clicked_link": "https://example.com/some-link"},
        {"customer_id": 123, "event_type": "purchase", "timestamp": "25-10-2023T15:33:00", "email_id": 1234, "product_id": 357, "amount": 49.99}
            ]

def test_get_event_with_invalid_customer_id():
    response = client.get("/get_event/999")
    assert response.status_code == 200
    assert response.json() == {'message': 'No events for the event provided'}