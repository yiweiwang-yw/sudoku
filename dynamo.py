import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('users')

print(table.creation_date_time)