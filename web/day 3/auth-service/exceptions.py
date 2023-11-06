
class BaseException(Exception):
    status = 400
    message = ""
    
    def __init__(self, status, message) -> None:
        super().__init__()
        self.status = status
        self.message = message

    def __str__(self):
        return str({'status': self.status, 'message': self.message})

class TokenGenerationError(BaseException):
    def __init__(self) -> None:
        super().__init__(500, "Unable to generate the token")

