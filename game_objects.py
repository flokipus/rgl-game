from settings import screen
import asciicels


class IVisualObject:
    def __init__(self, sprite, xy=(0, 0)):
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


class ILogicObject:
    def __init__(self, absolute_xy=(0, 0), layer_num=0):
        self._absolute_xy = absolute_xy
        self._layer_num = layer_num

    @property
    def layer_num(self):
        return self._layer_num

    def set_layer_num(self, layer_num):
        self._layer_num = layer_num

    @property
    def absolute_xy(self):
        return self._absolute_xy

    def set_xy(self, xy):
        self._absolute_xy = xy


class GameObject:
    def __init__(self, visual=None, logic=None):
        self._visual = visual
        self._logic = logic

    def update(self, function):
        function(self)

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


class Ground(GameObject):
    def __init__(self, sprite, xy, layer_num):
        super().__init__(IVisualObject(sprite, xy), ILogicObject(xy, layer_num))


class LetterObject(GameObject):
    def __init__(self, letter: chr, xy, layer_num):
        sprite = asciicels.genascii.symbol_over_transparent(letter)
        super().__init__(IVisualObject(sprite, xy), ILogicObject(xy, layer_num))
        self._letter = letter


class WallObject(LetterObject):
    def __init__(self, xy, layer_num):
        super().__init__('#', xy, layer_num)


ACTIVE_OBJECTS = set()
STATIC_OBJECTS = []

#########################################
# CREATE BASIC GRAPHIC OBJECTS: map #####
#########################################
cells_count_x = screen.SIZE[0] // screen.CELL_WIDTH
cells_count_y = screen.SIZE[1] // screen.CELL_HEIGHT
print("cells hor: {}, cells vert: {}.".format(cells_count_x, cells_count_y))
for i in range(cells_count_x):
    for j in range(cells_count_y):
        xy = (i * screen.CELL_WIDTH, j * screen.CELL_HEIGHT)
        ground_backgr = Ground(asciicels.sand_background, xy, 0)
        ground_empty = Ground(asciicels.dot_over_transparent, xy, 1)
        STATIC_OBJECTS.append(ground_backgr)
        ACTIVE_OBJECTS.add(ground_empty)


for i in range(cells_count_x//4, cells_count_x//4 + 10):
    xy = (i * screen.CELL_WIDTH, 2 * screen.CELL_HEIGHT)
    wall = WallObject(xy, 2)
    ACTIVE_OBJECTS.add(wall)
for i in range(cells_count_x//4, cells_count_x//4 + 4):
    xy = (i * screen.CELL_WIDTH, (2 + 3) * screen.CELL_HEIGHT)
    wall = WallObject(xy, 2)
    ACTIVE_OBJECTS.add(wall)
for i in range(cells_count_x//4 + 5, cells_count_x//4 + 10):
    xy = (i * screen.CELL_WIDTH, (2 + 3) * screen.CELL_HEIGHT)
    wall = WallObject(xy, 2)
    ACTIVE_OBJECTS.add(wall)
for j in range(2, 6):
    xy = (cells_count_x//4 * screen.CELL_WIDTH, j * screen.CELL_HEIGHT)
    wall = WallObject(xy, 2)
    ACTIVE_OBJECTS.add(wall)
for j in range(2, 6):
    xy = ((cells_count_x//4 + 9) * screen.CELL_WIDTH, j * screen.CELL_HEIGHT)
    wall = WallObject(xy, 2)
    ACTIVE_OBJECTS.add(wall)


super_go = LetterObject('O', (100, 300), 3)

main_hero = LetterObject('@', (0, 0), 3)

ACTIVE_OBJECTS.add(super_go)
ACTIVE_OBJECTS.add(main_hero)


def dist(xy1, xy2):
    return max(abs(xy1[0] - xy2[0]), abs(xy1[1] - xy2[1]))


def get_list_of_close_objects(abs_xy, radius):
    result = []
    for obj in ACTIVE_OBJECTS:
        if dist(obj.logic.absolute_xy, abs_xy) <= radius:
            result.append(obj)
    return result
