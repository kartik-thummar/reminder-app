from unittest.mock import patch
import pytest
import json, os

os.environ["REMINDERS_TABLE"] = "Reminders"
from ..createReminder import app, lambda_handler



def make_apigateway_event(path, method, body):
    return {
        "path": path,
        "httpMethod": method,
        "body": body,
        "headers": {"Content-Type": "application/json"},
        "isBase64Encoded": False
        }

@pytest.fixture
def mock_put_item():

    with patch("createReminder.DYNAMODB_CLIENT.put_item") as mock:
        mock.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
        yield mock

def test_create_reminder_success(mock_put_item):

    body = {
        "userId": "kartikthummar6@gmail.com",
        "message": "Test message",
        "reminderAt": "2026-03-03 4:00:00"
    }

    event = make_apigateway_event("/reminders", "POST", json.dumps(body))

    response = lambda_handler(event, {})

    data = json.loads(response["body"])

    # Validate response status code
    assert response["statusCode"] == 200, "Invalid response status code"
