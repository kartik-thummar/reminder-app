import json
import pytest
from unittest.mock import patch

from os import environ
environ["REMINDERS_TABLE"] = "Reminders"

from ..createReminder import lambda_handler, app



def make_api_gateway_request(path: str, method: str, body: dict) -> dict :

    return {
        "path": path,
        "httpMethod": method,
        "body": json.dumps(body),
        "headers": {"Content-Type": "application/json"},
        "isBase64Encoded": False
        }


@pytest.fixture
def mock_list_reminders():

    # pass
    with patch("createReminder.DYNAMODB_CLIENT.scan") as mock:

        mock.return_value = {"statusCode": 200}

        yield mock


@pytest.mark.integration
def test_list_reminders(mock_list_reminders):

    body = {"name":"test_name"}
    event = make_api_gateway_request("/reminders", "GET", body)

    response = lambda_handler(event, {})

    print(type(response["body"]))

    assert response["statusCode"] == 200, "Invalid response"

    assert json.loads(response["body"])["message"] == "Reminders data fetched successfully", "Invalid response message"

