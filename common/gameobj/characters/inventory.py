from __future__ import annotations

from typing import List, Union, TypeVar, Generic
from common.gameobj.items.items import IItem


class NotEnoughInventorySpace(Exception):
    pass


class CantPutToFullCell(Exception):
    pass


T = TypeVar('T', bound=IItem)


class ItemCell(Generic[T]):
    def __init__(self, default_item=None):
        self.item: Union[T, None] = default_item

    def empty(self) -> bool:
        return self.item is None

    def put_item(self, item: T) -> None:
        if not self.empty(): raise CantPutToFullCell('Cant put item to full cell')
        self.item = item

    def remove_item(self) -> Union[T, None]:
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

    # Выдрал интерфейс. Серьезно, в Python не хватает лаконичного способа описания интерфейса класса
    def put_to_cell(self, cell_pos: int, item_to_put: IItem) -> None: ...
    def swap_cells_items(self, cell_pos1: int, cell_pos2: int) -> None: ...
    def get_item_from_cell(self, cell_pos: int) -> Union[None, IItem]: ...
    def remove_item_from_cell(self, cell_pos: int) -> Union[None, IItem]: ...
    def get_cell(self, cell_pos: int) -> ItemCell: ...
    def put_to_inventory(self, item: IItem) -> None: ...
    def is_full(self) -> bool: ...
    def empty_cells_num(self) -> int: ...
    def get_first_free_cell(self) -> Union[None, ItemCell]: ...
    def total_weight(self) -> int: ...

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
