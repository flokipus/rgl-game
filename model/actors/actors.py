from typing import Dict, Set, ValuesView, KeysView

from gameobj.basegobj import GameObject
from .. import command_channel
from ..turnqueue import turnqueue


class Actors:
    """
    actor <-> (gobj, command_channel)
    actors <-> dict: gobj -> command_channel + turn_queue
    """
    def __init__(self, initial_actors: Dict[GameObject, command_channel.ModelCommandChannel]):
        self._gobj_to_channel = initial_actors
        self._turn_queue = turnqueue.TurnOrderInTime()
        for gobj in self._gobj_to_channel:
            self._turn_queue.add_turn(gobj, 0)

    def add_actor(self, gobj: GameObject, channel: command_channel.ModelCommandChannel) -> None:
        self._gobj_to_channel[gobj] = channel
        max_wait_time = self._turn_queue.last_gobj().time
        self._turn_queue.add_turn(gobj, max_wait_time)

    def add_actor_with_time(self,
                            gobj: GameObject,
                            channel: command_channel.ModelCommandChannel,
                            time_before_turn: int = 0) -> None:
        self._gobj_to_channel[gobj] = channel
        self._turn_queue.add_turn(gobj, time_before_turn)

    def get_command_channel(self, gobj: GameObject) -> command_channel.ModelCommandChannel:
        return self._gobj_to_channel[gobj]

    def remove_actor(self, gobj: GameObject) -> None:
        self._gobj_to_channel.pop(gobj)

    def get_all_gobjs(self) -> Set[GameObject]:
        return set(self._gobj_to_channel.keys())

    def get_all_gobjs_view(self) -> KeysView[GameObject]:
        return self._gobj_to_channel.keys()

    def current_gobj(self) -> GameObject:
        current_turn = self._turn_queue.current_turn()
        return current_turn.gobj

    def make_turn(self, turn_time: int) -> None:
        gobj = self.current_gobj()
        self._turn_queue.pop_actor()
        self._turn_queue.add_turn(gobj, turn_time)
