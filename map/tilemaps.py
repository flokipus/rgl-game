from __future__ import annotations
import pygame
from typing import overload, Union
from collections import namedtuple
from queue import Queue

from utils.utils import Vec2
from graphics.cell_sprites.sprite_ascii import AsciiCellCreator
from settings.screen import FONT_SIZE, CELL_SIZE, SCREEN_SIZE, CELL_HEIGHT, CELL_WIDTH
from settings import colors


def to_pixel_xy(xy: Vec2, screen_height) -> tuple:
    x = xy[0]
    y = screen_height - xy[1]
    return x, y


class Tile:
    def __init__(self, sprite: pygame.Surface):
        self.sprite = sprite

    @overload
    def move_cost(self) -> float: ...

    def move_cost(self) -> float:
        """Default cost"""
        return 100.0

    @classmethod
    def empty_tile(cls):
        return Tile(pygame.Surface((CELL_WIDTH, CELL_HEIGHT)))


class TileMap:
    def __init__(self, input_tiles: Union[None, dict] = None):
        if input_tiles is None:
            self.tiles = dict()
        elif isinstance(input_tiles, dict):
            self.tiles = input_tiles
        else:
            raise AttributeError('Wrong tiles container type. Expected dict, given is {}'.format(type(input_tiles)))

    def get_tile(self, ij: Vec2) -> Union[None, Tile]:
        if ij in self.tiles:
            return self.tiles[ij]
        else:
            return None

    def set_tile(self, ij: Vec2, tile: Tile) -> None:
        self.tiles[ij] = tile

    def to_surface(self) -> pygame.Surface:
        """TODO: write more optimal traversy over map
        """
        max_i, min_i = max([ij[0] for ij in self.tiles.keys()]), min([ij[0] for ij in self.tiles.keys()])
        max_j, min_j = max([ij[1] for ij in self.tiles.keys()]), min([ij[1] for ij in self.tiles.keys()])
        surf_size = CELL_WIDTH * (max_i - min_i + 1), CELL_HEIGHT * (max_j - min_j + 1)
        surface = pygame.Surface(surf_size)
        for ij in self.tiles:
            tile = self.tiles[ij]
            pose = ij - Vec2(min_i, min_j)
            draw_tile_descartes(tile.sprite, pose, surface)
        return surface


def draw_surf_descartes(what_to_draw: pygame.Surface, pos_left_bot: Vec2, where_to_draw: pygame.Surface):
    size = where_to_draw.get_size()
    xy = to_pixel_xy(pos_left_bot, size[1])
    xy = xy[0], xy[1] - what_to_draw.get_size()[1]
    where_to_draw.blit(what_to_draw, xy)


def draw_tile_descartes(what_to_draw: pygame.Surface, ij: Vec2, where_to_draw: pygame.Surface):
    draw_surf_descartes(what_to_draw, ij.dot(Vec2(CELL_WIDTH, CELL_HEIGHT)), where_to_draw)


def test_tile_map():
    tiles = TileMap()  # EMPTY
    desert_cell_sprite = pygame.Surface(CELL_SIZE)
    desert_cell_sprite.fill(colors.SAND)
    for i in range(8, 15):
        for j in range(18, 23):
            tiles.set_tile(Vec2(i, j), Tile(desert_cell_sprite))
    for i in range(15, 20):
        tiles.set_tile(Vec2(i, 18), Tile(desert_cell_sprite))
    for i in range(20, 24):
        for j in range(8, 19):
            tiles.set_tile(Vec2(i, j), Tile(desert_cell_sprite))
    return tiles
