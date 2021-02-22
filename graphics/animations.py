import math

from graphics.sprite import Sprite
# from settings.screen import CELL_SIZE, CELL_WIDTH, CELL_HEIGHT


class Animation:
    def __init__(self, sprite: Sprite):
        self.sprite = sprite

    def next_sprite(self):
        return self.sprite


class StaticStandAnimation(Animation):
    def __init__(self, sprite: Sprite, max_ticks=100, max_var=1/4):
        Animation.__init__(self, sprite)
        self.curr_tick = 0
        self.max_ticks = max_ticks
        self.max_var_y = max_var

    def next_sprite(self):
        self.curr_tick = (self.curr_tick + 1) % self.max_ticks
        r = self.curr_tick / self.max_ticks * 2
        r = r ** 2 * (r - 2) ** 2
        # upp + down: t**2 * (t-2)**2
        self.sprite.offset_xy = (0, r * self.max_var_y)
        return self.sprite


class StaticAttackAnimation(Animation):
    def __init__(self, sprite: Sprite, direction_xy: tuple, max_ticks=100, max_var_x=1, max_var_y=1):
        Animation.__init__(self, sprite)
        self.curr_tick = 0
        self.max_ticks = max_ticks

        length = math.sqrt(direction_xy[0] ** 2 + direction_xy[1] ** 2)
        variation = math.sqrt(max_var_x**2 + max_var_y**2)
        d = 1.5 * variation / length
        self.var_xy = d*direction_xy[0],  d*direction_xy[1]

    def next_sprite(self):
        self.curr_tick = (self.curr_tick + 1) % self.max_ticks
        r = self.curr_tick / self.max_ticks * 2
        r = r ** 2 * (r - 2) ** 2
        self.sprite.offset_xy = (r*self.var_xy[0], r*self.var_xy[1])
        return self.sprite


class StaticMoveAnimation(Animation):
    def __init__(self, sprite: Sprite,
                 dxdy: tuple,
                 speed=1,
                 max_ticks=100,
                 max_var_x=1/7,
                 max_var_y=1/7):
        Animation.__init__(self, sprite)
        self.curr_tick = 0
        self.max_ticks = max_ticks
        self.speed = speed
        length = math.sqrt(dxdy[0]**2 + dxdy[1]**2)
        self.dxdy = dxdy[0]/length, dxdy[1]/length
        self.max_var_x = max_var_x
        self.max_var_y = max_var_y

    def next_sprite(self):
        self.curr_tick = (self.curr_tick + self.speed) % self.max_ticks
        r = self.curr_tick / self.max_ticks
        _cos, _sin = self.dxdy
        # T = (cos -sin)
        #     (sin  cos)
        dx, dy = 0, abs(self.max_var_y * math.sin(r * 2 * math.pi))
        dx, dy = _cos*dx - _sin*dy, _sin*dx + _cos*dy
        self.sprite.offset_xy = dx, dy
        return self.sprite


if __name__ == '__main__':
    from matplotlib import pyplot

    import numpy as np

    xs = np.arange(0, 2.05, 0.05)
    ys = xs ** 2 * (xs - 2) ** 2
    pyplot.plot(xs, ys)
    pyplot.show()
