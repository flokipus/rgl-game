# -*- coding: utf-8 -*-

import pygame
from typing import Dict, Union, ValuesView

from .visualisation import Visualisation
from .visualisation_states import Standing, IVisualState, PassiveStanding
from common.utils import utils
from common.gameobj.basegobj import GameObject
from gamelogic.view.camera import camera, camera_states
from gamelogic.model import model


def adhoc_dot_sprite(tile_size_pixels: utils.Vec2i, boldness: int, transparency: int) -> pygame.Surface:
    dot_sprite: pygame.Surface = pygame.Surface(tile_size_pixels.to_tuple(), flags=pygame.SRCALPHA)
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
        self._camera = camera.Camera(utils.Vec2i(0, 0), camera_states.CameraBaseState())

    def synchronize_with_model(self, new_model: model.ModelGame):
        camera_center = self.cell_ij_to_pixel(new_model.player_character.get_pos())
        self._camera.set_center(camera_center)
        self._player_character = new_model.player_character
        for gobj in new_model.get_actors_gobjs():
            pixel_xy = self.cell_ij_to_pixel(gobj.get_pos())
            visual = Visualisation(sprite=gobj.get_sprite(),
                                   layer=3,
                                   pixel_xy_offset=pixel_xy,
                                   state=Standing(pixel_xy))
            self.set_gobj_visual(gobj, visual)
        for gobj in new_model.get_items_gobjs():
            pixel_xy = self.cell_ij_to_pixel(gobj.get_pos())
            visual = Visualisation(sprite=gobj.get_sprite(), layer=2, pixel_xy_offset=pixel_xy, state=PassiveStanding())
            self.set_gobj_visual(gobj, visual)
        dot_sprite = adhoc_dot_sprite(self._tile_size_pixels, boldness=2, transparency=50)
        for gobj in new_model.get_tile_map().get_all_tiles():
            pixel_xy = self.cell_ij_to_pixel(gobj.get_pos())
            visual = Visualisation(sprite=dot_sprite, layer=1, pixel_xy_offset=pixel_xy, state=PassiveStanding())
            dot_gobj = GameObject(pos=gobj.get_pos())
            self.set_gobj_visual(dot_gobj, visual)
        for gobj in new_model.get_tile_map().get_all_tiles():
            pixel_xy = self.cell_ij_to_pixel(gobj.get_pos())
            visual = Visualisation(sprite=gobj.get_sprite(), layer=0, pixel_xy_offset=pixel_xy, state=PassiveStanding())
            self.set_gobj_visual(gobj, visual)

    def cell_ij_to_pixel(self, ij: utils.Vec2i) -> utils.Vec2i:
        return self._tile_size_pixels.dot(ij)

    def set_gobj_visual(self, gobj: GameObject, visual: Visualisation) -> None:
        self._visuals[gobj] = visual

    def get_gobj_visual(self, gobj: GameObject) -> Visualisation:
        return self._visuals[gobj]

    def remove_gobj_visual(self, gobj: GameObject) -> None:
        self._visuals.pop(gobj)

    def set_visual_state(self, gobj: GameObject, state: IVisualState) -> None:
        self._visuals[gobj].set_new_state(state)

    def get_visual_state(self, gobj: GameObject) -> IVisualState:
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
