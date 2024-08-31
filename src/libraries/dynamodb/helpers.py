import logging

import boto3

logging.getLogger().setLevel(logging.INFO)


def get_dynamodb_table(table_name: str):
    return boto3.resource(
        "dynamodb",
        region_name="sa-east-1"
    ).Table(table_name)


def is_table_created(table_name: str, resource) -> bool:
    try:
        table = resource.Table(table_name)
        if table.creation_date_time:
            logging.info("Table already exists!")
            return True
    except resource.meta.client.exceptions.ResourceNotFoundException as err:
        return False


def create_table(table_name: str, resource, table_schema: dict) -> bool:
    if is_table_created(table_name, resource):
        return False

    table = resource.create_table(**table_schema)

    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

    logging.info("table {} successfully created!".format(table_name))

    return True


def update_ttl(client, table_name, ttl_attribute_name):
    try:
        response = client.update_time_to_live(
            TableName=table_name,
            TimeToLiveSpecification={
                "Enabled": True,
                "AttributeName": ttl_attribute_name,
            },
        )
        logging.info(
            f"TTL has been successfully enabled for {table_name} using"
            f" {ttl_attribute_name} as the TTL attribute."
        )
        return response
    except Exception as error:
        logging.exception(f"Error enabling TTL for {table_name}: {error}")
