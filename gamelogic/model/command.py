from typing import List, overload


from common.gameobj.basegobj import GameObject
from common.event import event
from common.utils.utils import Vec2i


class ModelCommand:
    @overload
    def to_model_events(self, model, gobj: GameObject) -> List[event.Event]: ...

    def to_model_events(self, model, gobj: GameObject) -> List[event.Event]:
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
            for actor_gobj in model.get_actors_gobjs():
                if gobj == actor_gobj:
                    continue
                actor_pos = actor_gobj.get_pos()
                if new_tile_ij == actor_pos:
                    wait_cost = 120
                    events_list.append(event.GobjMeleeAttackEvent(gobj, wait_cost, actor_gobj))
                    break
            else:
                # Ok, now we are actually moving!
                move_cost = target_tile.move_cost()
                events_list.append(event.GobjMoveEvent(gobj, move_cost, new_tile_ij))
        return events_list


class GobjWaitCommand(ModelCommand):
    def to_model_events(self, model, gobj: GameObject) -> List[event.Event]:
        # TODO: There is must not be magic consts!
        wait_cost = 80
        events_list = [event.GobjWaitEvent(gobj, wait_cost)]
        return events_list
