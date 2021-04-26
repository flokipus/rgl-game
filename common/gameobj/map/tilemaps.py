from __future__ import annotations
import pygame
from typing import overload, Union, Dict, ValuesView

from common.gameobj.basegobj import GameObject
from common.utils.utils import Vec2i
from gamelogic.view.settings import screen
from gamelogic.view.settings import colors


def to_pixel_xy(xy: Vec2i, screen_height) -> tuple:
    x = xy[0]
    y = screen_height - xy[1]
    return x, y


class Tile(GameObject):
    def __init__(self, *, pos: Vec2i, name: str = '', sprite: Union[None, pygame.Surface] = None):
        GameObject.__init__(self, pos=pos, name=name, sprite=sprite)

    @overload
    def move_cost(self) -> int: ...

    def move_cost(self) -> int:
        """Default cost"""
        return 100

    @classmethod
    def empty_tile(cls, pos: Vec2i = Vec2i(0, 0), name: str = ''):
        return Tile(pos=pos, name=name, sprite=pygame.Surface((screen.CELL_WIDTH, screen.CELL_HEIGHT)))


class TileMap:
    def __init__(self, input_tiles: Union[None, Dict[Vec2i, Tile]] = None):
        if input_tiles is None:
            self.tiles = dict()
        elif isinstance(input_tiles, dict):
            self.tiles = input_tiles
        else:
            raise AttributeError('Wrong tiles container type. Expected dict, given is {}'.format(type(input_tiles)))

    def get_tile(self, ij: Vec2i) -> Union[None, Tile]:
        if ij in self.tiles:
            return self.tiles[ij]
        else:
            return None

    def set_tile(self, ij: Vec2i, tile: Tile) -> None:
        if tile.get_pos() != ij:
            tile.set_pos(ij)
        self.tiles[ij] = tile

    def get_all_tiles(self) -> ValuesView[Tile]:
        return self.tiles.values()

    # def to_surface(self) -> pygame.Surface:
    #     """TODO: write more optimal traversy over map
    #     """
    #     max_i, min_i = max([ij[0] for ij in self.tiles.keys()]), min([ij[0] for ij in self.tiles.keys()])
    #     max_j, min_j = max([ij[1] for ij in self.tiles.keys()]), min([ij[1] for ij in self.tiles.keys()])
    #     surf_size = CELL_WIDTH * (max_i - min_i + 1), CELL_HEIGHT * (max_j - min_j + 1)
    #     surface = pygame.Surface(surf_size)
    #     for ij in self.tiles:
    #         tile = self.tiles[ij]
    #         pose = ij - Vec2(min_i, min_j)
    #         draw_tile_descartes(tile.get_sprite(), pose, surface)
    #     return surface

    def copy(self) -> TileMap:
        return TileMap(self.tiles.copy())


def draw_surf_descartes(what_to_draw: pygame.Surface, pos_left_bot: Vec2i, where_to_draw: pygame.Surface):
    size = where_to_draw.get_size()
    xy = to_pixel_xy(pos_left_bot, size[1])
    xy = xy[0], xy[1] - what_to_draw.get_size()[1]
    where_to_draw.blit(what_to_draw, xy)


def draw_tile_descartes(what_to_draw: pygame.Surface, ij: Vec2i, where_to_draw: pygame.Surface):
    draw_surf_descartes(what_to_draw, ij.dot(Vec2i(screen.CELL_WIDTH, screen.CELL_HEIGHT)), where_to_draw)


def test_tile_map():
    tiles = TileMap()  # EMPTY
    desert_cell_sprite = pygame.Surface(screen.CELL_SIZE)
    desert_cell_sprite.fill(colors.SAND)
    for i in range(8, 15):
        for j in range(18, 23):
            pos = Vec2i(i, j)
            tiles.set_tile(pos, Tile(pos=pos, name='sand_sprite', sprite=desert_cell_sprite))
    for i in range(15, 20):
        pos = Vec2i(i, 18)
        tiles.set_tile(pos, Tile(pos=pos, name='sand_sprite', sprite=desert_cell_sprite))
    for i in range(20, 24):
        for j in range(8, 19):
            pos = Vec2i(i, j)
            tiles.set_tile(pos, Tile(pos=pos, name='sand_sprite', sprite=desert_cell_sprite))
    return tiles
