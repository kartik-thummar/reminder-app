from boto3 import session

SESSION = session.Session()

REGION = 'ap-south-1'
DYNAMODB_CLIENT = SESSION.client(service_name='dynamodb', region_name=REGION)

