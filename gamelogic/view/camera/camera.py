from common.utils import utils
from common.state import interface
from .states.base import CameraBaseState


class Camera(interface.IStateOwner):
    def __init__(self,
                 init_center_pixels: utils.Vec2i,
                 init_state: CameraBaseState) -> None:
        interface.IStateOwner.__init__(self, init_state)
        self._center_pixels = init_center_pixels

    def get_center(self) -> utils.Vec2i:
        return self._center_pixels

    def set_center(self, new_center: utils.Vec2i) -> None:
        self._center_pixels = new_center

    def ready(self) -> bool:
        return type(self._state) == CameraBaseState
