import pygame
from typing import Any, Tuple, Dict, Callable, Union, List

from gameobj.basegobj import GameObject
from user_input.keyboard_processor import UserKeyboardProcessor
from model.model import ModelGame
from .eventcallback import apply_event
from .visualisation import Visualisation
from .visualisaton_state import BaseState
from .input_settings import key_to_command_name, PlayerCommand
from settings import colors
from utils import utils


class ViewGame:
    def __init__(self, model: ModelGame, screen_size: Tuple[int, int], tile_size_pixels: utils.Vec2i):
        self.model = model

        self._screen_size = screen_size
        self._tile_size_pixels = tile_size_pixels
        self.main_display = pygame.display.set_mode(screen_size)

        self._gobjs_to_animations: Dict[GameObject, Visualisation] = dict()
        for gobj in self.model.get_all_gobjs():
            pixel_xy = self.cell_ij_to_pixel(gobj.get_pos())
            self._gobjs_to_animations[gobj] = Visualisation(sprite=gobj.get_sprite(),
                                                            pixel_xy_offset=pixel_xy,
                                                            state=BaseState())

        self._we_wait_them: Dict[GameObject, Callable[[Any], bool]] = dict()
        self._events_to_process = list()

        # TODO: Class for user input!
        self._user_keyboard = UserKeyboardProcessor(delay=0.3)
        self._key_to_command_name = key_to_command_name

    def is_ready(self) -> bool:
        return len(self._we_wait_them) == 0 and len(self._events_to_process) == 0

    @property
    def tile_size_pixels(self):
        return self._tile_size_pixels

    def set_new_animation_state(self, gobj: GameObject, new_state: BaseState):
        self._gobjs_to_animations[gobj].set_new_state(new_state)

    def add_gobj_to_wait(self, gobj: GameObject, condition_callback: Callable[[Any], bool]):
        """We wait until gobj\'s callback doesnt return True"""
        self._we_wait_them[gobj] = condition_callback

    def process_events(self, fr_c):
        flag_event_occurs = False
        for event in self._events_to_process:
            flag_event_occurs = True
            apply_event(event_occured=event, game_view=self)
            # print('View has processed event: {}'.format(event.who_am_i()))
        if flag_event_occurs:
            print('view process events frame:', fr_c)
        self._events_to_process.clear()

    def update_animations(self):
        for animations in self._gobjs_to_animations.values():
            animations.update()
        to_delete = set()
        for obj in self._we_wait_them:
            obj_visual_state = self._gobjs_to_animations[obj].get_state()
            if self._we_wait_them[obj](obj_visual_state):
                to_delete.add(obj)
        for obj in to_delete:
            self._we_wait_them.pop(obj)

    def cell_ij_to_pixel(self, ij: utils.Vec2i) -> utils.Vec2i:
        screen_width, screen_height = self._screen_size
        x = ij[0] * self._tile_size_pixels[0]
        y = screen_height - ij[1] * self._tile_size_pixels[1]
        return utils.Vec2i(x, y)

    def get_user_commands(self) -> Union[None, PlayerCommand]:
        key = self._user_keyboard.process_input()
        if key in self._key_to_command_name:
            return self._key_to_command_name[key]
        else:
            return None

    def update(self, fr_c):
        self._events_to_process += self.model.unload_events()
        self.process_events(fr_c)
        self.update_animations()
        self.redraw()

    def redraw(self):
        self.main_display.fill(colors.BLACK_GREY)
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
                self.main_display.blit(anim.get_sprite(), anim.get_pixel_offset().to_tuple())
        for gobj in layer_1:
            if gobj in self._gobjs_to_animations:
                anim = self._gobjs_to_animations[gobj]
                self.main_display.blit(anim.get_sprite(), anim.get_pixel_offset().to_tuple())
        pygame.display.update()
