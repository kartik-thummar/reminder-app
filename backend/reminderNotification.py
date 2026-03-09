from mypy_boto3_ses.type_defs import SendEmailResponseTypeDef
from aws_lambda_powertools.utilities.data_classes import DynamoDBStreamEvent, event_source
from Utils import SES_CLIENT
from os import environ

SENDER_EMAIL_ID = environ["SENDER_EMAIL_ID"]


@event_source(data_class=DynamoDBStreamEvent)
def reminder_notification(event: DynamoDBStreamEvent, context):
    
    print(event.raw_event)

    print(event.records)
    for record in event.records:

        print(f"record : {record.raw_event}")

        if record.event_name.name == "REMOVE" :

                print(record.dynamodb.old_image)
                user_email = record.dynamodb.old_image["userId"]
                message = record.dynamodb.old_image["message"]

                response: SendEmailResponseTypeDef = SES_CLIENT.send_email(
                        Source=SENDER_EMAIL_ID,
                        Destination={
                            "ToAddresses": [user_email],
                        },
                        Message={
                            "Subject": {"Data": "Your reminder" , "Charset": "UTF-8"},
                            "Body": {
                                "Text": {
                                    "Data": message,
                                    "Charset": "UTF-8"
                                },
                            },
                        },
                    )

                print(response)

    # for record in event["Records"]:
    #     if record["eventName"] == "REMOVE":
    #         user_identity = record.get("userIdentity", {})
    #         if user_identity.get("type") == "Service":

    #             old_image = record["dynamodb"]["OldImage"]

    #             user_email = old_image["userId"]["S"]
    #             message = old_image["message"]["S"]

    #             response: SendEmailResponseTypeDef = SES_CLIENT.send_email(
    #                     Source=SENDER_EMAIL_ID,
    #                     Destination={
    #                         "ToAddresses": [user_email],
    #                     },
    #                     Message={
    #                         "Subject": {"Data": "Your reminder" , "Charset": "UTF-8"},
    #                         "Body": {
    #                             "Text": {
    #                                 "Data": message,
    #                                 "Charset": "UTF-8"
    #                             },
    #                         },
    #                     },
    #                 )

    #             print(response)

# Event data
{
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

