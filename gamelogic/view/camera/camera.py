# -*- coding: utf-8 -*-

from common.utils import utils


class Camera:
    def __init__(self,
                 init_center_pixels: utils.Vec2i,
                 init_state) -> None:
        self._state = init_state
        self._center_pixels = init_center_pixels

    def get_center(self) -> utils.Vec2i:
        return self._center_pixels

    def set_center(self, new_center: utils.Vec2i) -> None:
        self._center_pixels = new_center

    def update(self):
        result = self._state.update(camera_owner=self)
        if result is not None:
            self.set_new_state(result)

    def set_new_state(self, new_state):
        self._state.exit(camera_owner=self, next_state=new_state)
        new_state.enter(camera_owner=self, old_state=self._state)
        self._state = new_state

    def ready(self) -> bool:
        return self._state.ready()
