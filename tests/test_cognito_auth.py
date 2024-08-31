import boto3

COGNITO_CLIENT_ID = "2s981ptht8betprhiq13epigtb"
COGNITO_USER_POOL_ID = "sa-east-1_d8yGPfWlg"

_cognito_client = boto3.client("cognito-idp")


def initiate_auth(email):
    return _cognito_client.initiate_auth(
        ClientId=COGNITO_CLIENT_ID,
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": email,
            "PASSWORD": "Reidofutebol@55",
        }
    )


if __name__ == "__main__":
    user = _cognito_client.admin_get_user(
            UserPoolId=COGNITO_USER_POOL_ID,
            Username="kaueslim@gmail.com"
        )
    response = initiate_auth("kaueslim@gmail.com")
    print(response)
