import time
import math
from typing import Union

from common.utils import utils
from .base import CameraBaseState
from ..camera import Camera


class CameraShaking(CameraBaseState):
    ...


class CameraMovingWithDelay(CameraBaseState):
    def __init__(self, new_center_pixel: utils.Vec2i, time_to_move: float, delay_ratio: float, fps: int) -> None:
        self.time_to_move = time_to_move
        self.new_center = new_center_pixel
        self.delay_ratio = delay_ratio
        self.actual_delay = 0
        self.fps = fps
        self.time_begin = None
        self.init_center = None

    def enter(self, *, owner: Camera, old_state: CameraBaseState) -> None:
        if type(old_state) == CameraMovingWithDelay:
            self.actual_delay = 0
        else:
            self.actual_delay = self.delay_ratio
        self.time_begin = time.time() - 1/self.fps  # hack?
        self.init_center = owner.get_center()

    def __func_math(self, r, delay) -> float:
        if r <= delay:
            return 0
        x = (r-delay) / (1 - delay)
        1 + math.sin(math.pi/2 * (x-1))

    def update(self, *, owner: Camera) -> Union[None, CameraBaseState]:
        delta_time = time.time() - self.time_begin
        r = min(1.0, delta_time / self.time_to_move)
        if r == 1.0:
            owner.set_center(self.new_center)
            return CameraBaseState()
        else:
            f = self.__func_math(r, self.actual_delay)
            new_center = self.init_center + (self.new_center - self.init_center) * f
            owner.set_center(new_center)
            return None
