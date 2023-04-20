from contextvars import ContextVar

from enums import State

_state: ContextVar[State] = ContextVar('_state', default=State.LOGIN)


def set_state(state: State) -> None:
    _state.set(state)


def get_state() -> State:
    return _state.get()
