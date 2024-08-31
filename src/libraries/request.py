import json
import logging
from functools import wraps


def http_response(data, status_code: int):
    data = json.dumps(data)

    return {
        "statusCode": status_code,
        "body": data,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Credentials": True,
            "Content-Type": "application/json"
        }
    }


def load_query_string_params(event: dict):
    if not event.get("queryStringParameters"):
        return {}

    return event["queryStringParameters"]


def log_event(handler):
    @wraps(handler)
    def wrapper(*args, **kwargs):
        logging.getLogger().setLevel(logging.INFO)
        event = args[0]
        logging.info(f"Process started!\nevent -> {event}")
        response = handler(*args, **kwargs)
        logging.info("Process finished!")
        return response

    return wrapper
