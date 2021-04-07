from __future__ import annotations
import pygame
from typing import List, Callable, Any
from collections import namedtuple

from ai.aiprocessor import SimpleAgressiveAI, RandomMoveAI
from command.command import MoveCommand, Command, MOVE_ONE_TILE
from command.command_channel import UICommandChannel, AICommandChannel
from graphics.cell_sprites.sprite_ascii import AsciiCellCreator
from gameobj.basegobj import GameObject
from gameobj.actorgobj import Actor
import gameobj.states as states
from map.tilemaps import test_tile_map, TileMap, Tile, draw_tile_descartes
from settings import colors
from settings.screen import FONT_SIZE, CELL_SIZE, SCREEN_SIZE
from utils.utils import Vec2
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
        item, counter = self.data[-1]
        return item

    def pop_item(self) -> Any:
        """Remove the smallest item in queue"""
        return self.data.pop(-1)

    def empty(self) -> bool:
        return len(self.data) == 0

    def _sort(self):
        """
        Actual key is this:
        for item, counter = self.data[0] the key is the tuple
        (self.compare(item), counter) which is compared lexicographically
        """
        self.data.sort(key=self.__key, reverse=True)

    def raw_data(self):
        return self.data

    def clear(self) -> None:
        self.data.clear()

    def get_compare(self):
        return self.compare

    def delete_items(self, compare: Callable[[Any], Any]) -> None:
        raise NotImplementedError('ALARM!')


class TurnOrderInTime:
    def __init__(self):
        self._data_type = namedtuple('actor_time', ['actor', 'turn_time'])
        self._move_turns = OrderedQueue(key=lambda x: x['turn_time'])

    def add_turn(self, actor: Actor, turn_time: float) -> None:
        binding = {'actor': actor, 'turn_time': turn_time}
        self._move_turns.add_item(binding)

    def pop_actor(self) -> None:
        binding = self._move_turns.top_item()
        time_passed = binding['turn_time']
        raw_data = self._move_turns.raw_data()
        for binding, counter in raw_data:
            binding['turn_time'] -= time_passed
        self._move_turns.pop_item()

    def top_actor(self) -> Actor:
        """Just look at current actor"""
        binding = self._move_turns.top_item()
        return binding['actor']

    def remove_actor(self, actor: Actor) -> None:
        self.remove_actor_by_id(actor.get_gobj().id)

    def remove_actor_by_id(self, gobj_id: int) -> None:
        raw_data = self._move_turns.raw_data()
        for i, (binding, counter) in enumerate(raw_data):
            gobj: GameObject = binding['actor'].get_gobj()
            if gobj.id == gobj_id:
                raw_data.pop(i)
                break


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
    main_hero = GameObject(pos=Vec2(8, 18), name='main_char', sprite=m_spr)
    main_hero_actor = Actor(main_hero, states.Standing(), input_channel)

    d_spr = AsciiCellCreator(pygame.font.Font(None, FONT_SIZE), CELL_SIZE).create(
        'D',
        colors.BLUE,
        colors.TRANSPARENT_COLOR
    )
    dragon_gobj = GameObject(pos=Vec2(10, 18), name='dragon', sprite=d_spr)
    ai_com_chan = AICommandChannel(RandomMoveAI())
    dragon_actor = Actor(dragon_gobj, states.Standing(), ai_com_chan)

    n_spr = AsciiCellCreator(pygame.font.Font(None, FONT_SIZE), CELL_SIZE).create(
        '@',
        colors.BLACK_GREY,
        colors.TRANSPARENT_COLOR
    )
    necro_gobj = GameObject(pos=Vec2(12, 18), name='necromancer', sprite=n_spr)
    necro_actor = Actor(necro_gobj, states.Standing(), ai_com_chan)

    ACTORS = set()
    ACTORS.add(dragon_actor)
    ACTORS.add(main_hero_actor)
    ACTORS.add(necro_actor)

    USER_ACTOR = {main_hero_actor}

    turns_queue = TurnOrderInTime()
    for actor in ACTORS:
        turns_queue.add_turn(actor, 0)

    EVENT_QUEUE = []
    MOVING_NOW = set()
    allow_next_actor = False
    while True:
        # print('------')
        time_begin = pygame.time.get_ticks()
        # print('still_have_ticks: {}'.format(time_begin - time_end))
        # print(time_begin)

        if pygame.event.get([pygame.QUIT]):
            break

        to_delete = []
        for actor in MOVING_NOW:
            if isinstance(actor.get_state(), states.Standing):
                to_delete.append(actor)
        for actor in to_delete:
            MOVING_NOW.remove(actor)
        to_delete.clear()

        if len(MOVING_NOW) == 0:
            allow_next_actor = True
        else:
            allow_next_actor = False

        if allow_next_actor:
            actor: Actor = turns_queue.top_actor()
            if actor not in MOVING_NOW:
                command = actor.request_command()
                if actor == main_hero_actor:
                    if command is None:
                        pass  # wait input
                    elif isinstance(command, MoveCommand):
                        gobj = actor.get_gobj()
                        cur_pos = gobj.get_pos()
                        next_pos = cur_pos + command.dij
                        target_tile = tile_map.get_tile(next_pos)
                        if target_tile is not None:
                            time_cost = target_tile.move_cost()
                            EVENT_QUEUE.append((actor, command, time_cost))
                        else:
                            pass
                else:
                    # NPC case is here!
                    if command is None:
                        command = MOVE_ONE_TILE['WAIT']
                    if isinstance(command, MoveCommand):
                        gobj = actor.get_gobj()
                        cur_pos = gobj.get_pos()
                        next_pos = cur_pos + command.dij
                        target_tile = tile_map.get_tile(next_pos)
                        if target_tile is None:
                            command = MOVE_ONE_TILE['WAIT']
                            time_cost = tile_map.get_tile(cur_pos).move_cost()
                        else:
                            time_cost = target_tile.move_cost()
                        EVENT_QUEUE.append((actor, command, time_cost))

        # Apply events
        for event in EVENT_QUEUE:
            actor, command, time_cost = event
            actor.handle_command(command)
            MOVING_NOW.add(actor)
            turns_queue.remove_actor(actor)
            turns_queue.add_turn(actor, time_cost)
        EVENT_QUEUE.clear()

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
            gobj = actor.get_gobj()
            draw_tile_descartes(gobj.sprite, gobj.get_pos(), MAIN_DISPLAY)

        pygame.display.update()

        time_end = pygame.time.get_ticks()
        elapsed = time_end - time_begin

        # print(time_end)
        # print(elapsed)
        # print(clock.get_fps())
        clock.tick(30)
