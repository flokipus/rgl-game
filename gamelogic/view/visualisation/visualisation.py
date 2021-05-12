from __future__ import annotations
from typing import Dict, ValuesView, Union
import pygame
from pygame import Surface

from common.gameobj.basegobj import GameObject
from common.utils import utils
from common.state import interface
from gamelogic.model.model import ModelGame
from .camera import camera
from .visualisation_states.basic import VisualState
from .visualisation_states.derived import Standing, Moving, BouncingMotion, MeleeAttacking


class VisualStateOwner(interface.IStateOwner):
    def ready(self) -> bool:
        return self._state.ready()


class Visualisation(VisualStateOwner):
    def __init__(self,
                 sprite: pygame.Surface,
                 layer: int,
                 pixel_xy_offset: utils.Vec2i,
                 state: VisualState):
        VisualStateOwner.__init__(self, init_state=state)
        self._sprite = sprite
        self._layer = layer
        self._corner_xy = pixel_xy_offset
        self._flag_visible = True

    def set_corner_xy(self, new_offset: utils.Vec2i):
        """Set left bottom corner of MBR of sprite"""
        self._corner_xy = new_offset

    def get_corner_xy(self) -> utils.Vec2i:
        """Get left bottom corner of MBR of sprite"""
        return self._corner_xy

    def get_state(self) -> VisualState:
        return self._state

    def get_sprite(self):
        return self._sprite

    def get_layer(self) -> int:
        return self._layer

    def is_visible(self) -> bool:
        return self._flag_visible

    def set_visibility(self, flag_visible: bool) -> None:
        self._flag_visible = flag_visible


def adhoc_dot_sprite(tile_size_pixels: utils.Vec2i, boldness: int, transparency: int) -> pygame.Surface:
    dot_sprite: Surface = pygame.Surface(tile_size_pixels.to_tuple(), flags=pygame.SRCALPHA)
    dot_sprite.fill(color=(0, 0, 0, 0))
    tile_center_xy = tile_size_pixels // 2
    for i in range(-boldness, boldness):
        for j in range(-boldness, boldness):
            t = tile_center_xy + utils.Vec2i(1, 0) * i + utils.Vec2i(0, 1) * j
            dot_sprite.set_at(t.to_tuple(), (255, 255, 255, transparency))
    return dot_sprite


class VisualisationsContainer:
    def __init__(self, tile_size_pixels: utils.Vec2i):
        self._visuals: Dict[GameObject, Visualisation] = dict()
        self._player_character: Union[None, GameObject] = None
        self._tile_size_pixels = tile_size_pixels
        self._camera = camera.Camera(utils.Vec2i(0, 0), camera.CameraBaseState())

    def synchronize_with_model(self, model: ModelGame):
        camera_center = self.cell_ij_to_pixel(model.player_character.get_pos())
        self._camera.set_center(camera_center)
        self._player_character = model.player_character
        for gobj in model.get_actors_gobjs():
            pixel_xy = self.cell_ij_to_pixel(gobj.get_pos())
            visual = Visualisation(sprite=gobj.get_sprite(), layer=3, pixel_xy_offset=pixel_xy, state=VisualState())
            visual.set_new_state(Standing())
            self.set_gobj_visual(gobj, visual)
        for gobj in model.get_items_gobjs():
            pixel_xy = self.cell_ij_to_pixel(gobj.get_pos())
            visual = Visualisation(sprite=gobj.get_sprite(), layer=2, pixel_xy_offset=pixel_xy, state=VisualState())
            self.set_gobj_visual(gobj, visual)
        dot_sprite = adhoc_dot_sprite(self._tile_size_pixels, boldness=2, transparency=50)
        for gobj in model.get_tile_map().get_all_tiles():
            pixel_xy = self.cell_ij_to_pixel(gobj.get_pos())
            visual = Visualisation(sprite=dot_sprite, layer=1, pixel_xy_offset=pixel_xy, state=VisualState())
            dot_gobj = GameObject(pos=gobj.get_pos())
            self.set_gobj_visual(dot_gobj, visual)
        for gobj in model.get_tile_map().get_all_tiles():
            pixel_xy = self.cell_ij_to_pixel(gobj.get_pos())
            visual = Visualisation(sprite=gobj.get_sprite(), layer=0, pixel_xy_offset=pixel_xy, state=VisualState())
            self.set_gobj_visual(gobj, visual)

    def cell_ij_to_pixel(self, ij: utils.Vec2i) -> utils.Vec2i:
        return self._tile_size_pixels.dot(ij)

    def set_gobj_visual(self, gobj: GameObject, visual: Visualisation) -> None:
        self._visuals[gobj] = visual

    def get_gobj_visual(self, gobj: GameObject) -> Visualisation:
        return self._visuals[gobj]

    def remove_gobj_visual(self, gobj: GameObject) -> None:
        self._visuals.pop(gobj)

    def set_visual_state(self, gobj: GameObject, state: VisualState) -> None:
        self._visuals[gobj].set_new_state(state)

    def get_visual_state(self, gobj: GameObject) -> VisualState:
        return self._visuals[gobj].get_state()

    def get_all_visuals(self) -> ValuesView[Visualisation]:
        return self._visuals.values()

    def update(self) -> None:
        for visual in self._visuals.values():
            visual.update()
        self._camera.update()

    def get_camera(self) -> camera.Camera:
        return self._camera

    def set_camera(self, new_camera: camera.Camera) -> None:
        self._camera = new_camera


# class VisualisationsContainer:
#     def __init__(self):
#         self._actors: Dict[GameObject, Visualisation] = dict()
#         self._items: Dict[GameObject, Visualisation] = dict()
#         self._tiles: Dict[GameObject, Visualisation] = dict()
#         self._environments: Dict[GameObject, Visualisation] = dict()
#
#     def set_actor_visual(self, gobj: GameObject, visual: Visualisation) -> None:
#         self._actors[gobj] = visual
#
#     def get_actor_visual(self, gobj: GameObject) -> Visualisation:
#         return self._actors[gobj]
#
#     def set_item_visual(self, gobj: GameObject, visual: Visualisation) -> None:
#         self._items[gobj] = visual
#
#     def get_item_visual(self, gobj: GameObject) -> Visualisation:
#         return self._items[gobj]
#
#     def set_tile_visual(self, gobj: GameObject, visual: Visualisation) -> None:
#         self._tiles[gobj] = visual
#
#     def get_tile_visual(self, gobj: GameObject) -> Visualisation:
#         return self._tiles[gobj]
#
#     def get_environment_visual(self, gobj: GameObject) -> Visualisation:
#         return self._environments[gobj]

