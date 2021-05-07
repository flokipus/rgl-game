import pygame

from common.utils import utils
from common.state import interface
from gamelogic.view.visualisation.visualisation_states.basic import VisualState


class VisualStateOwner(interface.IStateOwner):
    def ready(self) -> bool:
        return type(self._state) == VisualState


class Visualisation(VisualStateOwner):
    def __init__(self,
                 sprite: pygame.Surface,
                 pixel_xy_offset: utils.Vec2i,
                 state: VisualState):
        self._sprite = sprite
        self._pixel_xy_offset = pixel_xy_offset
        VisualStateOwner.__init__(self, init_state=state)

    def set_pixel_xy_offset(self, new_offset: utils.Vec2i):
        self._pixel_xy_offset = new_offset

    def get_pixel_offset(self) -> utils.Vec2i:
        return self._pixel_xy_offset

    def get_state(self):
        return self._state

    def get_sprite(self):
        return self._sprite
