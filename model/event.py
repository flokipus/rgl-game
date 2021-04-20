from typing import overload


from .model import ModelGame
from gameobj.basegobj import GameObject
from utils.utils import Vec2i


class ModelEvent:
    @overload
    def apply_event(self, model) -> None: ...


class GobjMoveEvent(ModelEvent):
    def __init__(self, turn_maker: GameObject, turn_time: int, where_ij: Vec2i):
        self.turn_maker = turn_maker
        self.turn_time = turn_time
        self.where_ij = where_ij

    def apply_event(self, model: ModelGame) -> None:
        actors = model.get_actors()
        assert self.turn_maker == actors.current_gobj(), 'Only current actor can move!'
        actors.make_turn(self.turn_time)
        self.turn_maker.set_pos(self.where_ij)


class GobjWaitEvent(ModelEvent):
    def __init__(self, turn_maker: GameObject, turn_time: int):
        self.turn_maker = turn_maker
        self.turn_time = turn_time

    def apply_event(self, model: ModelGame) -> None:
        actors = model.get_actors()
        assert self.turn_maker == actors.current_gobj(), 'Only current actor can move!'
        actors.make_turn(self.turn_time)


class GobjMeleeAttackEvent(ModelEvent):
    def __init__(self, turn_maker: GameObject, turn_time: int, target_for_attack: GameObject):
        self.turn_maker = turn_maker
        self.turn_time = turn_time
        self.target_for_attack = target_for_attack

    def apply_event(self, model) -> None:
        # TODO: DO SOMETHING!!!
        actors = model.get_actors()
        assert self.turn_maker == actors.current_gobj(), 'Only current actor can move!'
        actors.make_turn(self.turn_time)
