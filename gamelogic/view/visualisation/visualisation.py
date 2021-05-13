# -*- coding: utf-8 -*-

from __future__ import annotations
import pygame

from common.utils import utils


class Visualisation:
    def __init__(self,
                 sprite: pygame.Surface,
                 layer: int,
                 pixel_xy_offset: utils.Vec2i,
                 state):
        self._state = state
        self._sprite = sprite
        self._layer = layer
        self._corner_xy = pixel_xy_offset
        self._flag_visible = True

    def set_corner_xy(self, new_offset: utils.Vec2i) -> None:
        """Set left bottom corner of MBR of sprite"""
        self._corner_xy = new_offset

    def get_corner_xy(self) -> utils.Vec2i:
        """Get left bottom corner of MBR of sprite"""
        return self._corner_xy

    def update(self) -> None:
        result = self._state.update(visual_owner=self)
        if result is not None:
            self.set_new_state(result)

    def set_new_state(self, new_state) -> None:
        self._state.exit(visual_owner=self, next_state=new_state)
        new_state.enter(visual_owner=self, old_state=self._state)
        self._state = new_state

    def ready(self) -> bool:
        return self._state.ready()

    def get_state(self):
        return self._state

    def get_sprite(self) -> pygame.Surface:
        return self._sprite

    def get_layer(self) -> int:
        return self._layer

    def is_visible(self) -> bool:
        return self._flag_visible

    def set_visibility(self, flag_visible: bool) -> None:
        self._flag_visible = flag_visible
