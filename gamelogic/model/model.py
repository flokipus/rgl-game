# -*- coding: utf-8 -*-

from typing import Dict, Set

from .actors import actors
from .actor_intention import ActorIntention
from .intention_channel import IntentionChannel
from common.gameobj.basegobj import GameObject
from common.gameobj.characters.base_character import Character
from common.gameobj.items import items as itemsm
from common.gameobj.map.tilemaps import TileMap, Tile
from common.observer import interface
from common.utils.utils import Vec2i


class ModelGame(interface.Subject):
    def __init__(self,
                 init_actors: Dict[Character, IntentionChannel],
                 tile_map: TileMap,
                 items: Set[itemsm.IItem],
                 player_character: Character):
        super().__init__()
        self._subj = interface.Subject()
        if player_character not in init_actors:
            raise RuntimeError('Player character should be actor')
        self._actors: actors.Actors = actors.Actors(initial_actors=init_actors)
        self._player_character = player_character
        self._tile_map = tile_map
        self._items = items

    @property
    def player_character(self) -> Character:
        return self._player_character

    def get_actors(self) -> actors.Actors:
        return self._actors

    def get_all_gobjs(self) -> Set[GameObject]:
        # TODO: make clean view; cast to set is too costly
        total_gobjs = set(self._actors.get_all_actors()).union(self._tile_map.get_all_tiles()).union(self._items)
        return total_gobjs

    def get_actors_gobjs(self) -> Set[Character]:
        return self._actors.get_all_actors()

    def get_items_gobjs(self) -> Set[itemsm.IItem]:
        return self._items

    def get_tile(self, ij: Vec2i) -> Tile:
        return self._tile_map.get_tile(ij)

    def get_tile_map(self) -> TileMap:
        return self._tile_map

    def one_cycle_turns(self) -> None:
        """We process first actor in the queue of turns and then continue processing
        in cycle until first player actor is met"""
        does_controlled_by_player = False
        while not does_controlled_by_player:
            this_turn_gobj: Character = self._actors.current_actor()
            this_turn_comm_channel = self._actors.get_command_channel(this_turn_gobj)
            this_turn_command = this_turn_comm_channel.request_command()
            if this_turn_command is None and this_turn_gobj == self._player_character:
                break
            action = this_turn_command.interpret(model=self, character=this_turn_gobj)
            new_events = action.apply(model=self)
            for event in new_events:
                self.notify(event)
            next_turn_gobj = self._actors.current_actor()
            does_controlled_by_player = (next_turn_gobj == self._player_character)

    def put_user_command(self, command: ActorIntention) -> None:
        self._actors.get_command_channel(self._player_character).put_command(command)
