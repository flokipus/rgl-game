import pygame

from utils import utils


class Visualisation:
    def __init__(self,
                 sprite: pygame.Surface,
                 pixel_xy_offset: utils.Vec2i,
                 state):
        self._sprite = sprite
        self._pixel_xy_offset = pixel_xy_offset
        self._state = state

    def set_pixel_xy_offset(self, new_offset: utils.Vec2i):
        self._pixel_xy_offset = new_offset

    def get_pixel_offset(self) -> utils.Vec2i:
        return self._pixel_xy_offset

    def set_new_state(self, new_state):
        self._state.exit(visual=self, next_state=new_state)
        old_state = self._state
        self._state = new_state
        self._state.enter(visual=self, old_state=old_state)

    def get_state(self):
        return self._state

    def get_sprite(self):
        return self._sprite

    def update(self):
        return_value = self._state.update(visual=self)
        if return_value is not None:
            self.set_new_state(return_value)

    def ready(self):
        return self._state.ready()
