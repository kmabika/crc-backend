import os
import boto3
import logging
import json
from botocore.exceptions import ClientError

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
    try:
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
    except client.exceptions.ResourceNotFoundException as e:
        logging.error('Cannot do operations on a non-existent table')
        raise e
    except ClientError as e:
        logging.error('Unexpected error')
        raise e


def lambda_handler(event, context):
    update_counter()
    table_name = os.environ['DDBTableName']
    client = get_ddb_connection()
    try:
        response = client.get_item(
            TableName=table_name,
            Key={
                'siteUrl': {'S': 'visitors'}
            }
        )

        if 'Item' in response:
            item = response['Item']
            count = int(item['visitors']['N'])

            return {
                'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': str(count)
            }

        else:
            return {
                'statusCode': '404',
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': 'Item not found'
                }),
            }

    except client.exceptions.ResourceNotFoundException as e:
        logging.error('Cannot do operation on a non-existent table')
        raise e
    except ClientError as e:
        logging.error('Unexpected error')
        raise e
