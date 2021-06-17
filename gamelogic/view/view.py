# -*- coding: utf-8 -*-

from typing import Tuple, Union

from common.event.event import Event
from common.gameobj.basegobj import GameObject
from common.observer.interface import Subject, Observer

from common.utils.user_input.keyboard_processor import UserKeyboardProcessor
from common.utils import utils
from gamelogic.model.model import ModelGame
from gamelogic.view.settings.input_settings import KEYS_TO_COMMANDS, PlayerCommand
from .visualisation.visualisation_states import IVisualState
from .visualisation.visualisation import Visualisation
from .visualisation.visual_container import VisualisationsContainer
from .display.display import Display
from .timings.timings import Timings
from .handle_events_from_model.model_event_handler import ModelEventHandler

from _DEBUG_perf import PERFOMANCE_DATA


class ViewGame(Observer, Subject):
    def __init__(self,
                 model: ModelGame,
                 screen_size: Tuple[int, int],
                 layers_num: int,
                 tile_size_pixels: Tuple[int, int],
                 timings: Timings):
        Observer.__init__(self)
        Subject.__init__(self)

        self._model = model
        self._timings = timings
        self._display = Display(screen_size, layers_num)

        self._tile_size_pixels = utils.Vec2i(*tile_size_pixels)
        self._visualisations: VisualisationsContainer = VisualisationsContainer(self._tile_size_pixels)
        self._visualisations.synchronize_with_model(model)
        self._gobj_event_handler = ModelEventHandler(timings, self._tile_size_pixels, self._visualisations)

        # User interactions with GUI
        # TODO: Class for user input!
        self._user_keyboard = UserKeyboardProcessor(delay=0.3)
        self._keys_to_commands = KEYS_TO_COMMANDS

    def on_notify(self, subject, event) -> None:
        if isinstance(subject, ModelGame) and isinstance(event, Event):
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
    def tile_size_pixels(self) -> utils.Vec2i:
        return self._tile_size_pixels

    def get_player(self) -> GameObject:
        return self._model.player_character

    def is_ready(self) -> bool:
        return self._gobj_event_handler.ready()

    def set_new_visual_state(self, gobj: GameObject, new_state: IVisualState) -> None:
        self._visualisations.set_visual_state(gobj, new_state)

    def get_gobj_visualisation(self, gobj) -> Visualisation:
        return self._visualisations.get_gobj_visual(gobj)

    def update_visualisations(self):
        self._visualisations.update()

    def cell_ij_to_pixel(self, ij: utils.Vec2i) -> utils.Vec2i:
        x = ij[0] * self._tile_size_pixels[0]
        y = ij[1] * self._tile_size_pixels[1]
        return utils.Vec2i(x, y)

    def get_user_commands(self) -> Union[None, PlayerCommand]:
        key = self._user_keyboard.process_input()
        if key in self._keys_to_commands:
            return self._keys_to_commands[key]
        else:
            return None

    def update(self):
        PERFOMANCE_DATA.start_visuals()
        self._gobj_event_handler.form_events_block()
        self._gobj_event_handler.apply_events_block()
        self.update_visualisations()
        self._gobj_event_handler.remove_finished_events()
        self.redraw()

    def redraw(self):
        self._display.redraw(self._visualisations)
