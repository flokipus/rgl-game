# -*- coding: utf-8 -*-

from __future__ import annotations
import pygame
from dataclasses import dataclass
from typing import Union, List, Tuple, TypeVar, Generic

from common.utils import utils
from common.gameobj.basegobj import GameObject
from . import body_cells
from . import inventory
from ..items import items


@dataclass
class CharacterAttributes:
    strength: int
    dexterity: int
    constitution: int
    wisdom: int
    charm: int


class CantPutThisOn(Exception):
    pass


@dataclass
class CharacterItems:
    torso: body_cells.TorsoCell = body_cells.TorsoCell(items.BareArmor())
    left_hand: body_cells.LeftHandCell = body_cells.LeftHandCell(items.BareArmor())
    right_hand: body_cells.RightHandCell = body_cells.RightHandCell(items.BareFist())

    def eval_weight(self) -> int:
        total_weight = self.torso.weight() + \
                       self.left_hand.weight() + \
                       self.right_hand.weight()
        return total_weight


class Character(GameObject):
    def __init__(self, *, pos: utils.Vec2i, name: str, sprite: pygame.Surface,
                 attributes: CharacterAttributes, inventory_capacity: int,
                 base_hp: int,
                 character_items: CharacterItems,
                 race: str = 'human'):
        GameObject.__init__(self, pos=pos, name=name, sprite=sprite)
        self.base_attributes = attributes
        self.wearing_items = CharacterItems()
        self.inventory = inventory.Inventory(inventory_capacity)
        self.race = race
        self.character_items = character_items
        self.hp = base_hp

        self.__message_fail = 'Cant put on {}: {} is already with item: {}; you should put off it first'

    def pick_up_item(self, item: items.IItem) -> bool:
        """Return True if success; False else"""
        result = True
        try:
            self.inventory.put_to_inventory(item)
        except inventory.NotEnoughInventorySpace as e:
            result = False
        return result

    def put_on_torso(self, item: items.IEquipment) -> bool:
        result = True
        try:
            self.character_items.torso.put_item(item)
        except body_cells.WrongItemType as e:
            result = False
        return result

    def put_on_lefthand(self, item: items.IEquipment) -> bool:
        result = True
        try:
            self.character_items.left_hand.put_item(item)
        except body_cells.WrongItemType as e:
            result = False
        return result

    def put_on_righthand(self, item: items.IEquipment) -> bool:
        result = True
        try:
            self.character_items.right_hand.put_item(item)
        except body_cells.WrongItemType as e:
            result = False
        return result


if __name__ == '__main__':
    ch_attrs = CharacterAttributes(12, 12, 15, 16, 14)
    character = Character(pos=utils.Vec2i(0, 0),
                          name='Wizard',
                          sprite=pygame.Surface((32, 32)),
                          attributes=ch_attrs,
                          inventory_capacity=10)
    b = BareArmor()
    character.inventory.get_cell(pos=11)
    pass
