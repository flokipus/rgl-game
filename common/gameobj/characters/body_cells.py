from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, Union
from .inventory import ItemCell
from ..items import items


class WrongItemType(Exception):
    pass


T = TypeVar('T', bound=items.IItem)


class BodyCell(ItemCell[T], ABC):
    @abstractmethod
    def check_type(self, item: items.IItem) -> bool: ...

    def put_item(self, item: items.IItem) -> None:
        if not self.check_type(item):
            raise WrongItemType('Can\'t put this on: wrong item type')
        else:
            if isinstance(self.item, items.BareArmor) or isinstance(self.item, items.BareFist):
                self.item = None
            ItemCell.put_item(self, item)


class LeftHandCell(BodyCell[Union[items.ShieldArmor, items.IWeapon]]):
    def check_type(self, item: items.IItem) -> bool:
        if isinstance(item, items.IWeapon) or isinstance(item, items.ShieldArmor):
            return True
        else:
            return False


class RightHandCell(BodyCell[Union[items.ShieldArmor, items.IWeapon]]):
    def check_type(self, item: items.IItem) -> bool:
        if isinstance(item, items.IWeapon) or isinstance(item, items.ShieldArmor):
            return True
        else:
            return False


class TorsoCell(BodyCell[items.TorsoArmor]):
    def check_type(self, item: items.IItem) -> bool:
        if isinstance(item, items.TorsoArmor):
            return True
        else:
            return False

