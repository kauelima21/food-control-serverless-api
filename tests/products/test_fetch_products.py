import pytest
from moto import mock_aws

from handlers.http.products.fetch_products import handle
from infra.dynamodb.create_products_table import create_products_table
from libraries.dynamodb.products import save_product


def create_and_populate_products():
    create_products_table()
    products = [
        {"price": 1590, "description": "product 1", "name": "product 1"},
        {"price": 599, "description": "product 2", "name": "product 2"},
        {"price": 800, "description": "product 3", "name": "product 3"},
    ]
    for product in products:
        save_product(product)


@mock_aws
def test_it_should_be_able_to_fetch_products():
    create_and_populate_products()
    event = {
        "resource": "/admin/products",
        "pathParameters": {},
        "queryStringParameters": {}
    }
    response = handle(event, None)
    assert response.get("statusCode") == 200


@mock_aws
def test_it_should_be_able_to_fetch_products_for_a_customer():
    create_and_populate_products()
    event = {
        "resource": "/products",
        "queryStringParameters": {}
    }
    response = handle(event, None)
    assert response.get("statusCode") == 200


if __name__ == "__main__":
    pytest.main()
