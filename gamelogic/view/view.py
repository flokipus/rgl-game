import pygame
import time
import math
from typing import Any, Tuple, Dict, Callable, Union, List, Set

from common.gameobj.basegobj import GameObject
from common.event import event
from common.utils.user_input.keyboard_processor import UserKeyboardProcessor
from common.utils import utils
from common.state import interface
from gamelogic.model.model import ModelGame
from .graphics.cell_sprites.sprite_ascii import AsciiCellCreator
from .settings import screen  # FONT_SIZE, CELL_SIZE
from .eventcallback import apply_event
from .visualisation import Visualisation
from .visualstate.basic import VisualState
from .input_settings import key_to_command_name, PlayerCommand
from .settings import colors



pygame.init()
DOT = AsciiCellCreator(pygame.font.Font(None, screen.FONT_SIZE), screen.CELL_SIZE).create(
        '.',
        pygame.Color(255, 255, 255, 155),
        colors.TRANSPARENT_COLOR
    )


class Timings:
    def __init__(self, time_to_move: float, time_to_attack: float, fps: int):
        self._time_to_move = time_to_move
        self._time_to_attack = time_to_attack
        self._fps = fps

    @property
    def time_to_move(self):
        return self._time_to_move

    @property
    def time_to_attack(self):
        return self._time_to_attack

    @property
    def fps(self):
        return self._fps


class ViewGame:
    def __init__(self, model: ModelGame, screen_size: Tuple[int, int], tile_size_pixels: utils.Vec2i, fps: int):
        self.model = model

        # Timings class
        self._time_to_move = 0.3
        self._time_to_attack = 0.3
        self._fps = fps

        # Camera class
        self._center = self.cell_ij_to_pixel(model.player_character.get_pos())

        # Display class
        self._screen_size = utils.Vec2i(screen_size[0], screen_size[1])
        self._tile_size_pixels = tile_size_pixels
        self.main_display = pygame.display.set_mode(screen_size)

        # Animations class
        self._gobjs_to_animations: Dict[GameObject, Visualisation] = dict()
        for gobj in self.model.get_all_gobjs():
            pixel_xy = self.cell_ij_to_pixel(gobj.get_pos())
            self._gobjs_to_animations[gobj] = Visualisation(sprite=gobj.get_sprite(),
                                                            pixel_xy_offset=pixel_xy,
                                                            state=VisualState())

        # Event handler
        self._we_wait_them: Set[GameObject] = set()
        self._events_to_process = list()

        # User interactions with GUI
        # TODO: Class for user input!
        self._user_keyboard = UserKeyboardProcessor(delay=0.3)
        self._key_to_command_name = key_to_command_name

    @property
    def time_to_move(self) -> float:
        return self._time_to_move

    @property
    def time_to_attack(self) -> float:
        return self._time_to_attack

    @property
    def tile_size_pixels(self):
        return self._tile_size_pixels

    @property
    def fps(self) -> int:
        return self._fps

    def is_ready(self) -> bool:
        return len(self._we_wait_them) == 0 and len(self._events_to_process) == 0

    def set_new_animation_state(self, gobj: GameObject, new_state: interface.IState):
        self._gobjs_to_animations[gobj].set_new_state(new_state)

    def get_gobj_visualisation(self, gobj) -> Visualisation:
        return self._gobjs_to_animations[gobj]

    def add_gobj_to_wait_animation(self, gobj: GameObject):
        """We wait until gobj\'s animation returns ready()=True"""
        self._we_wait_them.add(gobj)

    def process_events(self):
        for item_event in self._events_to_process:
            apply_event(event_occured=item_event, game_view=self)
        self._events_to_process.clear()

    def update_animations(self):
        for animations in self._gobjs_to_animations.values():
            animations.update()
        to_delete = set()
        for obj in self._we_wait_them:
            anim = self._gobjs_to_animations[obj]
            if anim.ready():
                to_delete.add(obj)
        for obj in to_delete:
            self._we_wait_them.remove(obj)

    def cell_ij_to_pixel(self, ij: utils.Vec2i) -> utils.Vec2i:
        screen_width, screen_height = self._screen_size.to_tuple()
        x = ij[0] * self._tile_size_pixels[0]
        y = screen_height - ij[1] * self._tile_size_pixels[1]
        return utils.Vec2i(x, y)

    def get_user_commands(self) -> Union[None, PlayerCommand]:
        # return self._key_to_command_name[pygame.K_d]
        key = self._user_keyboard.process_input()
        if key in self._key_to_command_name:
            return self._key_to_command_name[key]
        else:
            return None

    def update(self, new_events: Union[None, List[event.Event]]):
        if new_events is not None:
            self._events_to_process += new_events
        self.process_events()
        self.update_animations()
        self.redraw()

    def redraw(self):
        self.main_display.fill(colors.BLACK_GREY)
        pl_gobj = self.model.player_character

        camera_center = self._gobjs_to_animations[pl_gobj].get_pixel_offset() - self._screen_size/2

        layer_0: List[GameObject] = []
        layer_1: List[GameObject] = []
        tile_map = self.model.get_tile_map()
        for gobj in tile_map.get_all_tiles():
            layer_0.append(gobj)
        actors = self.model.get_actors()
        for gobj in actors.get_all_gobjs_view():
            layer_1.append(gobj)
        # Draw layer by layer
        for gobj in layer_0:
            if gobj in self._gobjs_to_animations:
                anim = self._gobjs_to_animations[gobj]
                pix_pos = anim.get_pixel_offset() - camera_center
                self.main_display.blit(anim.get_sprite(), pix_pos.to_tuple())
        # Draw aux dots
        for gobj in tile_map.get_all_tiles():
            ij = gobj.get_pos()
            flag_to_draw_dot = True
            for gactor in actors.get_all_gobjs_view():
                if self._gobjs_to_animations[gactor].ready() and gactor.get_pos() == ij:
                    flag_to_draw_dot = False
                    break
            anim = self._gobjs_to_animations[gobj]
            pix_pos = anim.get_pixel_offset() - camera_center
            if flag_to_draw_dot:
                self.main_display.blit(DOT, pix_pos.to_tuple())
        for gobj in layer_1:
            if gobj in self._gobjs_to_animations:
                anim = self._gobjs_to_animations[gobj]
                pix_pos = anim.get_pixel_offset() - camera_center
                self.main_display.blit(anim.get_sprite(), pix_pos.to_tuple())
        pygame.display.update()
