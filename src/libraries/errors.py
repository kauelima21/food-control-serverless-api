class CustomException(Exception):
    def __init__(self, code: str, error_message: str):
        super().__init__(f"{code}: {error_message}")


class VerifyAuthCodeError(CustomException):
    def __init__(self, error_message: str):
        self.code = "VERIFY_AUTH_CODE_ERROR"
        super().__init__(self.code, error_message)


class SendEmailError(CustomException):
    def __init__(self, error_message: str):
        self.code = "SEND_MAIL_ERROR"
        super().__init__(self.code, error_message)
