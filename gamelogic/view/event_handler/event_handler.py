from typing import List, Set, Dict

from common.event.event import GobjEvent, GobjMeleeAttackEvent, GobjWaitEvent
from common.gameobj.basegobj import GameObject
from .eventcallback import apply_event


class BlockOfEvents:
    def __init__(self):
        self.events = list()
        self.participants_istoks: Dict[GameObject, Set[GameObject]] = dict()
        self.participants_all: Set[GameObject] = set()

    def add_event(self, event: GobjEvent) -> None:
        self.events.append(event)
        if not isinstance(event, GobjWaitEvent):
            self.participants_istoks[event.turn_maker] = set()
            self.participants_all.add(event.turn_maker)
        if isinstance(event, GobjMeleeAttackEvent):
            self.participants_istoks[event.turn_maker].add(event.target_for_attack)
            self.participants_all.add(event.target_for_attack)

    def remove_participants_istoks(self, participants_to_delete: Set[GameObject]):
        for gobj in participants_to_delete:
            to_del = self.participants_istoks[gobj]
            self.participants_all.difference_update(to_del)
            self.participants_all.remove(gobj)
            self.participants_istoks.pop(gobj)

    def apply_events(self, game_view):
        for event in self.events:
            apply_event(event, game_view)
        self.events.clear()

    def empty(self) -> bool:
        return len(self.participants_all) == 0


class GobjEventHandler:
    def __init__(self, view_holder):
        self._event_queue: List[GobjEvent] = list()
        self._view_holder = view_holder

        self._block_of_events = BlockOfEvents()

        self.__to_remove_buffer = set()

    def add_event(self, event: GobjEvent) -> None:
        self._event_queue.append(event)

    def update(self):
        self.remove_finished_events()
        self.flush_event_queue()
        self.apply_events_block()

    def remove_finished_events(self):
        self.__to_remove_buffer.clear()
        for gobj in self._block_of_events.participants_istoks:
            visualisation = self._view_holder.get_gobj_visualisation(gobj)
            if visualisation.ready():
                self.__to_remove_buffer.add(gobj)
        self._block_of_events.remove_participants_istoks(self.__to_remove_buffer)

    def is_event_breakable(self, event: GobjEvent) -> bool:
        response = False
        if event.turn_maker in self._block_of_events.participants_all:
            response = True
        elif isinstance(event, GobjMeleeAttackEvent):
            if event.target_for_attack in self._block_of_events.participants_all:
                response = True
        return response

    def flush_event_queue(self):
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
        self._block_of_events.apply_events(self._view_holder)

    def ready(self) -> bool:
        return len(self._event_queue) == 0 and self._block_of_events.empty()

    def time_before_ready(self) -> float:
        pass
