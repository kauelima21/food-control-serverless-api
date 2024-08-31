import json
import os
from decimal import Decimal

from libraries.dynamodb.products import save_product
from libraries.request import http_response, log_event
from libraries.s3 import generate_post_url


@log_event
def handle(event: dict, _):
    body = json.loads(event["body"])

    if event.get("resource") == "/admin/products/upload":
        post_url = generate_post_url(
            os.environ["S3_PRODUCTS_BUCKET"],
            body.get("file_name"),
            body.get("type"),
        )

        return http_response({"post_url": post_url}, 201)

    product = {
        "name": body.get("name"),
        "price_in_cents": Decimal(body.get("price_in_cents")),
        "description": body.get("description"),
        "cover": body.get("cover"),
        "category": body.get("category"),
    }

    created_product = save_product(product)

    return http_response({"product_id": created_product["product_id"]}, 201)
