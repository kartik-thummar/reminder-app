from Utils import DYNAMODB_CLIENT, DYNAMODB_TASK_TABLE
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response
from mypy_boto3_dynamodb.type_defs import PutItemInputTablePutItemTypeDef
from uuid import uuid4
from datetime import datetime, timezone, timedelta

app = APIGatewayRestResolver()


@app.post("/reminders")
def create_reminder():
    
    # if app.current_event.json_body is None:
    #     pass

    print(app.current_event.raw_event)

    body = app.current_event.json_body
    print(body)


    # ist_str = "2026-03-01 15:30:00"
    ist_str = body["reminderAt"]
    dt_naive = datetime.strptime(ist_str, "%Y-%m-%d %H:%M:%S")
    IST = timezone(timedelta(hours=5, minutes=30))
    dt_ist = dt_naive.replace(tzinfo=IST)
    utc_timestamp = dt_ist.astimezone(timezone.utc).timestamp()


    print(utc_timestamp)

    response: PutItemInputTablePutItemTypeDef = DYNAMODB_CLIENT.put_item(
        TableName=DYNAMODB_TASK_TABLE,
        Item={
            "reminderId":   {"S": str(uuid4())},             # Primary Key
            "userId":       {"S": body['userId']},           # Secondary Key
            "message":      {"S": body['message']},
            "createdAt":    {"N": str(datetime.now(timezone.utc).timestamp())},
            "reminderAt":   {"N": str(utc_timestamp)},
        }
        )
    
    print(response)

    # return Responses.success_response({"message":"reminder successfully created", "response": response})
    return Response(
        status_code=200, 
        body={"message":"reminder successfully created", "response": response},
        headers={"Content-Type": "application/json", "CORS": "*"}
        )


def lambda_handler(event: dict, context):
    return app.resolve(event, context)