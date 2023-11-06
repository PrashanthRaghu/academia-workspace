

class TokenMissingError(BaseException):
    def __init__(self) -> None:
        super().__init__(400, "Auth Header Missing in request")


class TokenInvalidError(BaseException):
    def __init__(self) -> None:
        super().__init__(403, "Invalid Token")