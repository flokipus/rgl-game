import math
from cell_sprites import predef
from settings import screen, colors
from user_input import keyboard_processor

import sandmap
import pygame


class Command:
    def __init__(self, func, **kwargs):
        self._func = func
        self._kwargs = kwargs

    def exec(self):
        self._func(**self._kwargs)

    @property
    def func(self):
        return self._func

    @property
    def kwargs(self):
        return self._kwargs


class Order:
    pass


class SwiftMove(Order):
    def __init__(self, to_xy):
        self.to_xy = to_xy


class Sprite:
    def __init__(self, image):
        self._image = image
        self._xy_offset = (0, 0)

    def set_offset(self, xy):
        self._xy_offset = xy


class State:
    def update(self, gobj):
        pass

    def handle_order(self, gobj, order):
        pass

    def enter(self, gobj):
        pass

    def exit(self, gobj):
        pass


class ActorStand(State):
    def __init__(self):
        self.frame_tick = 0
        self.max_tick = 10

    def update(self, gobj):
        self.frame_tick = (self.frame_tick + 0.1) % self.max_tick
        # WE MUST MOVE IT: TO SPRITE
        # REASON: HIGH COUPLING
        sprite = gobj.sprite
        r = self.frame_tick/self.max_tick
        r*(1-r)
        y = r*(1-r)
        # x = r*(1-r) * math.sin(4 * math.pi * r * (1-r))
        x = 0
        sprite.set_offset((x, y))
        # END OF WE MUST
        return None

    def handle_order(self, gobj, order):
        if isinstance(order, SwiftMove):
            return ActorMove(order.to_xy)
        return None

    def enter(self, gobj):
        # gobj.set_sprite(Sprite(image=predef.human))
        pass

    def exit(self, gobj):
        gobj.sprite.set_offset((0, 0))


class ActorMove(State):
    def __init__(self, to_xy):
        self.frame_tick = 0
        self.max_tick = 10
        self.to_xy = to_xy
        self.init_xy = None
        self.dx = None
        self.dy = None

    def update(self, gobj):
        self.frame_tick += 1
        if self.frame_tick > self.max_tick:
            return ActorStand()
        #current x, y
        r = self.frame_tick / self.max_tick
        off_x = self.dx * self.frame_tick
        off_y = self.dy * self.frame_tick - 0.3 * math.sin(math.pi * r)
        gobj.sprite.set_offset((off_x, off_y))
        return None

    def enter(self, gobj):
        self.init_xy = gobj.xy
        t_x, t_y = self.to_xy
        i_x, i_y = self.init_xy
        self.dx = (t_x - i_x)/self.max_tick
        self.dy = (t_y - i_y)/self.max_tick

    def exit(self, gobj):
        gobj.set_xy(self.to_xy)
        gobj.sprite.set_offset((0, 0))


class GameObject:
    def __init__(self, init_state, init_xy, init_sprite):
        self._state = init_state
        self._xy = init_xy
        self._sprite = init_sprite
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

    @property
    def sprite(self):
        return self._sprite

    @property
    def xy(self):
        return self._xy

    def set_xy(self, new_xy):
        self._xy = new_xy


###########
# Form draftsman
pygame.init()

MAIN_DISPLAY = pygame.display.set_mode(screen.SIZE)

kproc = keyboard_processor.UserKeyboardProcessor(delay=0.5)
move_keys = {pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT}

human = GameObject(ActorStand(), (5, 5), Sprite(predef.human))
CLOCK = pygame.time.Clock()


while True:
    # корректная обработка input'а
    ckey = kproc.process_input(pygame.event.get(keyboard_processor.user_keyboard_events))
    order = None
    if ckey in move_keys:
        x, y = human.xy
        dx, dy = 0, 0
        if ckey == pygame.K_UP:
            dy = -1
        elif ckey == pygame.K_DOWN:
            dy = 1
        elif ckey == pygame.K_LEFT:
            dx = -1
        elif ckey == pygame.K_RIGHT:
            dx = 1
        order = SwiftMove((x+dx, y+dy))

    MAIN_DISPLAY.fill(colors.DEFAULT_BACKGROUND_COLOR)
    MAIN_DISPLAY.blit(sandmap.map_sprite, (0 * screen.CELL_WIDTH, 0 * screen.CELL_HEIGHT))

    x, y = human.xy
    dx, dy = human.sprite._xy_offset
    im_x, im_y = (x + dx) * screen.CELL_WIDTH, (y + dy) * screen.CELL_HEIGHT
    MAIN_DISPLAY.blit(human.sprite._image, (im_x, im_y))

    human.handle_order(order)
    human.update()

    pygame.display.update()
    CLOCK.tick(screen.FPS)
    pass
