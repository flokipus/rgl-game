# -*- coding: utf-8 -*-

from typing import Dict, Set

from .actors import actors
from .command import ModelCommand
from .command_channel import ModelCommandChannel
from .eventcallback import apply_event
from common.gameobj.basegobj import GameObject
from common.gameobj.map.tilemaps import TileMap, Tile
from common.observer import interface
from common.utils.utils import Vec2i


class ModelGame(interface.Subject):
    def __init__(self,
                 init_actors: Dict[GameObject, ModelCommandChannel],
                 tile_map: TileMap,
                 items: Set[GameObject],
                 player_character: GameObject):
        super().__init__()
        if player_character not in init_actors:
            raise RuntimeError('Player character should be actor')
        self._actors: actors.Actors = actors.Actors(initial_actors=init_actors)
        self._player_character = player_character
        self._tile_map = tile_map
        self._items = items

    @property
    def player_character(self) -> GameObject:
        return self._player_character

    def get_actors(self) -> actors.Actors:
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

    def one_cycle_turns(self) -> None:
        """We process first actor in the queue of turns and then continue processing
        in cycle until first player actor is met"""
        does_controlled_by_player = False
        while not does_controlled_by_player:
            this_turn_gobj: GameObject = self._actors.current_gobj()
            this_turn_comm_channel = self._actors.get_command_channel(this_turn_gobj)
            this_turn_command = this_turn_comm_channel.request_command()
            if this_turn_command is None and this_turn_gobj == self._player_character:
                break
            new_events = this_turn_command.to_model_events(model=self, gobj=this_turn_gobj)
            for event in new_events:
                apply_event(event_occured=event, game_model=self)  # self._actors can be updated here
                self.notify(event)
            next_turn_gobj = self._actors.current_gobj()
            does_controlled_by_player = (next_turn_gobj == self._player_character)

    def put_user_command(self, command: ModelCommand) -> None:
        self._actors.get_command_channel(self._player_character).put_command(command)
