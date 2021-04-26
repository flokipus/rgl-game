from typing import overload

from common.gameobj.basegobj import GameObject
from common.utils.utils import Vec2i


class Event:
    @overload
    def who_am_i(self) -> str: ...

    def who_am_i(self) -> str:
        return 'Empty event'


class GobjMoveEvent(Event):
    def __init__(self, turn_maker: GameObject, turn_time: int, to_ij: Vec2i):
        self.turn_maker = turn_maker
        self.turn_time = turn_time
        self.to_ij = to_ij
        self.from_ij = turn_maker.get_pos()

    def who_am_i(self) -> str:
        return 'MoveEvent(gobj.id={}; gobj.name={}; ij_from={}; ij_to={})'.format(
            self.turn_maker.id,
            self.turn_maker.name,
            self.from_ij,
            self.to_ij
        )


class GobjWaitEvent(Event):
    def __init__(self, turn_maker: GameObject, turn_time: int):
        self.turn_maker = turn_maker
        self.turn_time = turn_time

    def who_am_i(self) -> str:
        return 'WaitEvent(gobj.id={}; gobj.name={}; ij_from={})'.format(
            self.turn_maker.id,
            self.turn_maker.name,
            self.turn_maker.get_pos()
        )


class GobjMeleeAttackEvent(Event):
    def __init__(self, turn_maker: GameObject, turn_time: int, target_for_attack: GameObject):
        self.turn_maker = turn_maker
        self.attack_from_ij = turn_maker.get_pos()
        self.turn_time = turn_time
        self.target_for_attack = target_for_attack
        self.attack_to_ij = target_for_attack.get_pos()

    def who_am_i(self) -> str:
        return 'AttackEvent(attacker.id={}; attacker.name={}; attacker.pos={}; ' \
               'def.id={}; def.name={}; def.pos={})'.format(
            self.turn_maker.id,
            self.turn_maker.name,
            self.turn_maker.get_pos(),
            self.target_for_attack.id,
            self.target_for_attack.name,
            self.target_for_attack.get_pos()
        )
