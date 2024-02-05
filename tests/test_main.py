import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_email_events_with_valid_customer_id():
    response = client.get("/get_email_events/123")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_email_events_with_invalid_customer_id():
    response = client.get("/get_email_events/999")
    assert response.status_code == 200
    assert response.json() == {'message': 'No email events found for the provided customer_id'}


def test_get_email_events_with_time_range():
    response = client.get("/get_email_events/123?start_time=2023-10-23T14:00:00&end_time=2023-10-24T12:00:00")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_email_events_with_invalid_time_range():
    response = client.get("/get_email_events/123?start_time=2023-10-25T00:00:00&end_time=2023-10-26T00:00:00")
    assert response.status_code == 200
    assert response.json() == {'message': 'No email events found for the provided customer_id'}
