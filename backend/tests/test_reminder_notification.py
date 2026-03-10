from unittest.mock import patch
import pytest
from os import environ

environ["REMINDERS_TABLE"] = "Reminders"
environ["SENDER_EMAIL_ID"] = "kthummar786@gmail.com"
from ..reminderNotification import reminder_notification


@pytest.fixture
def mock_reminder_notification():

    with patch("reminderNotification.SES_CLIENT.send_email") as mock:

        mock.return_value({
            'MessageId': '0100019cd2924d32-69ce88c8-57d3-4694-86e7-ef11fdf45fdd-000000', 
            'ResponseMetadata': {
                'RequestId': '31a1b2af-d0bc-4e05-a259-857c7e0c2b04', 
                'HTTPStatusCode': 200, 
                'HTTPHeaders': {
                    'date': 'Mon, 09 Mar 2026 12:28:49 GMT', 
                    'content-type': 'text/xml', 
                    'content-length': '326', 
                    'connection': 'keep-alive', 
                    'x-amzn-requestid': '31a1b2af-d0bc-4e05-a259-857c7e0c2b04'
                    }, 
                'RetryAttempts': 0
                }
            }
        )

        yield mock


def make_lambda_event():
    return {
        "Records": [
            {
                "eventID": "7b60ece399848fce02a53ca43e9bb8d9",
                "eventName": "REMOVE",
                "eventVersion": "1.1",
                "eventSource": "aws:dynamodb",
                "awsRegion": "us-east-1",
                "dynamodb": {
                    "ApproximateCreationDateTime": 1772791961.0,
                    "Keys": {
                        "reminderId": {"S": "55ee4899-e749-4b0a-98bd-ec6283aa6c42"},
                        "userId": {"S": "kthummar786@gmail.com"},
                    },
                    "OldImage": {
                        "createdAt": {"N": "1772791039.314835"},
                        "reminderId": {"S": "55ee4899-e749-4b0a-98bd-ec6283aa6c42"},
                        "message": {"S": "Test Message"},
                        "reminderAt": {"N": "1772791200"},
                        "userId": {"S": "kthummar786@gmail.com"},
                    },
                    "SequenceNumber": "36922500002170499542653000",
                    "SizeBytes": 204,
                    "StreamViewType": "NEW_AND_OLD_IMAGES",
                },
                "userIdentity": {
                    "principalId": "dynamodb.amazonaws.com",
                    "type": "Service",
                },
                "eventSourceARN": "arn:aws:dynamodb:us-east-1:632598605203:table/Reminders/stream/2026-03-02T15:07:33.607",
            }
        ]
    }


def test_reminder_notification(mock_reminder_notification):

    event = make_lambda_event()
    response = reminder_notification(event, {})

    print(response)

    assert response["statusCode"] == 200, "Error response"

