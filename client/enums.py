from enum import Enum


class State(str, Enum):
    LOGIN = 'LOGIN'
    GAME = 'GAME'
    SHOP = 'SHOP'
    BUY = 'BUY'
    SELL = 'SELL'


class Commands(str, Enum):
    PROFILE = 'P'
    SHOP = 'M'
    LOGIN = 'L'
    CANCEL = 'C'
    QUIT = 'Q'
    ASSORTMENT = 'A'
    INVENTORY = 'I'
    BUY = 'B'
    SELL = 'S'
