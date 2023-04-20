from contextvars import ContextVar

import db
import config
from dto import User

authorized_user: ContextVar[User | None] = ContextVar('authorized_user', default=None)


class UserService:

    @classmethod
    def get_authorized_user(cls) -> User | None:
        if user := authorized_user.get():
            return user

        if username := cls._get_current_username():
            user = get_user(username)
            cls.set_authorized_user(user)
            return user

    @staticmethod
    def set_authorized_user(user: User) -> None:
        authorized_user.set(user)

    @staticmethod
    def _get_current_username() -> str | None:
        if config.AUTHORIZED_USER_PATH.exists():
            with open(config.AUTHORIZED_USER_PATH) as file:
                return file.read()


def create_new_user(username: str):
    db.create_user(username)


def authenticate(username: str) -> User:
    if not db.is_user_exists(username):
        db.create_user(username)
        db.create_credits_of_user(username)
    db.add_user_credits(username, config.CREDITS_ON_LOGIN)
    user = get_user(username)
    authorized_user.set(user)
    return user


def get_user(username: str) -> User:
    user = User(
        name=username,
        balance=db.get_user_balance(username),
        items=db.get_user_items(username)
    )
    db.add_user_credits(username, config.CREDITS_ON_LOGIN)
    return user


def get_all_usernames() -> list[str]:
    return db.get_all_usernames() or ()
