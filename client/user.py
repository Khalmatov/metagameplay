from contextvars import ContextVar

import config
from dto import User

_authorized_user: ContextVar[User | None] = ContextVar('_authorized_user', default=None)


class UserService:

    @classmethod
    def get_authorized_user(cls) -> User | None:
        if user := _authorized_user.get():
            return user

    @staticmethod
    def set_authorized_user(user: User) -> None:
        _authorized_user.set(user)
        with open(config.BASE_DIR / '.AUTHORIZED_USER', 'w') as file:
            file.write(user.name)

    @staticmethod
    def get_current_username() -> str | None:
        if config.AUTHORIZED_USER_PATH.exists():
            with open(config.AUTHORIZED_USER_PATH) as file:
                return file.read()
