import json

from libraries.dynamodb.orders import fetch_orders, fetch_orders_by_customer
from libraries.request import http_response, log_event


@log_event
def handle(event: dict, _):
    resource = event["resource"]

    if resource == "/admin/orders":
        orders = fetch_orders()
    else:
        customer = event["pathParameters"]["customer"]
        orders = fetch_orders_by_customer(customer).get("Items")

    orders = [{
        **order,
        "price_in_cents": int(order["price_in_cents"]),
        "order_items": json.loads(order["order_items"])
    } for order in orders]

    return http_response({"orders": orders}, 200)
