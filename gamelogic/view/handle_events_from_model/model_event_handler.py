from typing import List, Set, Dict

from common.event.event import GobjEvent, GobjMeleeAttackEvent, GobjWaitEvent, GobjMoveEvent
from common.gameobj.basegobj import GameObject
from common.utils import utils
from gamelogic.view.visualisation.visualisation import VisualisationsContainer
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
        self.busy_gobjs_adjs: Dict[GameObject, Set[GameObject]] = dict()
        self.all_busy_gobjs: Set[GameObject] = set()

    def __contains__(self, item: GameObject) -> bool:
        return item in self.all_busy_gobjs

    def add_event(self, event: GobjEvent) -> None:
        """Добавить эвент в блок. При этом, добавляются также соответствующие занятые объекты"""
        self.events.append(event)
        if not isinstance(event, GobjWaitEvent):
            self.busy_gobjs_adjs[event.turn_maker] = set()
            self.all_busy_gobjs.add(event.turn_maker)
        if isinstance(event, GobjMeleeAttackEvent):
            self.busy_gobjs_adjs[event.turn_maker].add(event.target_for_attack)
            self.all_busy_gobjs.add(event.target_for_attack)

    def remove_busy_src(self, participants_to_delete: Set[GameObject]):
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
        self._event_queue: List[GobjEvent] = list()
        self._block_of_events = BlockOfEvents()
        self._callbacker = GobjEventsCallbacks(timings, tile_size_pixels)
        self._visualisations = visualisations
        self.__to_remove_buffer = set()

    def add_event(self, event: GobjEvent) -> None:
        self._event_queue.append(event)

    def remove_finished_events(self):
        self.__to_remove_buffer.clear()
        for gobj in self._block_of_events.busy_gobjs_adjs:
            visualisation = self._visualisations.get_gobj_visual(gobj)
            if visualisation.ready():
                self.__to_remove_buffer.add(gobj)
        self._block_of_events.remove_busy_src(self.__to_remove_buffer)

    def is_event_breakable(self, event: GobjEvent) -> bool:
        response = False
        if event.turn_maker in self._block_of_events:
            response = True
        elif isinstance(event, GobjMeleeAttackEvent):
            if event.target_for_attack in self._block_of_events.all_busy_gobjs:
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
