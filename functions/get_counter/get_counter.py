import os
import boto3
import logging
import json


dynamo_client = boto3.resource('dynamodb')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_ddb_connection():
    ENV = os.environ['Environment']
    ddbclient = ''
    if ENV == 'local':
        ddbclient = boto3.client(
            'dynamodb', endpoint_url="http://dynamodb:8000/")
    else:
        ddbclient = boto3.client('dynamodb')
    return ddbclient


def update_counter():
    table_name = os.environ['DDBTableName']
    client = get_ddb_connection()
    client.update_item(
        TableName=table_name,
        Key={'siteUrl': {
            'S': 'visitors'
        }
        },
        ExpressionAttributeValues={
            ':inc': {'N': '1'}
        },
        UpdateExpression="ADD visitors :inc"
    )


def get_counter():
    table_name = os.environ['DDBTableName']
    client = get_ddb_connection()
    response = client.get_item(
        TableName=table_name,
        Key={
            'siteUrl': {'S': 'visitors'}
        }
    )

    item = response['Item']
    # print(json.dumps(response))
    count = int(item['visitors']['N'])
    return count


def lambda_handler(event, context):
    update_counter()
    count = get_counter()

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "message": "success",
            "count": count
        })
    }