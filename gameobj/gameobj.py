from states.basic import BaseState
from graphics.animations import Animation

from queue import Queue


class BaseGameObject:
    def __init__(self, init_state, init_xy, init_animation: Animation):
        self._state = init_state
        self._xy = init_xy
        self._animation = init_animation
        pass

    def update(self):
        return_state = self._state.update(self)
        if return_state is not None:
            self._state.exit(self)
            self._state = return_state
            self._state.enter(self)

    def handle_order(self, order):
        return_state = self._state.handle_order(self, order)
        if return_state is not None:
            self._state.exit(self)
            self._state = return_state
            self._state.enter(self)

    def next_frame(self):
        return self._animation.next_sprite()

    @property
    def sprite(self):
        return self._animation.sprite

    @property
    def xy(self):
        return self._xy

    def set_xy(self, new_xy):
        self._xy = new_xy

    def set_animation(self, new_animation: Animation):
        self._animation = new_animation

    @property
    def get_animation(self) -> Animation:
        return self._animation


class BaseMonster(BaseGameObject):
    def __init__(self, init_state: BaseState,
                 init_xy: tuple,
                 animation: Animation,
                 hp: int,
                 melee_attack: int,
                 map_objects: list,
                 aggressive: bool = False):
        BaseGameObject.__init__(self, init_state, init_xy, animation)
        self.order_queue = Queue()
        self.aggressive = aggressive
        self.hp = hp
        self.melee_attack = melee_attack
        self.map_objects = map_objects

    def add_order(self, order):
        self.order_queue.put(order)
