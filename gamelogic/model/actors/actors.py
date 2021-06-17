from typing import Dict, Set, KeysView

from common.gameobj.characters.base_character import Character
from .. import intention_channel
from ..turnqueue import turnqueue


class Actors:
    """
    Актором может быть только Character (наследник от GameObject); ибо аве SOLID!!1
    actor: по сути это синоним паре (character, command_channel); в command_channel поступают команды для character'а
        на выполнение, которые потом исполняются моделью
    Класс Actors инкапсулирует в себя акторов (в виде словаря, character->command_channel) и очередь их ходов,
        _turn_queue. На самом деле, название класса не тру, надо другое придумать.
    """
    def __init__(self, initial_actors: Dict[Character, intention_channel.IntentionChannel]):
        self._actor_to_channel = initial_actors
        self._turn_queue = turnqueue.TurnOrderInTime()
        for actor in self._actor_to_channel:
            self._turn_queue.add_turn(actor, 0)

    def add_actor(self, actor: Character, channel: intention_channel.IntentionChannel) -> None:
        self._actor_to_channel[actor] = channel
        max_wait_time = self._turn_queue.last_gobj().time
        self._turn_queue.add_turn(actor, max_wait_time)

    def add_actor_with_time(self,
                            actor: Character,
                            channel: intention_channel.IntentionChannel,
                            time_before_turn: int = 0) -> None:
        self._actor_to_channel[actor] = channel
        self._turn_queue.add_turn(actor, time_before_turn)

    def get_command_channel(self, actor: Character) -> intention_channel.IntentionChannel:
        return self._actor_to_channel[actor]

    def remove_actor(self, actor: Character) -> None:
        self._actor_to_channel.pop(actor)
        self._turn_queue.remove_gobj(actor)

    def get_all_actors(self) -> Set[Character]:
        return set(self._actor_to_channel.keys())

    def get_all_actors_view(self) -> KeysView[Character]:
        return self._actor_to_channel.keys()

    def current_actor(self) -> Character:
        current_turn = self._turn_queue.current_turn()
        return current_turn.gobj

    def make_turn(self, turn_time: int) -> None:
        gobj = self.current_actor()
        self._turn_queue.pop_actor()
        self._turn_queue.add_turn(gobj, turn_time)
