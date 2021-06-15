# -*- coding: utf-8 -*-

from typing import List
from abc import ABC, abstractmethod

from common.gameobj.basegobj import GameObject
from common.event import event
from common.utils.utils import Vec2i


class Action(ABC):
    @abstractmethod
    def apply(self, model) -> List[event.Event]: ...


class ModelCommand:
    def to_model_events(self, model, gobj: GameObject) -> List[event.Event]:
        pass

    def interpret(self, model, gobj: GameObject) -> Action:
        pass


class MoveGobjCommand(ModelCommand):
    def __init__(self, delta_ij: Vec2i):
        self._delta_ij = delta_ij

    def to_model_events(self, model, gobj: GameObject) -> List[event.Event]:
        events_list = []
        current_tile_ij = gobj.get_pos()
        new_tile_ij = current_tile_ij + self._delta_ij
        target_tile = model.get_tile(new_tile_ij)
        if target_tile is None:
            # TODO: There is must not be magic consts!
            wait_cost = 80
            events_list.append(event.GobjWaitEvent(gobj, wait_cost))
        else:
            # TODO: we need some fast sparse structures
            actors = model.get_actors().get_all_actors_view()
            for actor_gobj in actors:
                if gobj == actor_gobj:
                    continue
                actor_pos = actor_gobj.get_pos()
                if new_tile_ij == actor_pos:
                    wait_cost = 120
                    if gobj == model.player_character:
                        events_list.append(event.PlayerMeleeAttackEvent(gobj, wait_cost, actor_gobj))
                    else:
                        events_list.append(event.GobjMeleeAttackEvent(gobj, wait_cost, actor_gobj))
                    break
            else:
                # Ok, now we are actually moving!
                move_cost = target_tile.move_cost()
                if gobj == model.player_character:
                    events_list.append(event.PlayerMoveEvent(gobj, move_cost, new_tile_ij))
                else:
                    events_list.append(event.GobjMoveEvent(gobj, move_cost, new_tile_ij))
        return events_list


class GobjWaitCommand(ModelCommand):
    def to_model_events(self, model, gobj: GameObject) -> List[event.Event]:
        # TODO: There is must not be magic consts!
        wait_cost = 80
        events_list = [event.GobjWaitEvent(gobj, wait_cost)]
        return events_list
