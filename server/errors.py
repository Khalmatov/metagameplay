from enum import Enum


class Messages(str, Enum):
    Unknown = 'Неизвестная ошибка'
    InsufficientFunds = 'Недостаточно средств на счете'


class MainException(Exception):
    """Базовое исключение"""

    class Meta:
        message = Messages.Unknown

    def __init__(self, *args):
        error_msg = self.Meta.message
        if args:
            error_msg = error_msg % args
        super().__init__(error_msg)


class InsufficientFundsException(MainException):
    class Meta:
        message = Messages.InsufficientFunds
