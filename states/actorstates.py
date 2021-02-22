from .basic import BaseState
from order.order import *
from gameobj.gameobj import BaseGameObject, BaseMonster
from graphics.animations import *

import math


class ActorAttack(BaseState):
    def __init__(self, attack_move_xy, speed=4, enemy=None, max_tick=100):
        self.frame_tick = 0
        self.actual_max_tick = max_tick
        self.attack_move_xy = attack_move_xy
        self.enemy = enemy
        self.speed = speed

    def update(self, gobj: BaseGameObject):
        self.frame_tick += self.speed
        gobj.next_frame()
        if self.frame_tick > self.actual_max_tick:
            return ActorStandRealTime()
        return None

    def handle_order(self, gobj: BaseGameObject, order: Order):
        return None

    def enter(self, gobj: BaseGameObject):
        if self.enemy is not None:
            print('start attacking monster!')
        old_animation = gobj.get_animation
        # TODO: fix this shit at release curwa
        gobj.set_animation(StaticAttackAnimation(old_animation.sprite, self.attack_move_xy,
                                                 self.actual_max_tick // self.speed, 0.5, 0.5))

    def exit(self, gobj):
        if self.enemy is not None:
            print('stop attacking monster!')
            self.enemy.handle_order(None)


class ActorStandRealTime(BaseState):
    def __init__(self, speed=1, max_tick=100):
        self.frame_tick = 0
        self.max_tick = max_tick
        self.speed = speed

    def update(self, gobj):
        gobj.next_frame()
        return None

    def handle_order(self, gobj, order):
        if isinstance(order, SwiftMove):
            # check xy_target. If
            new_xy = gobj.xy[0] + order.dxdy[0], gobj.xy[1] + order.dxdy[1]
            return ActorMoveRealTime(order.dxdy)
        elif isinstance(order, AttackOrder):
            return ActorAttack(order.attack_dxdy)
        return None

    def enter(self, gobj):
        old_animation = gobj.get_animation
        # TODO: fix this shit at release curwa
        gobj.set_animation(StaticStandAnimation(old_animation.sprite, self.max_tick))
        pass

    def exit(self, gobj):
        pass


class ActorMoveRealTime(BaseState):
    def __init__(self, dxdy, speed=0.3, max_tick=100):
        self.frame_tick = 0
        self.max_tick = max_tick
        self.speed = speed
        length = math.sqrt(dxdy[0]**2 + dxdy[1]**2)
        self.dxdy = dxdy[0]/length, dxdy[1]/length

    def update(self, gobj: BaseMonster):
        gobj.next_frame()
        self.frame_tick += 1
        if self.frame_tick > self.max_tick:
            return ActorStandRealTime()
        x, y = gobj.xy
        x, y = (x + self.speed * self.dxdy[0], y + self.speed * self.dxdy[1])
        # CHECK IF POSSIBLE TO MOVE
        for actor in gobj.map_objects:
            ob_x, ob_y = actor.xy
            if (ob_x, ob_y) == gobj.xy:
                continue
            if math.sqrt((ob_x - x)**2 + (ob_y-y)**2) < 1:
                return ActorAttack(self.dxdy, enemy=actor)
        gobj.set_xy((x, y))
        return None

    def handle_order(self, gobj, order):
        if isinstance(order, SwiftMove):
            self.dxdy = order.dxdy
        elif isinstance(order, AttackOrder):
            return ActorAttack(order.attack_dxdy)
        else:
            return ActorStandRealTime()

    def enter(self, gobj: BaseGameObject):
        old_animation = gobj.get_animation
        if not isinstance(old_animation, StaticMoveAnimation):
            gobj.set_animation(StaticMoveAnimation(old_animation.sprite, self.dxdy, self.max_tick))
        pass

    def exit(self, gobj: BaseGameObject):
        pass
