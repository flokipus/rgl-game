from __future__ import annotations
import pygame
from typing import overload, Union
from collections import namedtuple
from queue import Queue

from utils import Vec2i
from graphics.cell_sprites.sprite_ascii import AsciiCellCreator
from settings.screen import FONT_SIZE, CELL_SIZE, SCREEN_SIZE, CELL_HEIGHT, CELL_WIDTH
from settings import colors


def to_pixel_xy(xy: Vec2i, screen_height) -> tuple:
    x = xy[0]
    y = screen_height - xy[1]
    return x, y


class Tile:
    def __init__(self, sprite: pygame.Surface):
        self.sprite = sprite

    @overload
    def speed_factor(self) -> float: ...

    @overload
    def can_move(self) -> bool: ...

    def speed_factor(self) -> float:
        return 1.0

    def can_move(self) -> bool:
        return True

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

    def get_tile(self, ij: Vec2i) -> Union[None, Tile]:
        if ij in self.tiles:
            return self.tiles[ij]
        else:
            return None

    def set_tile(self, ij: Vec2i, tile: Tile) -> None:
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
            pose = ij - Vec2i(min_i, min_j)
            draw_tile_descartes(tile.sprite, pose, surface)
        return surface


def draw_surf_descartes(what_to_draw: pygame.Surface, pos_left_bot: Vec2i, where_to_draw: pygame.Surface):
    size = where_to_draw.get_size()
    xy = to_pixel_xy(pos_left_bot, size[1])
    xy = xy[0], xy[1] - what_to_draw.get_size()[1]
    where_to_draw.blit(what_to_draw, xy)


def draw_tile_descartes(what_to_draw: pygame.Surface, ij: Vec2i, where_to_draw: pygame.Surface):
    draw_surf_descartes(what_to_draw, ij.dot(Vec2i(CELL_WIDTH, CELL_HEIGHT)), where_to_draw)


def test_tile_map():
    tiles = TileMap()  # EMPTY
    desert_cell_sprite = pygame.Surface(CELL_SIZE)
    desert_cell_sprite.fill(colors.SAND)
    for i in range(8, 15):
        for j in range(18, 23):
            tiles.set_tile(Vec2i(i, j), Tile(desert_cell_sprite))
    for i in range(15, 20):
        tiles.set_tile(Vec2i(i, 18), Tile(desert_cell_sprite))
    for i in range(20, 24):
        for j in range(8, 19):
            tiles.set_tile(Vec2i(i, j), Tile(desert_cell_sprite))
    return tiles


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()

    tile_map = test_tile_map()
    back_sprite = tile_map.to_surface()

    dots = TileMap()
    for ij in tile_map.tiles:
        dot_center = AsciiCellCreator(pygame.font.Font(None, FONT_SIZE), CELL_SIZE).create(
            '.',
            colors.WHITE,
            colors.TRANSPARENT_COLOR
        )
        dots.set_tile(ij, Tile(dot_center))

    MAIN_DISPLAY = pygame.display.set_mode(SCREEN_SIZE)
    MAIN_DISPLAY.fill(colors.BLACK)

    time_end = pygame.time.get_ticks()

    from gameobj.actor import Actor
    from states.actorstates import ActorStand, ActorMove
    from user_input.keyboard_processor import UserKeyboardProcessor, USER_KEYBOARD_EVENTS
    from command.base import MoveCommand

    input_queue = Queue()

    m_spr = AsciiCellCreator(pygame.font.Font(None, FONT_SIZE), CELL_SIZE).create(
        '@',
        colors.WHITE,
        colors.TRANSPARENT_COLOR
    )
    main_hero = Actor(Vec2i(8, 18), ActorStand(), input_queue, m_spr)

    d_spr = AsciiCellCreator(pygame.font.Font(None, FONT_SIZE), CELL_SIZE).create(
        'D',
        colors.BLUE,
        colors.TRANSPARENT_COLOR
    )
    n_spr = AsciiCellCreator(pygame.font.Font(None, FONT_SIZE), CELL_SIZE).create(
        '@',
        colors.BLACK_GREY,
        colors.TRANSPARENT_COLOR
    )

    ACTORS = []
    ACTORS.append(main_hero)

    ActionMove = namedtuple('ActionMove', ['di', 'dj'])

    user_input_proc = UserKeyboardProcessor(0.3)
    MOVE_KEYS = {pygame.K_w, pygame.K_UP, pygame.K_s, pygame.K_DOWN, pygame.K_a, pygame.K_LEFT, pygame.K_d,
                 pygame.K_RIGHT}
    while True:
        # print('------')
        time_begin = pygame.time.get_ticks()
        # print('still_have_ticks: {}'.format(time_begin - time_end))
        # print(time_begin)

        ckey = user_input_proc.process_input(pygame.event.get(USER_KEYBOARD_EVENTS))
        if ckey in MOVE_KEYS:
            print('Move keys')
            di, dj = 0, 0
            if ckey in {pygame.K_UP, pygame.K_w}:
                dj = 1
            elif ckey in {pygame.K_DOWN, pygame.K_s}:
                dj = -1
            elif ckey in {pygame.K_LEFT, pygame.K_a}:
                di = -1
            elif ckey in {pygame.K_RIGHT, pygame.K_d}:
                di = 1
            input_queue.put(ActionMove(di=di, dj=dj))
        if ckey == pygame.K_ESCAPE:
            input_queue = Queue()

        main_hero.request_command()


        MAIN_DISPLAY.fill(colors.BLACK)
        # Layer 0
        for ij in tile_map.tiles:
            draw_tile_descartes(tile_map.get_tile(ij).sprite, ij, MAIN_DISPLAY)

        draw_tile_descartes(main_hero.sprite, main_hero.pos, MAIN_DISPLAY)

        # Layer 1
        for ij in dots.tiles:
            draw_tile_descartes(dots.get_tile(ij).sprite, ij, MAIN_DISPLAY)
        pygame.display.update()

        time_end = pygame.time.get_ticks()
        elapsed = time_end - time_begin

        # print(time_end)
        # print(elapsed)
        # print(clock.get_fps())
        clock.tick(30)
