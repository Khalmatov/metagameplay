from contextvars import ContextVar

import db
import config

authorized_user: ContextVar[str | None] = ContextVar('authorized_user', default=None)


def create_new_user(username: str):
    db.create_user(username)


def authenticate(username: str):
    if not db.is_user_exists(username):
        db.create_user(username)
    db.add_credits_to_user(username, config.CREDITS_ON_LOGIN)
    authorized_user.set(username)
    user = {
        'name': username,
        'balance': db.get_user_balance(username),
        'items': db.get_user_inventory()
    }


def get_all_users() -> tuple[str]:
    return db.get_all_users() or ()
