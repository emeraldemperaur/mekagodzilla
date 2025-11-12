from typing import Optional

# Errors
class ApiError(Exception):
    def __init__(self, message: str, * , status_code:Optional[int]=None, body:Optional[str]=None):
        super().__init__(message)
        self.status_code = status_code
        self.body = body

    def __str__(self) -> str:
        base = super().__str__()
        if self.status_code is not None:
            base += f" (status code={self.status_code})"
        if self.body:
                base += f" body={self.body[:400]}"
        return base