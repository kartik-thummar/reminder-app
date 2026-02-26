from boto3 import session
from mypy_boto3_dynamodb import DynamoDBClient
from http import HTTPStatus
import json

SESSION = session.Session()

REGION = 'ap-south-1'
SERVICE = 'dynamodb'
DYNAMODB_CLIENT: DynamoDBClient = SESSION.client(service_name=SERVICE, region_name=REGION)

DYNAMODB_TASK_TABLE = "Reminders"

class Responses():

    @classmethod
    def success_response(body: dict) -> dict :
        return {
            "statusCode": HTTPStatus.OK, 
            "body": json.dumps(body),
            "headers": {"Content-Type": "application/json"}
            }