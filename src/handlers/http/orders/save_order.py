import json
import os
from decimal import Decimal

from libraries.dynamodb.orders import save_order
from libraries.request import http_response, log_event


@log_event
def handle(event: dict, _):
    body = json.loads(event["body"])

    order_items = [{
        "quantity": product["quantity"],
        "price_in_cents": product["price_in_cents"],
        "name": product["name"],
    } for product in body.get("products")]

    order = {
        "customer_name": body.get("customer_name"),
        "price_in_cents": Decimal(body.get("price_in_cents")),
        "phone": body.get("phone"),
        "address": body.get("address"),
        "order_items": json.dumps(order_items),
    }

    created_order = save_order(order)

    return http_response({"order_id": created_order["order_id"]}, 201)
