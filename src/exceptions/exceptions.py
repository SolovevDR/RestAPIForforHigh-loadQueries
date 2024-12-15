class NotFoundError(Exception):
    def __str__(self):
        return "not found error"


class ExchangeNotFound(Exception):
    def __str__(self):
        return "exchange not found"
