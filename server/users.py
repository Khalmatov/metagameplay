from contextvars import ContextVar

import hashlib
import hmac

import config
import db


authorized_user: ContextVar[str | None] = ContextVar('authorized_user', default=None)


def create_new_user(username: str, password: str):
    hash_of_password = hash_password(password)
    db.create_user(username, hash_of_password)


def authenticate(username: str, password: str):
    hash_of_password = db.get_user_password(username)
    if is_correct_password(hash_of_password, password):
        authorized_user.set(username)


def hash_password(password: str) -> bytes:
    hash_of_password = hashlib.pbkdf2_hmac('sha256', password.encode(), config.SECRET_KEY.encode('utf-8'), 100000)
    return hash_of_password


def is_correct_password(hash_of_password: bytes, password: str) -> bool:
    return hmac.compare_digest(
        hash_of_password,
        hashlib.pbkdf2_hmac('sha256', password.encode(), config.SECRET_KEY.encode('utf-8'), 100000)
    )
