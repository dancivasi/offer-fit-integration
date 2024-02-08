import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, mock_open
import datetime

client = TestClient(app)


@pytest.fixture()
def mock_open_file():
    with patch('builtins.open', new_callable=mock_open, read_data='''[ {"customer_id": 1010, "event_type": 
    "email_click", "timestamp": "2023-11-10T16:55:00", "email_id": 1111, "clicked_link": 
    "https://example.com/link-6"}, {"customer_id": 1010, "event_type": "purchase", "timestamp": 
    "2023-11-10T15:25:00", "email_id": 1111, "product_id": 1212, "amount": 49.99}, {"customer_id": 1111, 
    "event_type": "email_open", "timestamp": "2023-11-11T11:15:00", "email_id": 1212}, {"customer_id": 1111, 
    "event_type": "email_unsubscribe", "timestamp": "2023-11-11T11:45:00", "email_id": 1212}, {"customer_id": 1212, 
    "event_type": "email_click", "timestamp": "2023-11-12T10:05:00", "email_id": 1313, "clicked_link": 
    "https://example.com/link-7"}, {"customer_id": 1212, "event_type": "email_open", "timestamp": 
    "2023-11-12T10:35:00", "email_id": 1313}, {"customer_id": 1313, "event_type": "email_click", "timestamp": 
    "2023-11-13T14:20:00", "email_id": 1414, "clicked_link": "https://example.com/link-8"}, {"customer_id": 1313, 
    "event_type": "purchase", "timestamp": "2023-11-13T14:50:00", "email_id": 1414, "product_id": 1515, 
    "amount": 59.99}, {"customer_id": 1414, "event_type": "email_open", "timestamp": "2023-11-14T17:35:00", 
    "email_id": 1515}, {"customer_id": 1414, "event_type": "email_unsubscribe", "timestamp": "2023-11-14T18:05:00", 
    "email_id": 1515}, {"customer_id": 1515, "event_type": "email_click", "timestamp": "2023-11-15T08:50:00", 
    "email_id": 1616, "clicked_link": "https://example.com/link-9"}]'''
               ):
        yield


def test_get_email_events_with_valid_customer_id(mock_open_file):
    response = client.get("/events/1010")
    assert response.status_code == 200
    assert response.json() == [
        {"customer_id": 1010, "event_type": "email_click", "timestamp": "2023-11-10T16:55:00", "email_id": 1111,
         "clicked_link": "https://example.com/link-6"},
        {"customer_id": 1010, "event_type": "purchase", "timestamp": "2023-11-10T15:25:00", "email_id": 1111,
         "product_id": 1212, "amount": 49.99}
    ]


def test_get_event_with_invalid_customer_id(mock_open_file):
    response = client.get("/events/999")
    assert response.status_code == 204
    assert response.json() == {'message': 'No events for the event provided'}


def test_get_email_events_with_time_range(mock_open_file):
    response = client.get("/get_events/1010?start_time=2023-11-10T16:55:00&end_time=2023-11-15T08:50:00")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_email_events_with_invalid_time_range(mock_open_file):
    response = client.get("/get_events/1010?start_time=2023-01-02T16:55:00&end_time=2023-02-03T08:50:00")
    assert response.status_code == 200
    assert response.json() == {'message': 'No email events found for the provided customer_id'}


def test_get_email_events_with_just_start_time(mock_open_file):
    response = client.get("/get_events/1010?start_time=2023-11-10T16:55:00")
    assert response.status_code == 200
    assert len(response.json()) == 1
