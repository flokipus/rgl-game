# -*- coding: utf-8 -*-

from __future__ import annotations
import pygame
from abc import ABC, abstractmethod
from copy import copy
from dataclasses import dataclass
from typing import Union, List, Tuple, TypeVar, Generic

from common.utils import utils
from common.gameobj.basegobj import GameObject


@dataclass
class CharacterAttributes:
    strength: int
    dexterity: int
    constitution: int
    wisdom: int
    charm: int


class IItem(ABC):
    @abstractmethod
    def weight(self) -> int:
        pass

    @abstractmethod
    def name(self) -> str:
        pass

    def __hash__(self) -> int:
        return hash(self.name())

    def __eq__(self, other: IItem):
        return self.name() == other.name()

    def __str__(self):
        return self.name()


@dataclass
class RequirementCheckAnswer:
    result: bool
    message_reason: str


class IEquipment(IItem, ABC):
    """You can put this on your character"""
    @abstractmethod
    def check_requirements_to_wield(self, character_attrs: CharacterAttributes) -> RequirementCheckAnswer:
        """But sometimes you can't"""
        pass


@dataclass
class IWeapon(IEquipment):
    @abstractmethod
    def eval_damage(self, character_attrs: CharacterAttributes) -> int:
        """Positive value"""

    @abstractmethod
    def bonus_chance_to_hit(self, character_attrs: CharacterAttributes) -> int:
        """Additional chance to hit target. From 0 to 100.
        Characters attributes are taken into account"""


class IOneHandedWeapon(IWeapon, ABC):
    pass

class ITwoHandedWeapon(IWeapon, ABC):
    pass


class BareHand(IOneHandedWeapon):
    def weight(self) -> int:
        return 0

    def name(self) -> str:
        return 'Bare hand'

    def check_requirements_to_wield(self, character_attrs: CharacterAttributes) -> RequirementCheckAnswer:
        return RequirementCheckAnswer(result=True, message_reason='')

    def eval_damage(self, character_attrs: CharacterAttributes) -> int:
        damage: int = character_attrs.strength // 2
        return damage

    def bonus_chance_to_hit(self, character_attrs: CharacterAttributes) -> int:
        chance: int = character_attrs.dexterity // 2
        return chance


class OneHandAxe(IOneHandedWeapon):
    def weight(self) -> int:
        return 2000

    def name(self) -> str:
        return 'Ordinary one hand axe'

    def check_requirements_to_wield(self, character_attrs: CharacterAttributes) -> RequirementCheckAnswer:
        result = character_attrs.strength >= 8
        if result:
            message_reason = ''
        else:
            message_reason = 'Not enough strength'
        return RequirementCheckAnswer(result, message_reason)

    def eval_damage(self, character_attrs: CharacterAttributes) -> int:
        damage: int = 8 + character_attrs.strength // 2
        return damage

    def bonus_chance_to_hit(self, character_attrs: CharacterAttributes) -> int:
        return character_attrs.strength // 2 + character_attrs.dexterity // 4


@dataclass
class IArmor(IEquipment):
    @abstractmethod
    def eval_chance_to_avoid_hit(self, character_attrs: CharacterAttributes) -> int:
        """From 0 to 100. Characters attributes are taken into account"""

    @abstractmethod
    def damage_reduction(self, character_attrs: CharacterAttributes) -> int:
        pass

class BareArmor(IArmor):
    def __init__(self):
        IArmor.__init__(self)

    def weight(self) -> int:
        return 0

    def name(self) -> str:
        return 'Bare body'

    def check_requirements_to_wield(self, character_attrs: CharacterAttributes) -> RequirementCheckAnswer:
        return RequirementCheckAnswer(result=True, message_reason='')

    def eval_chance_to_avoid_hit(self, character_attrs: CharacterAttributes) -> int:
        chance: int = character_attrs.dexterity // 2
        return chance

    def damage_reduction(self, character_attrs: CharacterAttributes) -> int:
        return 0


class HeadArmor(BareArmor):
    pass


class BodyArmor(BareArmor):
    pass


class ShieldArmor(BareArmor):
    pass


class LegsArmor(BareArmor):
    pass


class CantPutToFullCell(Exception):
    pass


class ItemCell:
    def __init__(self):
        self.item: Union[IItem, None] = None

    def empty(self) -> bool:
        return self.item is None

    def put_item(self, item: IItem) -> None:
        if not self.empty(): raise CantPutToFullCell('Cant put item to full cell')
        self.item = item

    def remove_item(self) -> Union[IItem, None]:
        if self.empty():
            return None
        item = self.item
        self.item = None
        return item

    def weight(self) -> int:
        if self.empty():
            return 0
        else:
            return self.item.weight()

    def swap_with_other(self, other: ItemCell) -> None:
        self.item, other.item = other.item, self.item


class NotEnoughInventorySpace(BaseException):
    pass


class Inventory:
    """Inventory contain certain amount of cells. Every cell can be empty"""
    def __init__(self, maximum_items: int):
        if maximum_items <= 0:
            raise ValueError('Inventory must have positive capacity')
        self.maximum_items = maximum_items
        self.cells_grid: List[ItemCell] = [ItemCell() for _ in range(maximum_items)]

        self.__was_touched: bool = False
        self.__first_empty_cell = self.cells_grid[0]
        self.__weight = 0
        self.__count_free_cells = self.maximum_items

    def put_to_cell(self, cell_pos: int, item_to_put: IItem) -> None:
        """Trying to put item to cell"""
        self.__check_inv_range(cell_pos)
        try:
            self.cells_grid[cell_pos].put_item(item_to_put)
        except CantPutToFullCell:
            pass
        else:
            self.__was_touched = True

    def swap_cells_items(self, cell_pos1: int, cell_pos2: int) -> None:
        self.__check_inv_range(cell_pos1)
        self.__check_inv_range(cell_pos2)
        # This is more cheap to swap cells references instead of cell\'s content. But
        # the current approach prevents from the mistakes
        self.cells_grid[cell_pos1].swap_with_other(self.cells_grid[cell_pos2])

    def get_item_from_cell(self, cell_pos: int) -> Union[None, IItem]:
        self.__check_inv_range(cell_pos)
        return self.cells_grid[cell_pos].item

    def remove_item_from_cell(self, cell_pos: int) -> Union[None, IItem]:
        self.__check_inv_range(cell_pos)
        self.__was_touched = True
        return self.cells_grid[cell_pos].remove_item()


    def get_cell(self, cell_pos: int) -> ItemCell:
        self.__check_inv_range(cell_pos)
        return_cell = self.cells_grid[cell_pos]
        self.__was_touched = True
        return return_cell

    def put_to_inventory(self, item: IItem) -> None:
        free_cell = self.get_first_free_cell()
        if free_cell is not None:
            free_cell.put_item(item)
            self.__was_touched = True
        else:
            raise NotEnoughInventorySpace('Not enough inventory space')

    def is_full(self) -> bool:
        if self.__was_touched:
            self.__count_free_cells = self.empty_cells_num()
        return self.__count_free_cells == 0

    def empty_cells_num(self) -> int:
        count_free_cells = 0
        for cell in self.cells_grid:
            if cell.empty():
                count_free_cells += 1
        return count_free_cells

    def get_first_free_cell(self) -> Union[None, ItemCell]:
        if self.__was_touched:
            for cell in self.cells_grid:
                if cell.empty():
                    self.__first_empty_cell = cell
                    break
            else:
                self.__first_empty_cell = None
        return self.__first_empty_cell

    def total_weight(self) -> int:
        if self.__was_touched:
            self.__weight = 0
            for cell in self.cells_grid:
                self.__weight += cell.weight()
        return self.__weight

    def __check_inv_range(self, cell_pos: int) -> None:
        if cell_pos >= self.maximum_items:
            raise AttributeError(f'Out of inventory range: cell_pos={cell_pos}; maximum_items={self.maximum_items}')


class CantPutThisOn(Exception):
    pass


class HeadCell(ItemCell):
    def put_item(self, item: IItem) -> None:
        if isinstance(item, HeadArmor):
            ItemCell.put_item(self, item)
        else:
            raise CantPutThisOn('Bla-bla')

    def swap_with_other(self, other: ItemCell) -> None:
        if isinstance(other.item, HeadArmor):
            ItemCell.swap_with_other(self, other)
        else:
            raise CantPutThisOn('Bla-bla')


class LeftHandCell(ItemCell):
    def put_item(self, item: IItem) -> None:
        if (isinstance(self.item, IOneHandedWeapon) or isinstance(self.item, ShieldArmor)) and \
                (isinstance(item, IOneHandedWeapon) or isinstance(item, ShieldArmor)):
            ItemCell.put_item(self, item)
        else:
            raise CantPutThisOn('You should write correct exception text')

    def swap_with_other(self, other: ItemCell) -> None:
        if (isinstance(self.item, IOneHandedWeapon) or isinstance(self.item, ShieldArmor)) and \
                (isinstance(other.item, IOneHandedWeapon) or isinstance(other.item, ShieldArmor)):
            ItemCell.swap_with_other(self, other)
        else:
            raise CantPutThisOn('You should write correct exception text')


class RightHandCell(ItemCell):
    def put_item(self, item: IItem) -> None:
        pass


@dataclass
class CharacterItems:
    # head_cell
    # head: BareHeadArmor = BareHeadArmor()
    # body: BareBodyArmor = BareBodyArmor()
    # left_hand: Union[BareShieldArmor, IOneHandedWeapon, ITwoHandedWeapon] = BareHand
    # right_hand: Union[IOneHandedWeapon, ITwoHandedWeapon] = BareHand
    # legs: BareLegsArmor = BareLegsArmor()

    def eval_weight(self) -> int:
        total_weight = self.legs.weight() + \
                       self.body.weight() + \
                       self.head.weight() + \
                       self.left_hand.weight() + \
                       self.right_hand.weight()
        return total_weight


class Character(GameObject):
    def __init__(self, *, pos: utils.Vec2i, name: str, sprite: pygame.Surface,
                 attributes: CharacterAttributes, inventory_capacity: int):
        GameObject.__init__(self, pos=pos, name=name, sprite=sprite)
        self.base_attributes = attributes
        self.wearing_items = CharacterItems()
        self.inventory = Inventory(inventory_capacity)

        self.__message_fail = 'Cant put on {}: {} is already with item: {}; you should put off it first'

    def pick_up_item(self, item: IItem) -> bool:
        """Return True if success; False else"""
        result = True
        try:
            self.inventory.put_to_cell(item)
        except NotEnoughInventorySpace as e:
            result = False
        return result

    def put_on_body(self, item: IEquipment) -> None:
        pass

    def put_on_item(self, item: IEquipment, body_part: ) -> None:
        body_part =

    def put_on_item(self, item: IEquipment) -> None:
        if isinstance(item, BareArmor):
            if isinstance(item, BareHeadArmor):
                if type(self.wearing_items.head) == BareHeadArmor:
                    self.wearing_items.head = item
                else:
                    raise CantPutOnThis(self.__message_fail.format(item, 'head', self.wearing_items.head))
            if isinstance(item, BareShieldArmor):
                if type(self.wearing_items.left_hand) == BareShieldArmor:
                    self.wearing_items.left_hand = item
                else:
                    raise CantPutOnThis(self.__message_fail.format(item, 'left hand', self.wearing_items.left_hand))
            if isinstance(item, BareBodyArmor):
                if type(item) == BareBodyArmor:
                    self.wearing_items.body = item
                else:
                    raise CantPutOnThis(self.__message_fail.format(item, 'body', self.wearing_items.body))
            if isinstance(item, BareLegsArmor):
                if type(item) == BareLegsArmor:
                    self.wearing_items.legs = item
                else:
                    raise CantPutOnThis(self.__message_fail.format(item, 'legs', self.wearing_items.legs))
            else:
                raise TypeError('put_on item: Not familiar with this armor type: {}'.format(type(item)))
        elif isinstance(item, HandWeapon):
            if isinstance(item, OneHandAxe)
        else:
            raise CantPutOnThis('Wrong item type.')


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
