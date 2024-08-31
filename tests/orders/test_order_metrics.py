import pytest

from handlers.http.orders.order_metrics import handle


def test_it_should_get_month_revenue():
    event = {
        "resource": "/metrics/month-revenue"
    }
    response = handle(event, None)
    assert response.get("statusCode") == 200


def test_it_should_get_month_orders_amount():
    event = {
        "resource": "/metrics/month-orders-amount"
    }
    response = handle(event, None)
    assert response.get("statusCode") == 200


def test_it_should_get_month_canceled_orders_amount():
    event = {
        "resource": "/metrics/month-canceled-orders-amount"
    }
    response = handle(event, None)
    assert response.get("statusCode") == 200


def test_it_should_get_day_orders_amount():
    event = {
        "resource": "/metrics/day-orders-amount"
    }
    response = handle(event, None)
    assert response.get("statusCode") == 200


def test_it_should_get_popular_products():
    event = {
        "resource": "/metrics/popular-products"
    }
    response = handle(event, None)
    assert response.get("statusCode") == 200


if __name__ == "__main__":
    pytest.main()
