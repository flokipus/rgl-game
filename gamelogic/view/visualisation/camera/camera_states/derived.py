import math
from typing import Union

from common.utils import utils
from common import globals
from .base import CameraBaseState
from ..camera import Camera


class CameraShaking(CameraBaseState):
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

    def enter(self, *, owner: Camera, old_state: CameraBaseState) -> None:
        self.time_begin = globals.current_time_ms / 1000
        self.init_center = owner.get_center()
        print('shaking enter: ', self.init_center)

    def exit(self, *, owner: Camera, next_state: CameraBaseState) -> None:
        owner.set_center(self.init_center)

    def update(self, *, owner: Camera) -> Union[None, CameraBaseState]:
        delta_time = globals.current_time_ms / 1000 - self.time_begin
        if delta_time < self.delay:
            return None
        else:
            delta_time -= self.delay
            r = min(1.0, delta_time / self.decay_time)
            if r >= 1.0:
                return CameraBaseState()
            dxy = self.__noise_func(r)
            owner.set_center(self.init_center + dxy)
            return None

    def __noise_func(self, r) -> utils.Vec2i:
        radius = 2 * self.amplitude * r * (1 - r)
        x = radius * math.sin(math.pi*2*r)
        y = radius * math.cos(math.pi*2*r)
        return utils.Vec2i(x, y)


class CameraSticky(CameraBaseState):
    def __init__(self, animation):
        self.target_animation = animation

    def enter(self, *, owner: Camera, old_state: CameraBaseState) -> None:
        pass

    def update(self, *, owner: Camera) -> Union[None, CameraBaseState]:
        owner.set_center(self.target_animation.get_corner_xy())
        return None


class CameraMovingWithDelay(CameraBaseState):
    def __init__(self, new_center_pixel: utils.Vec2i, time_to_move: float, delay_ratio: float, fps: int) -> None:
        self.time_to_move = time_to_move
        self.new_center = new_center_pixel
        self.delay_ratio = delay_ratio
        self.actual_delay = delay_ratio
        self.fps = fps
        self.time_begin = None
        self.init_center = None
        self.__a = 0

    def enter(self, *, owner: Camera, old_state: CameraBaseState) -> None:
        if type(old_state) == CameraMovingWithDelay:
            self.actual_delay = 0
        elif self.actual_delay > 0.0:
            self.actual_delay = self.delay_ratio
            self.__a = 1 / (4*self.actual_delay * self.time_to_move)

        self.time_begin = (globals.current_time_ms / 1000) - 1/self.fps  # hack?
        self.init_center = owner.get_center()

    def __func_math(self, r) -> float:
        if r < 2*self.actual_delay:
            return self.__a * r**2
        else:
            return (r - self.actual_delay) / self.time_to_move

    def update(self, *, owner: Camera) -> Union[None, CameraBaseState]:
        delta_time = globals.current_time_ms / 1000 - self.time_begin
        if delta_time >= self.time_to_move + self.actual_delay:
            owner.set_center(self.new_center)
            return CameraBaseState()
        else:
            f = self.__func_math(delta_time)
            new_center = self.init_center + (self.new_center - self.init_center) * f
            owner.set_center(new_center)
            return None

    def exit(self, *, owner, next_state) -> None:
        owner.set_center(self.new_center)


if __name__ == '__main__':
    from matplotlib import pyplot
    t = 0.3
    d = 0.1
    step = 0.05
    num = int((t+d) / step)

    xs = [step * i for i in range(num + 1)]
    ys1 = []
    for x in xs:
        # y = 58.33333333333333*x**3 + -9.166666666666666*x**2
        y = x**2 / (4*d*t)
        ys1.append(y)
    pyplot.plot(xs, ys1)
    ys2 = []
    for x in xs:
        y = (x - d) / t
        ys2.append(y)
    pyplot.plot(xs, ys2)

    pyplot.show()
