from __future__ import annotations
from typing import Dict, Set


from common.event import Event
from common.gameobj.basegobj import GameObject


class StateOfThings:
    """C-like structure"""
    def __init__(self, actors: Dict[GameObject, CommandChannel], tile_map: TileMap):
        self._actors = actors
        self._tile_map = tile_map

    def swap(self, other: StateOfThings) -> None:
        self._actors, other._actors = other._actors, self._actors
        self._tile_map, other._tile_map = other._tile_map, self._tile_map

    def get_tiles(self) -> Set[GameObject]:
        return set(self._tile_map.get_all_tiles())

    def get_actors(self) -> KeysView[GameObject]:
        return self._actors.keys()

    def get_all_gobjects(self) -> Set[GameObject]:
        result = set()
        for actor in self._actors:
            result.add(actor)
        for tile in self._tile_map.get_all_tiles():
            result.add(tile)
        return result

    def copy(self) -> StateOfThings:
        return StateOfThings(self._actors.copy(), self._tile_map.copy())

    @property
    def actors(self) -> Dict[GameObject, CommandChannel]:
        return self._actors

    def apply_event(self, event: Event) -> None:
        if isinstance(event, GobjDoNothingEvent):
            pass
        elif isinstance(event, MoveGobjEvent):
            gobj = event.gobj
            gobj.set_pos(event.ij_after)
