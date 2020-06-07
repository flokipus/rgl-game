import sys
from settings import screen
from settings import colors
import math
import pygame
import asciicels
import visualisation
import game_objects
import time
import heapq
import itertools


def manage_xy_pyg(old_xy, new_xy):
    x, y = old_xy
    possible_interact = game_objects.ACTIVE_OBJECTS.get_objs_in_tile(new_xy)
    for obj in possible_interact:
        if type(obj) == game_objects.WallObject:
            # dist_old = game_objects.dist(old_xy, obj.logic.xy)
            # dist_new = game_objects.dist(new_xy, obj.logic.xy)
            # if dist_new < dist_old:
            #     return old_xy
            return old_xy
    return new_xy


pygame.init()
CLOCK = pygame.time.Clock()
print(asciicels.sand_background)
print(screen)
MAIN_DISPLAY = pygame.display.set_mode(screen.SIZE)
MAIN_DISPLAY.fill(colors.DEFAULT_BACKGROUND_COLOR)

draftsman = visualisation.IDraftsman()
visualisation_core = visualisation.IVisualisationCore(MAIN_DISPLAY, 10, draftsman)

for obj_id in game_objects.STATIC_OBJECTS.id_to_objs:
    obj = game_objects.STATIC_OBJECTS.id_to_objs[obj_id]
    layer_num = obj.visual.layer_num
    visualisation_core.get_static_layers[layer_num].append(obj.visual)
for obj_id in game_objects.ACTIVE_OBJECTS.id_to_objs:
    obj = game_objects.ACTIVE_OBJECTS.id_to_objs[obj_id]
    layer_num = obj.visual.layer_num
    visualisation_core.get_dynamic_layers[layer_num].add(obj.visual)

#########################################
## MAIN LOOP
#########################################
#########################################


def try_to_move(gobj, move_xy):
    print("We are trying to move {} by {}".format(gobj, move_xy))
    x, y = gobj.logic.xy
    mx, my = move_xy
    new_xy = (x + mx, y + my)
    gobj.logic.set_xy(manage_xy_pyg(game_objects.main_hero.logic.xy, new_xy))
    gobj.visual.set_xy(game_objects.main_hero.logic.xy)


class Command:
    def __init__(self, what_to_do, priority=0, **kwargs):
        self._kwdata = kwargs
        self._func = what_to_do
        self._priority = priority

    def __call__(self):
        return self._func(**self._kwdata)


def create_move_command(gobj, move_key):
    if key is None:
        return None
    if isinstance(gobj, game_objects.LetterObject):
        move_xy = (0, 0)
        if move_key in [pygame.K_RIGHT, pygame.K_KP6]:
            move_xy = (screen.CELL_WIDTH, 0)
        if move_key in [pygame.K_LEFT, pygame.K_KP4]:
            move_xy = (-screen.CELL_WIDTH, 0)
        if move_key in [pygame.K_UP, pygame.K_KP8]:
            move_xy = (0, -screen.CELL_HEIGHT)
        if move_key in [pygame.K_DOWN, pygame.K_KP2]:
            move_xy = (0, screen.CELL_HEIGHT)
        return Command(try_to_move, priority=10, gobj=gobj, move_xy=move_xy)
    else:
        return None


def open_inventory():
    game_objects.central_object = game_objects.inventory_object
    visualisation_core.add_visual_obj_to_dynamic_layer(game_objects.inventory_object.visual, 5)


def close_inventory():
    game_objects.central_object = game_objects.main_hero
    for layer in visualisation_core.get_dynamic_layers:
        if game_objects.inventory_object.visual in layer:
            layer.remove(game_objects.inventory_object.visual)


def create_open_inventory_command():
    return Command(open_inventory, priority=9)


def create_quit_command():
    return Command(exit, priority=0)


def create_close_inventory_command():
    return Command(close_inventory, priority=9)

# QUIT              none
# ACTIVEEVENT       gain, state
# KEYDOWN           key, mod, unicode, scancode
# KEYUP             key, mod
# MOUSEMOTION       pos, rel, buttons
# MOUSEBUTTONUP     pos, button
# MOUSEBUTTONDOWN   pos, button
# JOYAXISMOTION     joy, axis, value
# JOYBALLMOTION     joy, ball, rel
# JOYHATMOTION      joy, hat, value
# JOYBUTTONUP       joy, button
# JOYBUTTONDOWN     joy, button
# VIDEORESIZE       size, w, h
# VIDEOEXPOSE       none
# USEREVENT         code


user_keyboard_events = [pygame.KEYDOWN, pygame.KEYUP]
user_mouse_events = [pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN]


class UserKeyboardProcessor:
    def __init__(self, delay):
        self.__last_pressed_key = None
        self.__time_press = 0.0
        self.__delay = delay
        self.__flag_first_time_process = True

    def process_input(self, pyg_events):
        for event in pyg_events:
            if event.type not in user_keyboard_events:
                raise RuntimeError
            self._process_key_event(event)
        return self._final_key()

    def _process_key_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.__last_pressed_key = event.key
            self.__time_press = time.time()
            self.__flag_first_time_process = True
        elif event.type == pygame.KEYUP:
            if event.key == self.__last_pressed_key:
                self.__last_pressed_key = None

    def _final_key(self):
        """
        Обрабатывается первая нажатая клавиша;
        если клавиша нажата более self._delay секунд, то она также
        пораждает соответствующую ей команду;
        если несколько клавиш нажаты более self._delay секунд,
        то пораждает команду та, которая нажата дольше всего;
        если не нажата ни одна, то возвращается None
        """
        if self.__last_pressed_key is None:
            return None
        if self.__flag_first_time_process:
            self.__flag_first_time_process = False
            return self.__last_pressed_key
        else:
            current_time = time.time()
            delta = current_time - self.__time_press
            if delta > self.__delay:
                return self.__last_pressed_key
            else:
                return None


move_keys = {pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT}
inventory_keys = {pygame.K_i, pygame.K_TAB}
escape_keys = {pygame.K_ESCAPE}


# def key_to_command(main_gobj, key):
#     if key in move_keys:
#         return create_move_command(main_gobj, key)
#     else:
#         return None
#     # if key in open_inventory_keys:
#     #     create_open_inventory_command(main_gobj, key)


commands = []
user_keyboard_processor = UserKeyboardProcessor(delay=0.5)


def gobj_key_to_command(gobj, key):
    if gobj is game_objects.main_hero:
        if key in move_keys:
            return create_move_command(gobj, key)
        elif key in inventory_keys:
            return create_open_inventory_command()
    elif gobj is game_objects.inventory_object:
        if key in move_keys:
            return None
        elif key in escape_keys:
            return create_close_inventory_command()
    else:
        return None


import queue
import itertools


class CommandsPriorityQueue:
    def __init__(self, capacity=0):
        self.__queue = queue.PriorityQueue(capacity)
        self.__iter = itertools.count(start=0, step=1)

    def add_command(self, command, priority, block=False, timeout=None):
        self.__queue.put((priority, next(self.__iter), command), block, timeout)

    def get_top(self, block=False, timeout=None):
        prio, count, command = self.__queue.get(block, timeout)
        return command

    def empty(self):
        return self.__queue.empty()

    def size(self):
        return self.__queue.qsize()


def handle_input():
    exit_event = pygame.event.get([pygame.QUIT])
    if len(exit_event) > 0:
        print("user exit the game")
        sys.exit()

    kb_events = pygame.event.get(user_keyboard_events)
    key = user_keyboard_processor.process_input(kb_events)

    return key

def handle_command():
    pass


commands_queue = CommandsPriorityQueue()
while True:
    # 1: handle user input
    key = handle_input()
    # 2: transform user input to commands
    command, priority = gobj_key_to_command(game_objects.central_object, key)
    if command is not None:
        commands_queue.add_command(command, priority)
    # 3: TURN BASE SPECIFIC: take one command from top and execute it
    if not commands_queue.empty():
        command = commands.pop()
        command()
    # 4:

    # 5:

    # 6: Visualize changes
    visualisation_core.draw_all()
    pygame.display.update()
    CLOCK.tick(screen.FPS)
