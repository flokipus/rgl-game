from typing import overload

from common.state import interface


class VisualState(interface.IState):
    """Base state. It does nothing."""
    @overload
    def ready(self) -> bool: ...

    def ready(self) -> bool:
        return True
