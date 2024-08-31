import json

from libraries.cognito import initiate_auth, register_user
from libraries.errors import VerifyAuthCodeError
from libraries.request import http_response, log_event


@log_event
def handle(event: dict, _):
    try:
        resource = event["resource"]
        body = json.loads(event["body"])
        name = body.get("name")
        email = body.get("email")
        password = body.get("password")
        role = body.get("role")

        if resource == "/sign-in":
            response = initiate_auth(email, password)
            return http_response(response, 201)

        created_user = register_user(name, email, password, role, True)
        return http_response(created_user, 201)
    except VerifyAuthCodeError:
        return http_response("Unauthorized", 401)
