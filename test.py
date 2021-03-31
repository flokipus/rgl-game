from graphics.cell_sprites import predef
from settings import screen, colors
from user_input import keyboard_processor
from gameobj.__gameobj import BaseMonster
from gameobj.states import ActorStandRealTime
from graphics.animations import *
from command.command import AttackOrder, SwiftMove

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


###########
# Form draftsman
pygame.init()

MAIN_DISPLAY = pygame.display.set_mode(screen.SCREEN_SIZE)

# kproc = keyboard_processor.UserKeyboardProcessor(delay=0.5)
kproc = keyboard_processor.UserKeyboardProcessor(delay=0)
move_keys = {pygame.K_w, pygame.K_UP, pygame.K_s, pygame.K_DOWN, pygame.K_a, pygame.K_LEFT, pygame.K_d, pygame.K_RIGHT}
attack_keys = {pygame.K_z, pygame.K_x}


map_objects = []

human_anim = StaticStandAnimation(Sprite(predef.human))
human = BaseMonster(ActorStandRealTime(), (5, 5), human_anim, 100, 15, map_objects)

dragon_anim = StaticStandAnimation(Sprite(predef.dragon))
dragon = BaseMonster(ActorStandRealTime(), (10, 5), dragon_anim, 100, 40, map_objects)

map_objects += [human, dragon]

CLOCK = pygame.time.Clock()


def draw_gobj(display, gobj):
    x, y = gobwj.xy
    dx, dy = gobj.sprite.offset_xy
    im_x, im_y = (x + dx) * screen.CELL_WIDTH, (y + dy) * screen.CELL_HEIGHT
    display.blit(gobj.sprite.surface, (im_x, im_y))


while True:

    ################################
    # корректная обработка input'а
    ckey = kproc.process_input(pygame.event.get(keyboard_processor.USER_KEYBOARD_EVENTS))
    order = None
    if ckey in move_keys:
        dx, dy = 0, 0
        if ckey in {pygame.K_UP, pygame.K_w}:
            dy = -1
        elif ckey in {pygame.K_DOWN, pygame.K_s}:
            dy = 1
        elif ckey in {pygame.K_LEFT, pygame.K_a}:
            dx = -1
        elif ckey in {pygame.K_RIGHT, pygame.K_d}:
            dx = 1
        x, y = human.xy
        # drag_x, drag_y = dragon.xy
        # if abs(dx + x - drag_x) < 1 and abs(dy + y - drag_y) < 1:
        #     command = AttackOrder((dx, dy), dragon)
        #     order_to_dragon = SufferOrder()
        #     damage = 1
        #     if dragon.is_alive():
        #         pass
        # else:
        order = SwiftMove((dx, dy))
    elif ckey in attack_keys:
        if ckey == pygame.K_z:
            order = AttackOrder((-1, 0))
        if ckey == pygame.K_x:
            order = AttackOrder((1, 0))
    #################################

    human.handle_order(order)
    human.update()

    dragon.update()

    MAIN_DISPLAY.fill(colors.DEFAULT_BACKGROUND_COLOR)
    MAIN_DISPLAY.blit(sandmap.map_sprite, (0 * screen.CELL_WIDTH, 0 * screen.CELL_HEIGHT))
    draw_gobj(MAIN_DISPLAY, human)
    draw_gobj(MAIN_DISPLAY, dragon)
    pygame.display.update()
    CLOCK.tick(screen.FPS)
    pass
