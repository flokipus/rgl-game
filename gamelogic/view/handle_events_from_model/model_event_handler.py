# -*- coding: utf-8 -*-

from typing import List, Set, Dict

from common.event import event as m_event
from common.gameobj.characters.base_character import Character
from common.utils import utils
from gamelogic.view.visualisation.visual_container import VisualisationsContainer
from gamelogic.view.timings.timings import Timings
from .eventcallback import GobjEventsCallbacks


class BlockOfEvents:
    """
    events:          набор всех эвентов в данном блоке

    busy_gobjs_adjs: dict -- словарь зависимостей gameobject'ов, занятых в эвентах
                    Например, если gobj1 атакует gobj2, то в эвентах заняты gobj1 и gobj2 (точнее, соотв. им
                    визуализации), при этом, если gobj1 проиграл свою анимацию атаки, то освобождается как
                    gobj1, так и gobj2.

    all_busy_gobjs: все занятые в эвентах данного блока объекты
    """

    def __init__(self):
        self.events = list()
        self.busy_gobjs_adjs: Dict[Character, Set[Character]] = dict()
        self.all_busy_gobjs: Set[Character] = set()

    def __contains__(self, item: Character) -> bool:
        return item in self.all_busy_gobjs

    def add_event(self, event: m_event.Event) -> None:
        """Добавить эвент в блок. При этом, добавляются также соответствующие занятые объекты"""
        self.events.append(event)
        if isinstance(event, m_event.CharacterMadeMeleeAttack):
            if event.who in self.busy_gobjs_adjs:
                self.busy_gobjs_adjs[event.who].add(event.whom)
            else:
                self.busy_gobjs_adjs[event.who] = {event.whom}
            self.all_busy_gobjs.add(event.who)
            self.all_busy_gobjs.add(event.whom)
        if isinstance(event, m_event.CharacterMadeMove) or isinstance(event, m_event.CharacterDied):
            self.busy_gobjs_adjs[event.who] = set()
            self.all_busy_gobjs.add(event.who)

    def remove_busy_src(self, participants_to_delete: Set[Character]):
        """Удаляет все GameObject'ы из gobjs_to_delete. При этом, каждый gobj из gobjs_to_delete должен быть
        "порождающим"
        """
        for gobj in participants_to_delete:
            to_del = self.busy_gobjs_adjs[gobj]
            self.all_busy_gobjs.difference_update(to_del)
            self.all_busy_gobjs.remove(gobj)
            self.busy_gobjs_adjs.pop(gobj)

    def empty(self) -> bool:
        return len(self.all_busy_gobjs) == 0


class ModelEventHandler:
    def __init__(self,
                 timings: Timings,
                 tile_size_pixels: utils.Vec2i,
                 visualisations: VisualisationsContainer):
        self._event_queue: List[Character] = list()
        self._block_of_events = BlockOfEvents()
        self._callbacker = GobjEventsCallbacks(timings, tile_size_pixels)
        self._visualisations = visualisations
        self.__to_remove_buffer = set()

    def add_event(self, event: Character) -> None:
        self._event_queue.append(event)

    def remove_finished_events(self):
        self.__to_remove_buffer.clear()
        for gobj in self._block_of_events.busy_gobjs_adjs:
            try:
                visualisation = self._visualisations.get_gobj_visual(gobj)
                if visualisation.ready():
                    self.__to_remove_buffer.add(gobj)
            except KeyError:
                self.__to_remove_buffer.add(gobj)
        self._block_of_events.remove_busy_src(self.__to_remove_buffer)

    def is_event_breakable(self, event: m_event.Event) -> bool:
        response = False
        if isinstance(event, m_event.CharacterMadeMove):
            if event.who in self._block_of_events:
                response = True
        elif isinstance(event, m_event.CharacterDied):
            if event.who in self._block_of_events:
                response = True
        elif isinstance(event, m_event.CharacterMadeMeleeAttack):
            if event.who in self._block_of_events:
                response = True
            if event.whom in self._block_of_events.all_busy_gobjs:
                response = True
        return response

    def form_events_block(self):
        counter_events = 0
        for event in self._event_queue:
            if self.is_event_breakable(event):
                break
            else:
                self._block_of_events.add_event(event)
                counter_events += 1
        if counter_events > 0:
            self._event_queue = self._event_queue[counter_events:]

    def apply_events_block(self):
        for event in self._block_of_events.events:
            self._callbacker.apply_event(event, self._visualisations)
        self._block_of_events.events.clear()

    def ready(self) -> bool:
        return len(self._event_queue) == 0 and self._block_of_events.empty()

    def time_before_ready(self) -> float:
        raise NotImplementedError()
