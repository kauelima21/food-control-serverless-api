import logging

import boto3

from libraries.dynamodb.helpers import create_table

logging.getLogger().setLevel(logging.INFO)

resource = boto3.resource("dynamodb", region_name="sa-east-1")
__table_name = "orders"


def table_schema():
    return {
        "TableName": __table_name,
        "KeySchema": [
            {
                "AttributeName": "order_id",
                "KeyType": "HASH"
            },
        ],
        "AttributeDefinitions": [
            {
                "AttributeName": "order_id",
                "AttributeType": "S"
            },
            {
                "AttributeName": "customer",
                "AttributeType": "S"
            },
            {
                "AttributeName": "status",
                "AttributeType": "S"
            }
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "status-index",
                "KeySchema": [
                    {
                        "AttributeName": "status",
                        "KeyType": "HASH"
                    },
                    {
                        "AttributeName": "customer",
                        "KeyType": "RANGE"
                    },
                ],
                "Projection": {
                    "ProjectionType": "ALL"
                },
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5
                }
            },
            {
                "IndexName": "customer-index",
                "KeySchema": [
                    {
                        "AttributeName": "customer",
                        "KeyType": "HASH"
                    },
                ],
                "Projection": {
                    "ProjectionType": "ALL"
                },
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    'WriteCapacityUnits': 5
                }
            },
        ],
        "ProvisionedThroughput": {
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    }


def create_orders_table():
    create_table(__table_name, resource, table_schema())


if __name__ == "__main__":
    create_orders_table()
