from settings import screen
import random


class GameState:
    def __init__(self):
        self.id_turn = -1
        self.battle_flag = False
        self.main_hero_move = True
        self.vision_area = None  # TODO: что-то с быстрым поиском.
        # Суть такова: если объект в области, то отрисовываем его
        self.camera_xy = (0, 0)
        self.actors = None
        self.main_char_id = -1


class IdGeneratorBase:
    __current_id = 0

    @classmethod
    def generate(cls) -> int:
        cls.__current_id += 1
        return cls.__current_id


class Visual:
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


class Logic:
    def __init__(self, absolute_xy=(0, 0)):
        self._absolute_xy = absolute_xy

    @property
    def xy(self):
        return self._absolute_xy

    def set_xy(self, xy):
        self._absolute_xy = xy


class GameObject:
    __idGenerator = IdGeneratorBase

    def __init__(self, visual: Visual, logic: Logic):
        self._visual = visual
        self._logic = logic
        self.__id = GameObject.__idGenerator.generate()

    def update(self, game_state: GameState):
        pass

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


class GOContainer:
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
    def container(self):
        return self.__container


class NPC(GameObject):
    """
    Самый простой тип npc: всего 3 вида поведения
    """
    def __init__(self, visual: Visual, logic: Logic, attitude=0):
        """
        attitude in {-1, 0, 1}: -1 -- враждебный,
                                 0 -- нейтральный,
                                 1 -- дружелюбный,
                          TODO: -2 -- берсерк, атакует ближайшего врага
        """
        super().__init__(visual, logic)
        self.__attitude = attitude
        pass

    def update(self, game_state: GameState):
        if game_state.id_turn == self.obj_id:
            if self.__attitude == 0:
                direction = random.randint(-1, 1)
                new_x = self.logic.xy[0] + screen.CELL_WIDTH * direction
                direction = random.randint(-1, 1)
                new_y = self.logic.xy[1] + screen.CELL_HEIGHT * direction
                self.logic.set_xy((new_x, new_y))
            elif self.__attitude == -1:
                # Идем ближайшим путем ко врагу
                mid = game_state.main_char_id
                m_chr = game_state.actors.get_obj_by_id(mid)
                m_x, m_y = m_chr.logix.xy
                x, y = self.logic.xy
                if x > m_x:
                    x -= screen.CELL_WIDTH
                elif x < m_x:
                    x += screen.CELL_WIDTH
                if y > m_y:
                    y -= screen.CELL_HEIGHT
                elif y < m_y:
                    y -= screen.CELL_HEIGHT
                self.logic.set_xy((x, y))
        # Update only visual part
        x, y = self.logic.xy
        x_cam, y_cam = game_state.camera_xy
        self.visual.set_xy((x - x_cam, y - y_cam))
