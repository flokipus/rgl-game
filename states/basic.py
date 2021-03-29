from __future__ import annotations
from typing import overload, Union


from gameobj.base import GameObject
from command.base import Command


class BaseState:
    @overload
    def update(self, *, gobj: GameObject) -> Union[None, BaseState]: ...

    @overload
    def handle_command(self, *, gobj: GameObject, command: Command) -> Union[None, BaseState]: ...

    @overload
    def enter(self, *, gobj: GameObject, old_state: BaseState) -> None: ...

    @overload
    def exit(self, *, gobj: GameObject, next_state: BaseState) -> None: ...

    @overload
    def ready(self) -> bool: ...

    """Empty implementations
    """
    def update(self, *, gobj: GameObject) -> Union[None, BaseState]:
        pass

    def handle_command(self, *, gobj: GameObject, command: Command) -> Union[None, BaseState]:
        pass

    def enter(self, *, gobj: GameObject, old_state: BaseState) -> None:
        pass

    def exit(self, *, gobj: GameObject, next_state: BaseState) -> None:
        pass

    def ready(self) -> bool:
        return True
