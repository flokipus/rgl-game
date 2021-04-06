from __future__ import annotations
import pygame
from typing import List, Callable, Any
from collections import namedtuple

from ai.aiprocessor import SimpleAgressiveAI
from command.command_channel import UICommandChannel, AICommandChannel
from command.command import MoveCommand
from graphics.cell_sprites.sprite_ascii import AsciiCellCreator
from gameobj.actorgobj import Actor
from gameobj.states import ActorStand
from map.tilemaps import test_tile_map, TileMap, Tile, draw_tile_descartes
from settings import colors
from settings.screen import FONT_SIZE, CELL_SIZE, SCREEN_SIZE
from utils.utils import Vec2i
from user_input.keyboard_processor import UserKeyboardProcessor


class ActorTurn:
    def __init__(self, actor, rest_time):
        self.actor = actor
        self.rest_time = rest_time

    def __le__(self, other: ActorTurn) -> bool:
        return self.rest_time <= other.rest_time

    def __lt__(self, other: ActorTurn) -> bool:
        return self.rest_time < other.rest_time

    def __ge__(self, other: ActorTurn) -> bool:
        return self.rest_time >= other.rest_time

    def __gt__(self, other: ActorTurn) -> bool:
        return self.rest_time > other.rest_time


class OrderedQueue:
    def __init__(self, *, data: List[Any] = None, key: Callable[[Any], Any] = None):
        self.__counter = 0
        if data is not None:
            self.data = data
        else:
            self.data = []
        if key is not None:
            if callable(key):
                self.compare = key
                self.__key = lambda x: (self.compare(x[0]), x[1])
            else:
                raise AttributeError('order is not callable')
        self.data.sort(key=self.__key)

    def add_item(self, item) -> None:
        self.data.append((item, self.__counter))
        self.__counter += 1
        self._sort()

    def top_item(self) -> Any:
        """Return the smallest item in queue"""
        return self.data[-1]

    def pop_item(self) -> Any:
        """Remove the smallest item in queue"""
        return self.data.pop(-1)

    def empty(self) -> bool:
        return len(self.data) == 0

    def _sort(self):
        self.data.sort(key=self.compare, reverse=True)

    def clear(self) -> None:
        self.data.clear()

    def delete_items(self, compare: Callable[[Any], Any]) -> None:
        raise NotImplementedError('ALARM!')


if __name__ == '__main__':

    """TODO: Decoupling event application form Actors"""

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

    m_spr = AsciiCellCreator(pygame.font.Font(None, FONT_SIZE), CELL_SIZE).create(
        '@',
        colors.WHITE,
        colors.TRANSPARENT_COLOR
    )
    input_channel = UICommandChannel(UserKeyboardProcessor(delay=0.3))
    main_hero = Actor(Vec2i(8, 18), ActorStand(), input_channel, m_spr)

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
    ai_com_chan = AICommandChannel(SimpleAgressiveAI(None))
    dragon = Actor(Vec2i(10, 18), ActorStand(), ai_com_chan, d_spr)

    ACTORS = list()
    ACTORS.append(main_hero)
    ACTORS.append(dragon)

    moves_queue = OrderedQueue(key=lambda x: x[1])
    for actor in ACTORS:
        moves_queue.add_item((actor, 0))

    EVENT_QUEUE = []
    while True:
        # print('------')
        time_begin = pygame.time.get_ticks()
        # print('still_have_ticks: {}'.format(time_begin - time_end))
        # print(time_begin)

        if pygame.event.get([pygame.QUIT]):
            break

        curr_actor = moves_queue.top_item()[0][0]
        if curr_actor.ready_to_move():
            command = curr_actor.request_command()
            if isinstance(command, MoveCommand):
                cur_pos = curr_actor.get_pos()
                next_pos = cur_pos + command.dij
                target_tile = tile_map.get_tile(next_pos)
                if target_tile is not None and target_tile.can_move():
                    # APPLY COMMAND
                    moves_queue.pop_item()
                    curr_actor.handle_command()
                    moves_queue.add_item((curr_actor, 0))
                    EVENT_QUEUE.append((curr_actor, command))
                    pass

        for actor in ACTORS:
            actor.update()

        ### DRAWING ###
        MAIN_DISPLAY.fill(colors.BLACK)
        # Layer 0
        for ij in tile_map.tiles:
            draw_tile_descartes(tile_map.get_tile(ij).sprite, ij, MAIN_DISPLAY)
        draw_tile_descartes(main_hero.sprite, main_hero.pos, MAIN_DISPLAY)
        # Layer 1
        for ij in dots.tiles:
            draw_tile_descartes(dots.get_tile(ij).sprite, ij, MAIN_DISPLAY)
        for actor in ACTORS:
            draw_tile_descartes(actor.sprite, actor.get_pos(), MAIN_DISPLAY)

        pygame.display.update()

        time_end = pygame.time.get_ticks()
        elapsed = time_end - time_begin

        # print(time_end)
        # print(elapsed)
        # print(clock.get_fps())
        clock.tick(30)
