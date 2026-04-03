from mypy_boto3_ses.type_defs import SendEmailResponseTypeDef
from aws_lambda_powertools.utilities.data_classes import DynamoDBStreamEvent, event_source
from Utils import SES_CLIENT, success_response
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

    return success_response({"message": "Email sent successfully"})


