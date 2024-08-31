import logging
import os
import uuid

import boto3

from libraries.dynamodb.auth_codes import find_token, destroy_token
from libraries.errors import VerifyAuthCodeError

COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")

_cognito_client = boto3.client("cognito-idp")


def initiate_auth(email: str, password: str):
    response = _cognito_client.initiate_auth(
        ClientId=COGNITO_CLIENT_ID,
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": email,
            "PASSWORD": password,
        }
    )

    return response["AuthenticationResult"]


def verify_auth_code(email: str, verification_code: str):
    try:
        _cognito_client.admin_get_user(
            UserPoolId=COGNITO_USER_POOL_ID,
            Username=email
        )

        auth_code = find_token(verification_code)
        destroy_token(auth_code["token"])
    except Exception as err:
        logging.info(str(err))
        raise VerifyAuthCodeError(str(err))


def register_user(name: str, email: str, password: str, role="common",
                  automatic_confirm=False):
    user = _cognito_client.sign_up(
        ClientId=COGNITO_CLIENT_ID,
        Username=email,
        Password=password,
        UserAttributes=[
            {
                "Name": "email",
                "Value": email
            },
            {
                "Name": "custom:name",
                "Value": name,
            },
            {
                "Name": "custom:role",
                "Value": role,
            }
        ]
    )

    if automatic_confirm:
        confirm_user(email)

    return user


def confirm_user(email: str):
    _cognito_client.admin_update_user_attributes(
        UserPoolId=COGNITO_USER_POOL_ID,
        Username=email,
        UserAttributes=[
            {
                "Name": "email_verified",
                "Value": "true"
            }
        ]
    )
    _cognito_client.admin_confirm_sign_up(
        UserPoolId=COGNITO_USER_POOL_ID,
        Username=email
    )
