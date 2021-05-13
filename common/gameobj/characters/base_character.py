import pygame
from copy import copy
from dataclasses import dataclass

from common.utils import utils
from common.gameobj.basegobj import GameObject


@dataclass
class CharacterAttributes:
    strength: int
    dexterity: int
    constitution: int
    wisdom: int
    charm: int


@dataclass
class Item:
    weight: int
    name: str


@dataclass
class Weapon(Item):
    damage: int


@dataclass
class BodyPartsItems:
    head: None
    body: None
    left_hand: None
    right_hand: None
    legs: None


class BaseCharacter(GameObject):
    def __init__(self, *, pos: utils.Vec2i, name: str, sprite: pygame.Surface, attributes: CharacterAttributes):
        GameObject.__init__(self, pos=pos, name=name, sprite=sprite)
        self._base_attributes = attributes
        self._actual_attributes = copy(attributes)


if __name__ == '__main__':
    w = Weapon(1, 2)
    print(w)

    viking_attributes = CharacterAttributes(16, 14, 14, 10, 12)
    vikings = BaseCharacter(pos=utils.Vec2i(0, 0), name='viking', sprite=None, attributes=viking_attributes)
    print(vikings._actual_attributes)
    print(vikings._base_attributes)
    print(vikings._actual_attributes is vikings._base_attributes)
    vikings._actual_attributes.charm = 15
    print(vikings._actual_attributes)
    print(vikings._base_attributes)
    print(vikings._actual_attributes is vikings._base_attributes)
