from enum import Enum


class Command(str, Enum):
    LOGIN = 'login'
    GET = 'get'
    SET = 'set'
    SELL = 'sell'
