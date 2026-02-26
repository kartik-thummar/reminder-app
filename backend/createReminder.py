from Utils import DYNAMODB_CLIENT, DYNAMODB_TASK_TABLE, Responses
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response
from mypy_boto3_dynamodb.type_defs import PutItemInputTablePutItemTypeDef
from uuid import uuid4
from datetime import datetime, timezone


def create_reminder(event: APIGatewayRestResolver, context):

    if event.current_event.json_body is None:
        pass

    print(type(event.current_event.raw_event))
    print(event.current_event.raw_event)

    body = event.current_event.json_body
    print(type(body))
    print(body)

    response: PutItemInputTablePutItemTypeDef = DYNAMODB_CLIENT.put_item(
        TableName=DYNAMODB_TASK_TABLE,
        Item={
            "reminderId":   {"S": uuid4()},             # Primary Key
            "userId":       {"S": body['userId']},      # Secondary Key
            "message":      {"S": body['message']},
            "dateTime":     {"N": str(datetime.now(timezone.utc))},
        }
        )
    
    print(response)

    return Responses.success_response(response)