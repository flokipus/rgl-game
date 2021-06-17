from __future__ import annotations
from typing import List, Callable, Any

from common.gameobj.basegobj import GameObject


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

    def bot_item(self) -> Any:
        item, counter = self.data[0]
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


class GobjWithTime:
    def __init__(self, gobj, time):
        self.gobj = gobj
        self.time = time


class TurnOrderInTime:
    def __init__(self):
        self._move_turns = OrderedQueue(key=lambda x: x.time)

    def add_turn(self, gobj: GameObject, time_before_move: int) -> None:
        binding = GobjWithTime(gobj, time_before_move)
        self._move_turns.add_item(binding)

    def pop_actor(self) -> None:
        binding = self._move_turns.top_item()
        time_passed = binding.time
        raw_data = self._move_turns.raw_data()
        for binding, counter in raw_data:
            binding.time -= time_passed
        self._move_turns.pop_item()

    def current_turn(self) -> GobjWithTime:
        """Just look at current actor"""
        return self._move_turns.top_item()

    def last_gobj(self) -> GobjWithTime:
        return self._move_turns.bot_item()

    def remove_gobj(self, actor: GameObject) -> None:
        self.remove_gobj_by_id(actor.id)

    def remove_gobj_by_id(self, gobj_id: int) -> None:
        raw_data = self._move_turns.raw_data()
        for i, (binding, counter) in enumerate(raw_data):
            gobj: GameObject = binding.gobj
            if gobj.id == gobj_id:
                raw_data.pop(i)
                break
