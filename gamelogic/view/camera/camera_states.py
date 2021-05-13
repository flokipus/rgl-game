# -*- coding: utf-8 -*-

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Union
import math

from common import global_parameters
from common.utils import utils
from gamelogic.view.camera import camera


class ICameraState(ABC):
    @abstractmethod
    def enter(self, *, camera_owner: camera.Camera, old_state: ICameraState) -> None:
        pass

    @abstractmethod
    def exit(self, *, camera_owner: camera.Camera, next_state: ICameraState) -> None:
        pass

    @abstractmethod
    def update(self, *, camera_owner: camera.Camera) -> Union[None, ICameraState]:
        pass

    @abstractmethod
    def ready(self) -> bool:
        pass


class CameraBaseState(ICameraState):
    def enter(self, *, camera_owner: camera.Camera, old_state: ICameraState) -> None:
        return

    def exit(self, *, camera_owner: camera.Camera, next_state: ICameraState) -> None:
        return

    def update(self, *, camera_owner: camera.Camera) -> Union[None, ICameraState]:
        return None

    def ready(self) -> bool:
        return True


class CameraShaking(ICameraState):
    def __init__(self, decay_time: float, delay: float, amplitude: int, fps: int) -> None:
        """Total time of shaking = decay_time + delay
        amplitude = max amplitude of shaking
        """
        self.decay_time = decay_time
        self.amplitude = amplitude
        self.delay = delay
        self.fps = fps
        self.time_begin = None
        self.init_center = None

    def enter(self, *, camera_owner: camera.Camera, old_state: ICameraState) -> None:
        self.time_begin = global_parameters.current_frame_time_ms / 1000
        self.init_center = camera_owner.get_center()

    def exit(self, *, camera_owner: camera.Camera, next_state: ICameraState) -> None:
        camera_owner.set_center(self.init_center)

    def update(self, *, camera_owner: camera.Camera) -> Union[None, ICameraState]:
        delta_time = global_parameters.current_frame_time_ms / 1000 - self.time_begin
        if delta_time < self.delay:
            return None
        else:
            delta_time -= self.delay
            r = min(1.0, delta_time / self.decay_time)
            if r >= 1.0:
                return CameraBaseState()
            dxy = self.__noise_func(r)
            camera_owner.set_center(self.init_center + dxy)
            return None

    def __noise_func(self, r) -> utils.Vec2i:
        radius = 2 * self.amplitude * r * (1 - r)
        x = radius * math.sin(math.pi*2*r)
        y = radius * math.cos(math.pi*2*r)
        return utils.Vec2i(x, y)

    def ready(self) -> bool:
        return False


class CameraMovingWithDelay(ICameraState):
    def __init__(self, new_center_pixel: utils.Vec2i, time_to_move: float, delay_ratio: float, fps: int) -> None:
        self.time_to_move = time_to_move
        self.new_center = new_center_pixel
        self.delay_ratio = delay_ratio
        self.actual_delay = delay_ratio
        self.fps = fps
        self.time_begin = None
        self.init_center = None
        self.__a = 0

    def enter(self, *, camera_owner: camera.Camera, old_state: ICameraState) -> None:
        if isinstance(old_state, CameraMovingWithDelay):
            self.actual_delay = 0
        elif self.actual_delay > 0.0:
            self.actual_delay = self.delay_ratio
            self.__a = 1 / (4*self.actual_delay * self.time_to_move)

        self.time_begin = (global_parameters.current_frame_time_ms / 1000) - 1/self.fps  # hack?
        self.init_center = camera_owner.get_center()

    def __func_math(self, r) -> float:
        if r < 2*self.actual_delay:
            return self.__a * r**2
        else:
            return (r - self.actual_delay) / self.time_to_move

    def update(self, *, camera_owner: camera.Camera) -> Union[None, ICameraState]:
        delta_time = global_parameters.current_frame_time_ms / 1000 - self.time_begin
        if delta_time >= self.time_to_move + self.actual_delay:
            camera_owner.set_center(self.new_center)
            return CameraBaseState()
        else:
            f = self.__func_math(delta_time)
            new_center = self.init_center + (self.new_center - self.init_center) * f
            camera_owner.set_center(new_center)
            return None

    def exit(self, *, camera_owner: camera.Camera, next_state: ICameraState) -> None:
        camera_owner.set_center(self.new_center)

    def ready(self) -> bool:
        return False


if __name__ == '__main__':
    pass
