from settings import screen
import asciicels
import sparse_index


class IdGeneratorBase:
    __current_id = 0

    @classmethod
    def generate(cls) -> int:
        cls.__current_id += 1
        return cls.__current_id


class VisualObjectBase:
    def __init__(self, sprite, xy=(0, 0), layer_num=0):
        self._layer_num = layer_num
        self._sprite = sprite
        self._xy = xy

    @property
    def sprite(self):
        return self._sprite

    def set_sprite(self, sprite):
        self._sprite = sprite

    @property
    def xy(self):
        return self._xy

    def set_xy(self, xy):
        self._xy = xy

    @property
    def layer_num(self):
        return self._layer_num

    def set_layer_num(self, layer_num):
        self._layer_num = layer_num


class LogicObjectBase:
    def __init__(self, absolute_xy=(0, 0)):
        self._absolute_xy = absolute_xy

    @property
    def xy(self):
        return self._absolute_xy

    def set_xy(self, xy):
        self._absolute_xy = xy


class GameObjectBase:
    __idGenerator = IdGeneratorBase

    def __init__(self, visual=None, logic=LogicObjectBase()):
        self._visual = visual
        self._logic = logic
        self.__id = GameObjectBase.__idGenerator.generate()

    @property
    def obj_id(self):
        return self.__id

    @property
    def visual(self):
        return self._visual

    @property
    def logic(self):
        return self._logic

    def set_logic(self, logic):
        self._logic = logic

    def set_visual(self, visual):
        self._visual = visual

    def __hash__(self):
        return hash(self.__id)

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        else:
            return self.__id == other.__id


class Ground(GameObjectBase):
    def __init__(self, sprite, xy, layer_num):
        super().__init__(VisualObjectBase(sprite, xy, layer_num), LogicObjectBase(xy))


class LetterObject(GameObjectBase):
    def __init__(self, letter: chr, xy, layer_num):
        sprite = asciicels.genascii.symbol_over_transparent(letter)
        super().__init__(VisualObjectBase(sprite, xy, layer_num), LogicObjectBase(xy))
        self._letter = letter


class WallObject(LetterObject):
    def __init__(self, xy, layer_num):
        super().__init__('#', xy, layer_num)


class Camera(GameObjectBase):
    def __init__(self, xy):
        logic = LogicObjectBase(xy)
        super().__init__(logic=logic, visual=None)


class GameObjectContainer:
    def __init__(self, indexing):
        self.__container = {}
        self.__indexing = indexing

    def add_object(self, game_obj):
        self.__container[game_obj.obj_id] = game_obj
        self.__indexing.add_obj(game_obj)

    def remove_object(self, game_obj):
        if game_obj.obj_id in self.__container:
            self.__container.pop(game_obj.obj_id)
            self.__indexing.remove_obj(game_obj.obj_id, game_obj.logic.xy)

    def get_obj_by_id(self, obj_id):
        return self.__container[obj_id]

    def get_objs_in_tile(self, xy_in_tile) -> list:
        obj_ids = self.__indexing.get_objs_in_xy(xy_in_tile)
        return [self.__container[obj_id] for obj_id in obj_ids]

    @property
    def id_to_objs(self):
        return self.__container


ACTIVE_OBJECTS = GameObjectContainer(sparse_index.SparseIndexing())  # Предполагают какое-то взаимодействие
STATIC_OBJECTS = GameObjectContainer(sparse_index.SparseIndexing())  # По большому счету это только спрайт
CAMERA = Camera(xy=(0, 0))


#########################################
# CREATE BASIC GRAPHIC OBJECTS: map #####
#########################################
cells_count_x = screen.SIZE[0] // screen.CELL_WIDTH
cells_count_y = screen.SIZE[1] // screen.CELL_HEIGHT
print("cells hor: {}, cells vert: {}.".format(cells_count_x, cells_count_y))
for i in range(cells_count_x):
    for j in range(cells_count_y):
        obj_xy = (i * screen.CELL_WIDTH, j * screen.CELL_HEIGHT)
        ground_backgr = Ground(asciicels.sand_background, obj_xy, 0)
        ground_empty = Ground(asciicels.dot_over_transparent, obj_xy, 1)
        STATIC_OBJECTS.add_object(ground_backgr)
        ACTIVE_OBJECTS.add_object(ground_empty)

for i in range(cells_count_x//4, cells_count_x//4 + 10):
    obj_xy = (i * screen.CELL_WIDTH, 2 * screen.CELL_HEIGHT)
    wall = WallObject(obj_xy, 2)
    ACTIVE_OBJECTS.add_object(wall)
for i in range(cells_count_x//4, cells_count_x//4 + 4):
    obj_xy = (i * screen.CELL_WIDTH, (2 + 3) * screen.CELL_HEIGHT)
    wall = WallObject(obj_xy, 2)
    ACTIVE_OBJECTS.add_object(wall)
for i in range(cells_count_x//4 + 5, cells_count_x//4 + 10):
    obj_xy = (i * screen.CELL_WIDTH, (2 + 3) * screen.CELL_HEIGHT)
    wall = WallObject(obj_xy, 2)
    ACTIVE_OBJECTS.add_object(wall)
for j in range(2, 6):
    obj_xy = (cells_count_x//4 * screen.CELL_WIDTH, j * screen.CELL_HEIGHT)
    wall = WallObject(obj_xy, 2)
    ACTIVE_OBJECTS.add_object(wall)
for j in range(2, 6):
    obj_xy = ((cells_count_x//4 + 9) * screen.CELL_WIDTH, j * screen.CELL_HEIGHT)
    wall = WallObject(obj_xy, 2)
    ACTIVE_OBJECTS.add_object(wall)


super_go = LetterObject('O', (100, 300), 3)

main_hero = LetterObject('@', (0, 0), 3)

ACTIVE_OBJECTS.add_object(super_go)
ACTIVE_OBJECTS.add_object(main_hero)


# def dist(xy1, xy2):
#     return max(abs(xy1[0] - xy2[0]), abs(xy1[1] - xy2[1]))
#
#
# def get_list_of_close_objects(abs_xy, radius):
#     result = []
#     for obj in ACTIVE_OBJECTS:
#         if dist(obj.logic.xy, abs_xy) <= radius:
#             result.append(obj)
#     return result
# def dist(xy1, xy2):
#     return max(abs(xy1[0] - xy2[0]), abs(xy1[1] - xy2[1]))
#
#
# def get_list_of_close_objects(abs_xy, radius):
#     result = []
#     for obj in ACTIVE_OBJECTS:
#         if dist(obj.logic.xy, abs_xy) <= radius:
#             result.append(obj)
#     return result
