import json
from datetime import datetime, timedelta
from itertools import chain

from boto3.dynamodb.conditions import Attr
from dateutil.relativedelta import relativedelta

from libraries.dynamodb.orders import fetch_orders_by_date, fetch_orders


def sum_orders_amount(orders: list):
    return sum(int(order["price_in_cents"]) for order in orders)


def get_popular_products():
    orders = fetch_orders()
    all_order_items = [json.loads(order["order_items"]) for order in orders]
    all_order_items_list = list(chain.from_iterable(all_order_items))
    products_amount = {}

    for order_item in all_order_items_list:
        product = order_item["name"]
        if product in products_amount:
            products_amount[product] += 1
        else:
            products_amount[product] = 1

    popular_products = [{"product": product, "amount": amount} for product,
                        amount in products_amount.items()]

    return {
        "popular_products": popular_products[:5],
    }


def get_orders_in_a_month(canceled_orders=False):
    current_month = datetime.now()
    prev_month = (current_month - relativedelta(months=1)).strftime("%Y-%m")

    orders = fetch_orders_by_date(current_month.strftime("%Y-%m"))
    prev_month_orders = fetch_orders_by_date(prev_month)

    if not canceled_orders:
        orders = [order for order in orders if order["status"] != "canceled"]
        prev_month_orders = [order for order in prev_month_orders if order[
            "status"] != "canceled"]
    else:
        orders = [order for order in orders if order["status"] == "canceled"]
        prev_month_orders = [order for order in prev_month_orders if order[
            "status"] == "canceled"]

    if len(prev_month_orders) != 0:
        diff_from_last_month = ((len(orders) - len(prev_month_orders)) /
                                len(prev_month_orders))
    else:
        diff_from_last_month = 1 if len(orders) > 0 else 0

    return {
        "amount": len(orders),
        "diff_from_last_month": diff_from_last_month * 100
    }


def get_orders_in_a_day():
    current_day = datetime.now()
    prev_month = (current_day - relativedelta(days=1)).strftime("%Y-%m-%d")

    orders = fetch_orders_by_date(current_day.strftime("%Y-%m-%d"))
    prev_day_orders = fetch_orders_by_date(prev_month)

    if len(prev_day_orders) != 0:
        diff_from_last_day = ((len(orders) - len(prev_day_orders)) /
                              len(prev_day_orders))
    else:
        diff_from_last_day = 1

    return {
        "amount": len(orders),
        "diff_from_yesterday": diff_from_last_day * 100
    }


def get_total_revenue():
    current_month = datetime.now()
    prev_month = (current_month - relativedelta(months=1)).strftime("%Y-%m")

    orders = fetch_orders_by_date(current_month.strftime("%Y-%m"),
                                  Attr("status").ne("canceled"))
    current_amount = sum_orders_amount(orders)

    prev_month_orders = fetch_orders_by_date(prev_month, Attr("status").ne(
        "canceled"))
    prev_amount = sum_orders_amount(prev_month_orders)

    if prev_amount != 0:
        diff_from_last_month = (current_amount - prev_amount) / prev_amount
    else:
        diff_from_last_month = 1

    return {
        "revenue": current_amount,
        "diff_from_last_month": diff_from_last_month * 100
    }


def get_daily_revenue(range_start: str, range_end: str):
    if not range_start or not range_end:
        return []

    range_start = datetime.strptime(range_start, "%Y-%m-%dT%H:%M:%S.%fZ")
    range_end = datetime.strptime(range_end, "%Y-%m-%dT%H:%M:%S.%fZ")
    range_date = []
    current_date = range_start
    while current_date <= range_end:
        range_date.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)

    response = []
    for date in range_date:
        orders = fetch_orders_by_date(date, Attr("status").ne("canceled"))
        response.append({
            "date": date,
            "revenue": sum_orders_amount(orders)
        })

    return response
