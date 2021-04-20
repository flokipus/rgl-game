from __future__ import annotations
import pygame
from time import time
from typing import List, Callable, Any, Union, Tuple, overload
from collections import namedtuple

from model.ai import RandomMoveAI
from command.command import Command, MOVE_ONE_TILE, ExitCommand
from model.command_channel import UserCommandChannel, AICommandChannel
from graphics.cell_sprites.sprite_ascii import AsciiCellCreator
from gameobj.basegobj import GameObject
from map.tilemaps import test_tile_map, Tile
from settings import colors
from settings.screen import FONT_SIZE, CELL_SIZE, SCREEN_SIZE
from utils.utils import Vec2i
from user_input.keyboard_processor import UserKeyboardProcessor


class Event:
    """Empty"""
    pass


class MoveGobjEvent(Event):
    """C-like structure"""
    def __init__(self, gobj: GameObject, ij_before, ij_after):
        self.gobj = gobj
        self.ij_before = ij_before
        self.ij_after = ij_after


class MeeleAttackEvent(Event):
    def __init__(self, who_attack: GameObject, target: GameObject):
        self.who_attack = who_attack
        self.target = target


class GobjDoNothingEvent(Event):
    def __init__(self, who: GameObject):
        self.who = who


class CommandWithCost:
    """C-like structure"""
    def __init__(self, command, cost):
        self.command = command
        self.cost = cost




class BaseState:
    @overload
    def update(self, *, visual: Visualisation) -> Union[None, BaseState]: ...

    @overload
    def enter(self, *, visual: Visualisation, old_state: BaseState) -> None: ...

    @overload
    def exit(self, *, visual: Visualisation, next_state: BaseState) -> None: ...

    @overload
    def ready(self) -> bool: ...

    """Empty implementations
    """
    def update(self, *, visual: Visualisation) -> Union[None, BaseState]:
        pass

    def enter(self, *, visual: Visualisation, old_state: BaseState) -> None:
        pass

    def exit(self, *, visual: Visualisation, next_state: BaseState) -> None:
        pass

    def ready(self) -> bool:
        return True


class Visualisation:
    def __init__(self, sprite: pygame.Surface, pixel_xy_offset: Vec2i = Vec2i(0, 0),
                 state: BaseState = BaseState()):
        self._sprite = sprite
        self._pixel_xy_offset = pixel_xy_offset
        self._state = state

    def set_pixel_xy_offset(self, new_offset: Vec2i):
        self._pixel_xy_offset = new_offset

    def get_pixel_offset(self) -> Vec2i:
        return self._pixel_xy_offset

    def set_new_state(self, new_state: BaseState):
        self._state.exit(visual=self, next_state=new_state)
        old_state = self._state
        self._state = new_state
        self._state.enter(visual=self, old_state=old_state)

    def get_sprite(self):
        return self._sprite

    def update(self):
        return_value = self._state.update(visual=self)
        if return_value is not None:
            self.set_new_state(return_value)

    def ready(self):
        return self._state.ready()


class Moving(BaseState):
    def __init__(self, dxy: Vec2i, time_to_move: float = 0.3):
        self.dxy = dxy
        self.time_to_move = time_to_move
        self.initial_offset_xy = None
        self.time_begin = 0.0

    def update(self, *, visual: Visualisation) -> Union[None, BaseState]:
        current_time = time()
        elapsed_time = current_time - self.time_begin
        r = min(1.0, elapsed_time / self.time_to_move)
        visual.set_pixel_xy_offset((self.initial_offset_xy + self.dxy * r))
        if elapsed_time > self.time_to_move:
            return BaseState()
        else:
            return None

    def enter(self, *, visual: Visualisation, old_state: BaseState) -> None:
        self.time_begin = time()
        self.initial_offset_xy = visual.get_pixel_offset()

    def exit(self, *, visual: Visualisation, next_state: BaseState) -> None:
        pass

    def ready(self) -> bool:
        return False


class ViewGame:
    def __init__(self, model: ModelGame, screen_size: Tuple[int, int], tile_size_pixels: Vec2i):
        self.model = model

        self._screen_size = screen_size
        self._tile_size_pixels = tile_size_pixels
        self.main_display = pygame.display.set_mode(screen_size)

        self._gobjs_to_animations = dict()

        for gobj in self.model.get_all_gobjs():
            pixel_xy = self.cell_ij_to_pixel(gobj.get_pos())
            self._gobjs_to_animations[gobj] = Visualisation(gobj.get_sprite(), pixel_xy_offset=pixel_xy)

        self._we_wait_them = set()
        self.events_to_process = list()

        # TODO: Class for user input!
        self.user_keyboard = UserKeyboardProcessor(delay=0.3)
        self.key_to_action = {pygame.K_UP: MOVE_ONE_TILE['UP'], pygame.K_w: MOVE_ONE_TILE['UP'],
                              pygame.K_DOWN: MOVE_ONE_TILE['DOWN'], pygame.K_s: MOVE_ONE_TILE['DOWN'],
                              pygame.K_LEFT: MOVE_ONE_TILE['LEFT'], pygame.K_a: MOVE_ONE_TILE['LEFT'],
                              pygame.K_RIGHT: MOVE_ONE_TILE['RIGHT'], pygame.K_d: MOVE_ONE_TILE['RIGHT'],
                              pygame.K_SPACE: MOVE_ONE_TILE['WAIT'],
                              pygame.K_ESCAPE: ExitCommand()}

    def is_ready(self) -> bool:
        return len(self._we_wait_them) == 0 and len(self.events_to_process) == 0

    def process_events(self):
        while True:
            if len(self.events_to_process) == 0:
                break
            event = self.events_to_process[0]
            self.events_to_process.pop(0)
            if isinstance(event, MoveGobjEvent):
                dxy = (event.ij_after - event.ij_before).dot(self._tile_size_pixels)
                dxy[1] = -dxy[1]
                self._gobjs_to_animations[event.gobj].set_new_state(Moving(dxy))
                self._we_wait_them.add(event.gobj)

    def update_animations(self):
        for animations in self._gobjs_to_animations.values():
            animations.update()
        to_delete = set()
        for obj in self._we_wait_them:
            if self._gobjs_to_animations[obj].ready():
                to_delete.add(obj)
        self._we_wait_them.difference_update(to_delete)

    def cell_ij_to_pixel(self, ij: Vec2i) -> Vec2i:
        screen_width, screen_height = self._screen_size
        x = ij[0] * self._tile_size_pixels[0]
        y = screen_height - ij[1] * self._tile_size_pixels[1]
        return Vec2i(x, y)

    def get_user_commands(self) -> Union[None, Command]:
        key = self.user_keyboard.process_input()
        if key in self.key_to_action:
            return self.key_to_action[key]
        else:
            return None

    def update(self):
        self.events_to_process += self.model.unload_events()
        self.process_events()
        self.update_animations()
        self.redraw()

    def redraw(self):
        self.main_display.fill(colors.BLACK_GREY)
        layer_0 = []
        layer_1 = []
        for gobj in self.model.get_all_gobjs():
            if isinstance(gobj, Tile):
                layer_0.append(gobj)
            else:
                layer_1.append(gobj)
        for gobj in layer_0:
            if gobj in self._gobjs_to_animations:
                anim = self._gobjs_to_animations[gobj]
                self.main_display.blit(anim.get_sprite(), anim.get_pixel_offset().to_tuple())
        for gobj in layer_1:
            if gobj in self._gobjs_to_animations:
                anim = self._gobjs_to_animations[gobj]
                self.main_display.blit(anim.get_sprite(), anim.get_pixel_offset().to_tuple())
        pygame.display.update()


if __name__ == '__main__':
    """TODO: Decoupling event application form Actors"""
    pygame.init()
    clock = pygame.time.Clock()

    tile_map = test_tile_map()

    actors = dict()

    m_spr = AsciiCellCreator(pygame.font.Font(None, FONT_SIZE), CELL_SIZE).create(
        '@',
        colors.WHITE,
        colors.TRANSPARENT_COLOR
    )
    input_channel = UserCommandChannel()
    main_hero = GameObject(pos=Vec2i(8, 18), name='main_char', sprite=m_spr)
    actors[main_hero] = input_channel

    d_spr = AsciiCellCreator(pygame.font.Font(None, FONT_SIZE), CELL_SIZE).create(
        'D',
        colors.BLUE,
        colors.TRANSPARENT_COLOR
    )
    dragon_gobj = GameObject(pos=Vec2i(10, 18), name='dragon', sprite=d_spr)
    ai_com_chan = AICommandChannel(RandomMoveAI())
    actors[dragon_gobj] = ai_com_chan

    n_spr = AsciiCellCreator(pygame.font.Font(None, FONT_SIZE), CELL_SIZE).create(
        '@',
        colors.BLACK_GREY,
        colors.TRANSPARENT_COLOR
    )
    necro_gobj = GameObject(pos=Vec2i(12, 18), name='necromancer', sprite=n_spr)
    actors[necro_gobj] = ai_com_chan

    model_game = ModelGame(actors, tile_map, user_command_channel=input_channel)
    tile_size_pixels = Vec2i(CELL_SIZE[0], CELL_SIZE[1])
    view_game = ViewGame(model_game, SCREEN_SIZE, tile_size_pixels)

    while True:
        # print('------')
        time_begin = pygame.time.get_ticks()
        # print('still_have_ticks: {}'.format(time_begin - time_end))
        # print(time_begin)

        command_from_user = view_game.get_user_commands()
        if isinstance(command_from_user, ExitCommand):
            exit()
        elif view_game.is_ready():
            model_game.put_user_command(command_from_user)
            model_game.one_turn_tick()

        # View tick
        view_game.update()

        time_end = pygame.time.get_ticks()
        elapsed = time_end - time_begin
        # print(time_end)
        # print(elapsed)
        # print(clock.get_fps())
        clock.tick(30)
