from settings import screen
import random


class GameData:
    def __init__(self):
        self.id_turn = -1
        self.battle_flag = False
        self.main_hero_move = True
        self.vision_area = None  # TODO: что-то с быстрым поиском.
        # Суть такова: если объект в области, то отрисовываем его
        self.camera_xy = (0, 0)
        self.actors = None  # type = GOContainer
        self.map_size = None
        self.main_char_id = -1


class IdGeneratorBase:
    __current_id = 0

    @classmethod
    def generate(cls) -> int:
        cls.__current_id += 1
        return cls.__current_id


class GameObject:
    __idGenerator = IdGeneratorBase

    def __init__(self, xy: tuple, sprite, layer=0):
        self._xy = xy
        self._sprite = sprite
        self._layer = 0
        self.__id = GameObject.__idGenerator.generate()

    def update(self, game_state: GameData) -> int:
        return 0

    @property
    def xy(self):
        return self._xy

    def set_xy(self, xy):
        self._xy = xy

    @property
    def layer(self):
        return self._layer

    @property
    def sprite(self):
        return self._sprite

    @property
    def id(self):
        return self.__id

    def __hash__(self):
        return hash(self.__id)

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        else:
            return self.__id == other.__id


class GOContainer:
    def __init__(self, indexing):
        self.__container = {}
        self.__indexing = indexing

    def add_object(self, game_obj):
        self.__container[game_obj.id] = game_obj
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

    def get_control_of_obj(self, obj_id: int):
        obj = self.__container.pop(obj_id)
        self.__indexing.remove_obj(obj_id=obj_id, xy_hint=obj.xy)
        return obj

    def return_control_of_obj(self, obj: GameObject):
        self.__container[obj.id] = obj
        self.__indexing.add_obj(obj)

    @property
    def container(self):
        return self.__container


def check_if_in_map(xy, map_size_xy):
    bool_result = (xy[0] >= 0) and (xy[0] <= map_size_xy[0]) and (xy[1] >= 0) and (xy[1] <= map_size_xy[1])
    return bool_result


class NPC(GameObject):
    """
    Самый простой тип npc: всего 3 вида поведения
    """
    def __init__(self, xy: tuple, sprite, layer=0, attitude=0):
        """
        attitude in {-1, 0, 1}: -1 -- враждебный,
                                 0 -- нейтральный,
                                 1 -- дружелюбный,
                          TODO: -2 -- берсерк, атакует ближайшего врага
        """
        super().__init__(xy, sprite, layer)
        self.__attitude = attitude
        self.__state = 0
        # self.__desired_xy = xy

    def update(self, game_state: GameData):
        if game_state.id_turn == self.id:
            if self.__attitude == 0:
                direction = random.randint(-1, 1)
                new_x = self.xy[0] + direction
                direction = random.randint(-1, 1)
                new_y = self.xy[1] + direction

                if check_if_in_map((new_x, new_y), game_state.map_size):
                    actors_in_tile = game_state.actors.get_objs_in_tile((new_x, new_y))
                    if len(actors_in_tile) == 0:
                        self.set_xy((new_x, new_y))
            elif self.__attitude == -1:
                # Идем ближайшим путем ко врагу
                mid = game_state.main_char_id
                m_chr = game_state.actors.get_obj_by_id(mid)
                m_x, m_y = m_chr.logix.xy
                x, y = self.xy
                if x > m_x:
                    x -= 1
                elif x < m_x:
                    x += 1
                if y > m_y:
                    y -= 1
                elif y < m_y:
                    y -= 1
                self.set_xy((x, y))
                # self.__desired_xy = (x, y)
        return 0
