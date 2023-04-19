from contextvars import ContextVar

from dto import User
import config
from server import server

authorized_user: ContextVar[User | None] = ContextVar('authorized_user', default=None)


class UserService:

    @classmethod
    def get_authorized_user(cls) -> User | None:
        if user := authorized_user.get():
            return user

        if username := cls._get_current_username():
            user = server.get_user(username)
            cls.set_authorized_user(user)
            return user

    @staticmethod
    def set_authorized_user(user: User) -> None:
        authorized_user.set(user)
        with open(config.BASE_DIR / '.AUTHORIZED_USER', 'w') as file:
            file.write(user.name)

    @classmethod
    def is_user_authorized(cls) -> bool:
        return bool(cls.get_authorized_user())

    @staticmethod
    def _get_current_username() -> str | None:
        if config.AUTHORIZED_USER_PATH.exists():
            with open(config.AUTHORIZED_USER_PATH) as file:
                return file.read()
