import pygame

from common.utils import utils
from common.state import interface
from gamelogic.view.visualisation.visualisation_states.basic import VisualState


class VisualStateOwner(interface.IStateOwner):
    def ready(self) -> bool:
        return self._state.ready()


class Visualisation(VisualStateOwner):
    def __init__(self,
                 sprite: pygame.Surface,
                 pixel_xy_offset: utils.Vec2i,
                 state: VisualState):
        self._sprite = sprite
        self._corner_xy = pixel_xy_offset
        VisualStateOwner.__init__(self, init_state=state)

    def set_corner_xy(self, new_offset: utils.Vec2i):
        """Set left bottom corner of MBR of sprite"""
        self._corner_xy = new_offset

    def get_corner_xy(self) -> utils.Vec2i:
        """Get left bottom corner of MBR of sprite"""
        return self._corner_xy

    def get_state(self):
        return self._state

    def get_sprite(self):
        return self._sprite
