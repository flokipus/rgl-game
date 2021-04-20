from typing import Dict, List, Set, Tuple


from .command import ModelCommand
from .command_channel import ModelCommandChannel
from .event import ModelEvent
from .turnqueue.turnqueue import TurnOrderInTime, GobjWithTime
from gameobj.basegobj import GameObject
from map.tilemaps import TileMap, Tile
from utils.utils import Vec2i


class Actors:
    """
    actor <-> (gobj, command_channel)
    actors <-> dict: gobj -> command_channel + turn_queue
    """
    def __init__(self, initial_actors: Dict[GameObject, ModelCommandChannel]):
        self._gobj_to_channel = initial_actors
        self._turn_queue = TurnOrderInTime()
        for gobj in self._gobj_to_channel:
            self._turn_queue.add_turn(gobj, 0)

    def add_actor(self, gobj: GameObject, channel: ModelCommandChannel) -> None:
        self._gobj_to_channel[gobj] = channel
        max_wait_time = self._turn_queue.last_gobj().time
        self._turn_queue.add_turn(gobj, max_wait_time)

    def add_actor_with_time(self, gobj: GameObject, channel: ModelCommandChannel, time_before_turn: int = 0) -> None:
        self._gobj_to_channel[gobj] = channel
        self._turn_queue.add_turn(gobj, time_before_turn)

    def get_command_channel(self, gobj: GameObject) -> ModelCommandChannel:
        return self._gobj_to_channel[gobj]

    def remove_actor(self, gobj: GameObject) -> None:
        self._gobj_to_channel.pop(gobj)

    def get_all_gobjs(self) -> Set[GameObject]:
        return set(self._gobj_to_channel.keys())

    def current_gobj(self) -> GobjWithTime:
        return self._turn_queue.current_gobj()

    def make_turn(self, turn_time: int) -> None:
        gobj = self._turn_queue.current_gobj().gobj
        self._turn_queue.pop_actor()
        self._turn_queue.add_turn(gobj, turn_time)


class ModelGame:
    def __init__(self,
                 actors: Dict[GameObject, ModelCommandChannel],
                 tile_map: TileMap,
                 items: Set[GameObject],
                 player_character: GameObject):
        if player_character not in actors:
            raise RuntimeError('Player character should be actor')
        self._actors: Actors = Actors(initial_actors=actors)
        self._player_character = player_character

        self._tile_map = tile_map
        self._items = items
        self._events_occurred = list()

    def get_actors(self) -> Actors:
        return self._actors

    def get_all_gobjs(self) -> Set[GameObject]:
        total_gobjs = set(self._actors.get_all_gobjs()).union(self._tile_map.get_all_tiles()).union(self._items)
        return total_gobjs

    def get_actors_gobjs(self) -> Set[GameObject]:
        return self._actors.get_all_gobjs()

    def get_items_gobjs(self) -> Set[GameObject]:
        return self._items

    def get_tile(self, ij: Vec2i) -> Tile:
        return self._tile_map.get_tile(ij)

    def get_tile_map(self) -> TileMap:
        return self._tile_map

    def what_is_in_tile(self, tile_ij: Vec2i) -> List[GameObject]:



    def one_turn_tick(self) -> None:
        """We process first actor in the queue of turns and then continue processing
        in cycle until first player actor is met"""
        does_controlled_by_player = False
        while not does_controlled_by_player:
            gobj_to_move: GameObject = self._actors.current_gobj().gobj
            command = self._actors.get_command_channel(gobj_to_move).request_command()
            if command is None and gobj_to_move == self._player_character:
                break
            new_events = command.to_model_events(model=self, gobj=gobj_to_move)
            for event in new_events:
                event.apply_event(model=self)
            self._events_occurred += new_events
            top_actor = self._turn_queue.top_actor()
            does_controlled_by_player = isinstance(self.get_actors()[top_actor], UserCommandChannel)

    def get_events(self) -> List[ModelEvent]:
        return self._events_occurred

    def put_user_command(self, command: ModelCommand) -> None:
        self._actors.get_command_channel(self._player_character).put_command(command)

    def unload_events(self) -> List[ModelEvent]:
        unloaded = self._events_occurred.copy()
        self._events_occurred.clear()
        return unloaded

    def _top_actor_wait(self, time):
        actor = self._turn_queue.top_actor()
        self._turn_queue.pop_actor()
        # TODO: There is must not be magic consts!
        self._turn_queue.add_turn(actor, time)
