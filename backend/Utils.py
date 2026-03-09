from boto3 import session
from mypy_boto3_dynamodb import DynamoDBClient
from mypy_boto3_ses import SESClient
from http import HTTPStatus
from os import environ
import json

SESSION = session.Session()

REGION = 'us-east-1'
SERVICE = 'dynamodb'
DYNAMODB_CLIENT: DynamoDBClient = SESSION.client(service_name=SERVICE, region_name=REGION)
SES_CLIENT: SESClient = SESSION.client(service_name="ses", region_name=REGION)

DYNAMODB_TASK_TABLE = environ['REMINDERS_TABLE']

class Responses():

    @classmethod
    def success_response(cls, body: dict) -> dict :
        return {
            "statusCode": HTTPStatus.OK, 
            "headers": {"Content-Type": "application/json", "CORS": "*"},
            "body": json.dumps(body)
            }