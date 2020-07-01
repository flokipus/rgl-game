import sys
from settings import screen
from settings import colors
import pygame
import asciicels
import graphics
import gobject

from user_input import keyboard_processor
import commqueue


def manage_xy_pyg(old_xy, new_xy):
    x, y = old_xy
    possible_interact = gobject.ACTIVE_OBJECTS.get_objs_in_tile(new_xy)
    for obj in possible_interact:
        if type(obj) == gobject.WallObject:
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

draftsman = graphics.Draftsman()
visualisation_core = graphics.Graphics(MAIN_DISPLAY, 10, draftsman)

for obj_id in gobject.STATIC_OBJECTS.container:
    obj = gobject.STATIC_OBJECTS.container[obj_id]
    layer_num = obj.visual.layer_num
    visualisation_core.get_static_layers[layer_num].append(obj.visual)
for obj_id in gobject.ACTIVE_OBJECTS.container:
    obj = gobject.ACTIVE_OBJECTS.container[obj_id]
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
    gobj.logic.set_xy(manage_xy_pyg(gobject.main_hero.logic.xy, new_xy))
    gobj.visual.set_xy(gobject.main_hero.logic.xy)


class Command:
    def __init__(self, what_to_do, priority=0, **kwargs):
        self._kwdata = kwargs
        self._func = what_to_do
        self._priority = priority

    def __call__(self):
        return self._func(**self._kwdata)


def create_move_command(gobj, move_key):
    if move_key is None:
        return None
    if isinstance(gobj, gobject.LetterObject):
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
    gobject.central_object = gobject.inventory_object
    visualisation_core.add_visual_obj_to_dynamic_layer(gobject.inventory_object.visual, 5)


def close_inventory():
    gobject.central_object = gobject.main_hero
    for layer in visualisation_core.get_dynamic_layers:
        if gobject.inventory_object.visual in layer:
            layer.remove(gobject.inventory_object.visual)


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



user_mouse_events = [pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN]

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




def gobj_key_to_command(gobj, key):
    if gobj is gobject.main_hero:
        if key in move_keys:
            return create_move_command(gobj, key)
        elif key in inventory_keys:
            return create_open_inventory_command()
    elif gobj is gobject.inventory_object:
        if key in move_keys:
            return None
        elif key in escape_keys:
            return create_close_inventory_command()
    else:
        return None


def handle_input():
    exit_event = pygame.event.get([pygame.QUIT])
    if len(exit_event) > 0:
        print("user exit the game")
        sys.exit()
    kb_events = pygame.event.get(keyboard_processor.user_keyboard_events)
    key = user_keyboard_processor.process_input(kb_events)
    return key


def handle_command():
    pass


user_keyboard_processor = keyboard_processor.UserKeyboardProcessor(delay=0.5)
commands_queue = commqueue.CommandsPriorityQueue()
states = ['usr_move', 'usr_animation', 'npc_move', 'npc_animation']
state = states[0]

animations = commqueue.CommandsPriorityQueue()
npc_moves = commqueue.CommandsPriorityQueue()

while True:
    # 1: handle user input
    input_key = handle_input()
    # 2: transform user input to command
    command, priority = gobj_key_to_command(gobject.central_object, key)

    if state == 'waiting_user_move':

        state = 'waiting_user_animation'
        pass


    if command is not None:
        commands_queue.add_command(command, priority)
    # 3: TURN BASE SPECIFIC: take one command from top and execute it
    if not commands_queue.empty():
        command = commands_queue.pop()
        command()
    # 4:

    # 5:

    # 6: Visualize changes
    visualisation_core.draw_all()
    pygame.display.update()
    CLOCK.tick(screen.FPS)
