import os

import boto3

from libraries.errors import SendEmailError

SES_EMAIL_SENDER = os.getenv("SES_EMAIL_SENDER")


def send_ses_email(subject: str, content: str, recipients: list[str],
                   sender=None):
    if not sender:
        sender = SES_EMAIL_SENDER

    try:
        ses_client = boto3.client("ses")
        ses_client.send_email(
            Source=sender,
            Destination={
                "ToAddresses": recipients
            },
            Message={
                "Subject": {
                    "Data": subject,
                    "Charset": "UTF-8"
                },
                "Body": {
                    "Html": {
                        "Data": content,
                        "Charset": "UTF-8"
                    }
                }
            }
        )
    except Exception as err:
        raise SendEmailError(str(err))


def generate_html_authenticate_email(email_login: str, auth_code: str):
    return f"""<html>
    <head></head>
    <body>
      <h1>Faça login no FoodControl.</h1>
      <p>Você solicitou acesso ao FoodControl para o email {email_login}</p>
      <p>Seu código é: <strong>{auth_code}</strong>. Você tem até 15 minutos 
      para acessar antes que ele expire.</p>
    </body>
    </html>"""
