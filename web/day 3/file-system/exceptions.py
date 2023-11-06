
class BaseException(Exception):
    status = 400
    message = ""
    
    def __init__(self, status, message) -> None:
        super().__init__()
        self.status = status
        self.message = message

    def __str__(self):
        return str({'status': self.status, 'message': self.message})

class FileExistsException(BaseException):
    def __init__(self) -> None:
        super().__init__(400, "File with id already exists")

class FileDoesNotExistsException(BaseException):
    def __init__(self) -> None:
        super().__init__(400, "File with id does not exist")