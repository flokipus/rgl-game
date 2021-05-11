import pygame
from typing import Tuple, Dict, Union, List, Set

from common.event.event import GobjEvent
from common.gameobj.basegobj import GameObject
from common.observer.interface import Subject, Observer

from common.utils.user_input.keyboard_processor import UserKeyboardProcessor
from common.utils import utils
from common.state import interface
from gamelogic.model.model import ModelGame
from gamelogic.view.visualisation.visualisation_states.basic import VisualState
from gamelogic.view.visualisation.visualisation_states.derived import Standing
from .visualisation.visualisation import Visualisation
from gamelogic.view.settings.input_settings import KEY_TO_COMMAND, PlayerCommand

from .camera.camera import Camera, CameraBaseState
from .graphics.cell_sprites.sprite_ascii import AsciiCellCreator
from .settings import screen  # FONT_SIZE, CELL_SIZE
from .settings import colors
from .timings.timings import Timings

from .model_event_handler.model_event_handler import ModelEventHandler


pygame.init()
DOT = AsciiCellCreator(pygame.font.Font(None, screen.FONT_SIZE), screen.CELL_SIZE).create(
        '.',
        pygame.Color(255, 255, 255, 155),
        colors.TRANSPARENT_COLOR
    )


class Layers:
    def __init__(self, num_layers: int):
        self._layers = [[] for i in range(num_layers)]

    def add_visualisation(self, layer_num, visualisation):
        self._layers[layer_num].append(visualisation)

    def get_layer(self, i: int) -> List[Visualisation]:
        return self._layers[i]

    def num_layers(self) -> int:
        return len(self._layers)



class Display:
    def __init__(self, screen_size: Tuple[int, int]):
        self._size = utils.Vec2i(*screen_size)
        self._monitor_center = self._size / 2
        self._display = pygame.display.set_mode(screen_size)

    def draw(self, layers: Layers, center: utils.Vec2i) -> None:
        for i in range(layers.num_layers()):
            self.draw_visuals(layers.get_layer(i), center)

    def draw_visuals(self, visualisations: List[Visualisation], center: utils.Vec2i) -> None:
        for vis in visualisations:
            sprite = vis.get_sprite()
            pos = vis.get_corner_xy()
            pos_at_display = self.descartes_to_monitor(pos - center) + self._monitor_center
            self._display.blit(sprite, pos_at_display.to_tuple())

    def descartes_to_monitor(self, xy_desc: utils.Vec2i) -> utils.Vec2i:
        new_xy = xy_desc.copy()
        new_xy[1] = self._size[1] - new_xy[1]
        return new_xy


class ViewGame(Observer, Subject):
    def __init__(self,
                 model: ModelGame,
                 display: Display,
                 tile_size_pixels: Tuple[int, int],
                 timings: Timings):
        Observer.__init__(self)
        Subject.__init__(self)

        self.model = model

        self._timings = timings
        self._gobj_event_handler = ModelEventHandler(view_holder=self)
        self._display = display
        self._vis_layers = Layers(4)
        self._tile_size_pixels = tile_size_pixels

        init_center = self.cell_ij_to_pixel(model.player_character.get_pos())
        self._camera = Camera(init_center, CameraBaseState())

        # Animations class
        self._gobjs_to_animations: Dict[GameObject, Visualisation] = dict()
        for gobj in self.model.get_all_gobjs():
            pixel_xy = self.cell_ij_to_pixel(gobj.get_pos())
            self._gobjs_to_animations[gobj] = Visualisation(sprite=gobj.get_sprite(),
                                                            pixel_xy_offset=pixel_xy,
                                                            state=VisualState())
        for gobj in self.model.get_actors_gobjs():
            self._gobjs_to_animations[gobj].set_new_state(Standing())

        # User interactions with GUI
        # TODO: Class for user input!
        self._user_keyboard = UserKeyboardProcessor(delay=0.3)
        self._key_to_command_name = KEY_TO_COMMAND

    def on_notify(self, subject, event) -> None:
        if isinstance(subject, ModelGame) and isinstance(event, GobjEvent):
            self._gobj_event_handler.add_event(event)
        else:
            raise NotImplemented('Only GobjEvent from ModelGame are implemented atm.')

    @property
    def timings(self) -> Timings:
        return self._timings

    @timings.setter
    def timings(self, new_timings: Timings) -> None:
        if isinstance(new_timings, Timings):
            self._timings = new_timings
        else:
            raise AttributeError('Wrong type of new_timings')

    @property
    def tile_size_pixels(self):
        return self._tile_size_pixels

    def get_player(self) -> GameObject:
        return self.model.player_character

    def is_ready(self) -> bool:
        return self._gobj_event_handler.ready()

    def set_new_animation_state(self, gobj: GameObject, new_state: interface.IState):
        self._gobjs_to_animations[gobj].set_new_state(new_state)

    def get_gobj_visualisation(self, gobj) -> Visualisation:
        return self._gobjs_to_animations[gobj]

    def update_animations(self):
        for animations in self._gobjs_to_animations.values():
            animations.update()

    def cell_ij_to_pixel(self, ij: utils.Vec2i) -> utils.Vec2i:
        screen_width, screen_height = self._screen_size.to_tuple()
        x = ij[0] * self._tile_size_pixels[0]
        y = screen_height - ij[1] * self._tile_size_pixels[1]
        return utils.Vec2i(x, y)

    def cell_ij_to_descartes_pixel(self, ij: utils.Vec2i):
        pass

    def get_user_commands(self) -> Union[None, PlayerCommand]:
        key = self._user_keyboard.process_input()
        if key in self._key_to_command_name:
            return self._key_to_command_name[key]
        else:
            return None

    def update(self):
        self._gobj_event_handler.form_events_block()
        self._gobj_event_handler.apply_events_block()
        self.update_animations()
        self._gobj_event_handler.remove_finished_events()
        self._camera.update()

    def redraw(self):
        center = self._camera.get_center()
        self._display.draw(layers=, center=center)

        self.main_display.fill(colors.BLACK_GREY)
        camera_center = self._camera.get_center() - self._screen_size // 2

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
                pix_pos = anim.get_corner_xy() - camera_center
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
            pix_pos = anim.get_corner_xy() - camera_center
            if flag_to_draw_dot:
                self.main_display.blit(DOT, pix_pos.to_tuple())

        for gobj in layer_1:
            if gobj in self._gobjs_to_animations:
                anim = self._gobjs_to_animations[gobj]
                pix_pos = anim.get_corner_xy() - camera_center
                self.main_display.blit(anim.get_sprite(), pix_pos.to_tuple())
        pygame.display.update()
