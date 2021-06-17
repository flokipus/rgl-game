from typing import overload
from dataclasses import dataclass

from common.gameobj.characters.base_character import Character
from common.utils.utils import Vec2i


class Event:
    @overload
    def who_am_i(self) -> str: ...

    def who_am_i(self) -> str:
        return 'Empty event'


@dataclass
class CharacterDied(Event):
    who: Character


@dataclass
class CharacterMadeMeleeAttack(Event):
    who: Character
    whom: Character
    target_tile_ij: Vec2i
    from_tile_ij: Vec2i
    damage: int
    does_hit_target: bool
    is_critical: bool


@dataclass
class CharacterMadeMove(Event):
    who: Character
    old_tile_ij: Vec2i
    new_tile_ij: Vec2i


@dataclass
class CharacterWaitTurn(Event):
    who: Character


@dataclass
class PlayerUnableToMadeWalk(Event):
    """Этот эвент нужен для ситуации, когда игрок очевидно не может сделать ход: скажем, уперся в стену.
    В этом случае, хода не происходит и мы оповещаем View об этом
    """
    from_tile_ij: Vec2i
    target_tile_ij: Vec2i
