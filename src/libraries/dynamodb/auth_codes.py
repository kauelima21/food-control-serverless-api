import random
import string
import time

from libraries.dynamodb.helpers import get_dynamodb_table

__table_name = "auth_codes"


def find_token(token: str):
    table = get_dynamodb_table(__table_name)
    response = table.get_item(Key={"token": token})

    return response.get("Item")


def destroy_token(token: str):
    table = get_dynamodb_table(__table_name)
    table.delete_item(Key={"token": token})


def store_auth_code(expiration_in_seconds=300):
    table = get_dynamodb_table(__table_name)
    auth_code = ''.join(random.choices(string.digits, k=6))
    table.put_item(Item={
        "token": auth_code,
        "expire_at": int(time.time()) + expiration_in_seconds
    })

    return auth_code
