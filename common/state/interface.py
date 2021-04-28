from __future__ import annotations
from typing import Any, Union, overload


class IState:
    @overload
    def update(self, *, owner: Any) -> Union[None, IState]: ...

    @overload
    def enter(self, *, owner: Any, old_state: IState) -> None: ...

    @overload
    def exit(self, *, owner: Any, next_state: IState) -> None: ...

    """Empty implementations
    """
    def update(self, *, owner: Any) -> Union[None, IState]:
        pass

    def enter(self, *, owner: Any, old_state: IState) -> None:
        pass

    def exit(self, *, owner: Any, next_state: IState) -> None:
        pass


class IStateOwner:
    def __init__(self, init_state: IState):
        self._state = init_state

    def set_new_state(self, new_state: IState) -> None:
        old_state = self._state
        self._state = new_state
        old_state.exit(owner=self, next_state=new_state)
        self._state.enter(owner=self, old_state=old_state)

    def update(self) -> None:
        new_state = self._state.update(owner=self)
        if new_state is not None:
            self.set_new_state(new_state)
