import datetime
import uuid

from boto3.dynamodb.conditions import Key, Attr

from libraries.dynamodb.helpers import get_dynamodb_table

__table_name = "products"
__table = get_dynamodb_table(__table_name)


def fetch_products(page: int = None, limit=50) -> list:
    response = __table.scan(Limit=limit)
    offset = 0

    if (page and page > 0) and "LastEvaluatedKey" in response:
        offset = page * limit
        for i in range(0, page):
            data = __table.scan(Limit=limit, ExclusiveStartKey=response[
                "LastEvaluatedKey"])
            response.get("Items").extend(data.get("Items"))

    return response.get("Items")[offset:limit+offset]


def find_product_by_id(product_id: str) -> dict:
    response = __table.get_item(Key={"product_id": product_id})

    return response.get("Item")


def fetch_products_by_filters(product_id: str = None, status: str = None,
                              page: int = None, limit=50):
    response = __filter_products(product_id, status, start_key=None,
                                 limit=limit)
    offset = 0

    if (page and page > 0) and "LastEvaluatedKey" in response:
        offset = page * limit
        for i in range(0, page):
            data = __filter_products(product_id, status, response[
                "LastEvaluatedKey"], limit)
            response.get("Items").extend(data.get("Items"))

    return response.get("Items")[offset:limit+offset]


def fetch_products_by_status(status: str, start_key: dict = None, limit=50):
    query = {
        "IndexName": "status-index",
        "KeyConditionExpression": Key("status").eq(status),
        "Limit": limit
    }

    if start_key:
        query.update({"ExclusiveStartKey": start_key})

    response = __table.query(**query)
    return response


def save_product(data: dict) -> dict:
    generated_id = uuid.uuid4()
    data.update({
        "product_id": str(generated_id),
        "status": "active",
        "created_at": datetime.datetime.now(datetime.UTC).isoformat()
    })

    __table.put_item(Item=data)

    return data


def __filter_products(product_id: str = None, status: str = None,
                      start_key: dict = None, limit=50):
    response = {}
    if status and not product_id:
        response = fetch_products_by_status(status, start_key, limit)

    if product_id:
        filter_expression = Attr("product_id").eq(product_id)

        if status:
            filter_expression = filter_expression & Attr("status").eq(status)

        query = {
            "FilterExpression": filter_expression,
            "Limit": limit
        }
        if start_key:
            query.update({"ExclusiveStartKey": start_key})
        response = __table.query(**query)

    return response
