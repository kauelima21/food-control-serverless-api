from datetime import datetime

from libraries.orders.metrics import get_total_revenue, get_orders_in_a_month, \
    get_orders_in_a_day, get_popular_products, get_daily_revenue
from libraries.request import http_response, log_event, \
    load_query_string_params


@log_event
def handle(event: dict, _):
    resource = event["resource"]
    response = {}

    if resource == "/metrics/day-orders-amount":
        response = get_orders_in_a_day()

    if resource == "/metrics/month-revenue":
        response = get_total_revenue()

    if resource == "/metrics/month-canceled-orders-amount":
        response = get_orders_in_a_month(canceled_orders=True)

    if resource == "/metrics/month-orders-amount":
        response = get_orders_in_a_month()

    if resource == "/metrics/popular-products":
        response = get_popular_products()

    if resource == "/metrics/daily-receipt-in-period":
        range_start = load_query_string_params(event).get("from")
        range_end = load_query_string_params(event).get("to")
        response = get_daily_revenue(range_start, range_end)

    return http_response(response, 200)
