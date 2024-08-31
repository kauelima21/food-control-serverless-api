from libraries.dynamodb.products import fetch_products, \
    fetch_products_by_status, find_product_by_id
from libraries.request import http_response, log_event


@log_event
def handle(event: dict, _):
    resource = event["resource"]

    if resource == "/products/{product_id}":
        product_id = event["pathParameters"]["product_id"]
        product = find_product_by_id(product_id)
        product["price_in_cents"] = int(product["price_in_cents"])

        return http_response({"product": product}, 200)

    if resource == "/admin/products":
        products = fetch_products()
    else:
        products = fetch_products_by_status("active").get("Items")

    products = [{
        **product, "price_in_cents": int(product.get("price_in_cents"))}
        for product in products]

    return http_response({"products": products}, 200)
