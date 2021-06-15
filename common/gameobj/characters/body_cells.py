from __future__ import annotations

from abc import ABC, abstractmethod
from .inventory import ItemCell
from ..items import items


class WrongItemType(Exception):
    pass


class BodyCell(ItemCell, ABC):
    @abstractmethod
    def check_type(self, item: items.IItem) -> bool: ...

    def put_item(self, item: items.IItem) -> None:
        if not self.check_type(item):
            raise WrongItemType('Can\'t put this on: wrong item type')
        else:
            ItemCell.put_item(self, item)


class LeftHandCell(BodyCell):
    def check_type(self, item: items.IItem) -> bool:
        if isinstance(item, items.IWeapon) or isinstance(item, items.ShieldArmor):
            return True
        else:
            return False


class RightHandCell(BodyCell):
    def check_type(self, item: items.IItem) -> bool:
        if isinstance(item, items.IWeapon) or isinstance(item, items.ShieldArmor):
            return True
        else:
            return False


class TorsoCell(BodyCell):
    def check_type(self, item: items.IItem) -> bool:
        if isinstance(item, items.TorsoArmor):
            return True
        else:
            return False

