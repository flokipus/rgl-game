from __future__ import annotations
import pygame
from typing import List, Callable, Any

from graphics.cell_sprites.sprite_ascii import AsciiCellCreator
from map.tilemaps import test_tile_map, TileMap, Tile, draw_tile_descartes
from settings import colors
from settings.screen import FONT_SIZE, CELL_SIZE, SCREEN_SIZE
from utils.utils import Vec2i
from gameobj.actorgobj import Actor
from gameobj.states import ActorStand
from user_input.keyboard_processor import UserKeyboardProcessor, USER_KEYBOARD_EVENTS
from command.command import MoveCommand, Command


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
    def __init__(self, *, data: List[Any] = None, compare: Callable[[Any], Any] = None):
        if data is not None:
            self.data = data
        else:
            self.data = []
        if compare is not None:
            if callable(compare):
                self.compare = compare
            else:
                raise AttributeError('order is not callable')
        self.data.sort(key=self.compare)

    def add_item(self, item) -> None:
        self.data.append(item)
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



    input_queue = list()

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

    ACTORS = list()
    ACTORS.append(main_hero)

    moves_queue = list()
    for actor in ACTORS:
        moves_queue.append(actor)

    EVENT_QUEUE = []

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
            input_queue.append(MoveCommand(Vec2i(di, dj)))
        if ckey == pygame.K_ESCAPE:
            input_queue.clear()

        curr_actor = moves_queue[0]
        if curr_actor.ready_to_move():
            command = curr_actor.request_command()
            if isinstance(command, MoveCommand):
                cur_pos = curr_actor.get_pos()
                next_pos = cur_pos + command.dij
                target_tile = tile_map.get_tile(next_pos)
                if target_tile is not None and target_tile.can_move():
                    # APPLY COMMAND
                    moves_queue.pop(0)
                    curr_actor.handle_command()
                    moves_queue.append(curr_actor)
                    EVENT_QUEUE.append((curr_actor, command))
                    pass

        for actor in ACTORS:
            actor.update()

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
