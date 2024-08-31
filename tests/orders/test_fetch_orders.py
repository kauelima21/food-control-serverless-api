import pytest
from moto import mock_aws

from handlers.http.orders.fetch_orders import handle
from infra.dynamodb.create_orders_table import create_orders_table
from libraries.dynamodb.orders import save_order


def create_and_populate_orders():
    create_orders_table()
    orders = [
        {"status": "delivered", "customer": "kaueslim@gmail.com",
         "description": "order 1"},
        {"status": "pending", "customer": "kaueslim@gmail.com",
         "description": "order 2"},
        {"status": "delivered", "customer": "kaueslim@gmail.com",
         "description": "order 3"},
        {"status": "delivered", "customer": "messi@outlook.com",
         "description": "order 4"},
        {"status": "pending", "customer": "messi@outlook.com",
         "description": "order 5"},
        {"status": "delivered", "customer": "kaueslim@gmail.com",
         "description": "order 6"},
        {"status": "delivered", "customer": "kaueslim@gmail.com",
         "description": "order 7"},
        {"status": "delivered", "customer": "kaueslim@gmail.com",
         "description": "order 8"},
    ]
    for order in orders:
        save_order(order)


@mock_aws
def test_it_should_be_able_to_fetch_orders():
    create_and_populate_orders()
    event = {
        "resource": "/admin/orders",
        "pathParameters": {},
        "queryStringParameters": {
            "limit": 2,
            "page_index": 1
        }
    }
    response = handle(event, None)
    assert response.get("statusCode") == 200


@mock_aws
def test_it_should_be_able_to_fetch_orders_by_filter():
    create_and_populate_orders()
    event = {
        "resource": "/admin/orders",
        "pathParameters": {},
        "queryStringParameters": {
            "status": "delivered",
            "customer": "kaueslim@gmail.com",
            "limit": 2,
            "page_index": 1
        }
    }
    response = handle(event, None)
    assert response.get("statusCode") == 200


@mock_aws
def test_it_should_be_able_to_fetch_orders_for_a_customer():
    create_and_populate_orders()
    event = {
        "resource": "/customer/{customer}/orders",
        "pathParameters": {
            "customer": "kaueslim@gmail.com"
        },
        "queryStringParameters": {}
    }
    response = handle(event, None)
    assert response.get("statusCode") == 200


if __name__ == "__main__":
    pytest.main()
