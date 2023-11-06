from exceptions.base import BaseException 

class ValidationError(BaseException):
    def __init__(self) -> None:
        super().__init__(400, "Invalid Input Parameter")

class EmployeeNotPresentError(BaseException):
    def __init__(self) -> None:
        super().__init__(404, "Employee not Present")


class FileMissingInUploadError(BaseException):
    def __init__(self) -> None:
        super().__init__(400, "File Missing in request")

class NoFileToDeleteError(BaseException):
    def __init__(self) -> None:
        super().__init__(400, "File Missing in request")

class NoFileToDownloadError(BaseException):
    def __init__(self) -> None:
        super().__init__(400, "File Missing to download")

