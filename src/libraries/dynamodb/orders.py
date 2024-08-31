import datetime
import uuid

from boto3.dynamodb.conditions import Key, Attr

from libraries.dynamodb.helpers import get_dynamodb_table

__table_name = "orders"
__table = get_dynamodb_table(__table_name)


def fetch_orders() -> list:
    response = __table.scan()
    orders = response.get("Items")

    if "LastEvaluatedKey" in response:
        response = __table.scan(ExclusiveStartKey=response[
            "LastEvaluatedKey"])
        orders.extend(response.get("Items"))

    return orders


def find_order_by_id(order_id: str) -> dict:
    response = __table.get_item(Key={"order_id": order_id})

    return response.get("Item")


def fetch_orders_by_filters(order_id: str = None, customer: str = None,
                            status: str = None, page: int = None, limit=50):
    response = __filter_orders(order_id, customer, status, start_key=None,
                               limit=limit)
    offset = 0

    if (page and page > 0) and "LastEvaluatedKey" in response:
        offset = page * limit
        for i in range(0, page):
            data = __filter_orders(order_id, customer, status, response[
                "LastEvaluatedKey"], limit)
            response.get("Items").extend(data.get("Items"))

    return response.get("Items")[offset:limit+offset]


def fetch_orders_by_status(status: str, start_key: dict = None, limit=50):
    query = {
        "IndexName": "status-index",
        "KeyConditionExpression": Key("status").eq(status),
        "Limit": limit
    }
    if start_key:
        query.update({"ExclusiveStartKey": start_key})
    response = __table.query(**query)

    return response


def fetch_orders_by_customer(customer: str, start_key: dict = None, limit=50):
    query = {
        "IndexName": "customer-index",
        "KeyConditionExpression": Key("customer").eq(customer),
        "Limit": limit
    }
    if start_key:
        query.update({"ExclusiveStartKey": start_key})
    response = __table.query(**query)

    return response


def save_order(data: dict) -> dict:
    generated_id = uuid.uuid4()
    data.update({
        "order_id": str(generated_id)[:8],
        "status": "pending",
        "created_at": datetime.datetime.now(datetime.UTC).isoformat()
    })

    __table.put_item(Item=data)
    return data


def fetch_orders_by_date(date: str, filters: str = None):
    filter_expression = Attr("created_at").begins_with(date)
    if filters:
        filter_expression = filter_expression & filters

    response = __table.scan(
        FilterExpression=filter_expression
    )
    orders = response.get("Items")

    while "LastEvaluatedKey" in response:
        response = __table.scan(
            FilterExpression=Attr("created_at").begins_with(date),
            ExclusiveStartKey=response["LastEvaluatedKey"]
        )
        orders.extend(response.get("Items"))

    return orders


# def __filter_orders(order_id: str = None, customer: str = None,
#                     status: str = None, start_key: dict = None, limit=50):
#     response = {}
#     if status and not order_id and not customer:
#         response = fetch_orders_by_status(status, start_key, limit)
#
#     if customer and not order_id and not status:
#         response = fetch_orders_by_customer(customer, start_key, limit)
#
#     if customer and status and not order_id:
#         query = {
#             "IndexName": "status-index",
#             "KeyConditionExpression": Key("status").eq(status) & Key(
#                 "customer").eq(customer),
#             "Limit": limit
#         }
#         if start_key:
#             query.update({"ExclusiveStartKey": start_key})
#         response = __table.query(**query)
#
#     if order_id:
#         filter_expression = Attr("order_id").eq(order_id)
#         if customer:
#             filter_expression = filter_expression & Attr("customer").eq(customer)
#
#         if status:
#             filter_expression = filter_expression & Attr("status").eq(status)
#
#         query = {
#             "FilterExpression": filter_expression,
#             "Limit": limit
#         }
#         if start_key:
#             query.update({"ExclusiveStartKey": start_key})
#         response = __table.query(**query)
#
#     return response
