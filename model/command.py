from typing import List, overload


from gameobj.basegobj import GameObject
from .event import ModelEvent, GobjWaitEvent, GobjMoveEvent, GobjMeleeAttackEvent
from .model import ModelGame
from utils.utils import Vec2i


class ModelCommand:
    @overload
    def to_model_events(self, model: ModelGame, gobj: GameObject) -> List[ModelEvent]: ...


class MoveGobjCommand:
    def __init__(self, delta_ij: Vec2i):
        self._delta_ij = delta_ij

    def to_model_events(self, model: ModelGame, gobj: GameObject) -> List[ModelEvent]:
        events_list = []
        current_tile_ij = gobj.get_pos()
        new_tile_ij = current_tile_ij + self._delta_ij
        target_tile = model.get_tile(new_tile_ij)
        if target_tile is None:
            # TODO: There is must not be magic consts!
            wait_cost = 80
            events_list.append(GobjWaitEvent(gobj, wait_cost))
        else:
            # TODO: we need some fast sparse structures
            for actor_gobj in model.get_actors_gobjs():
                if gobj == actor_gobj:
                    continue
                actor_pos = actor_gobj.get_pos()
                if new_tile_ij == actor_pos:
                    wait_cost = 120
                    events_list.append(GobjMeleeAttackEvent(gobj, wait_cost, actor_gobj))
                    break
            else:
                # Ok, now we actually moving!
                move_cost = target_tile.move_cost()
                events_list.append(GobjMoveEvent(gobj, move_cost, new_tile_ij))
        return events_list


