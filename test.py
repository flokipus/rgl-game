from settings import screen
from settings import colors
import math
import pygame
import asciicels
import visualisation
import game_objects
import time


def manage_xy_pyg(old_xy, key):
    x, y = old_xy

    # if len(possible_interact) > 0:
    #     print(len(possible_interact))
    if key == pygame.K_UP:
        new_xy = x, y - 5
    elif key == pygame.K_DOWN:
        new_xy = x, y + 5
    elif key == pygame.K_LEFT:
        new_xy = x - 5, y
    elif key == pygame.K_RIGHT:
        new_xy = x + 5, y
    else:
        new_xy = x, y

    possible_interact = game_objects.ACTIVE_OBJECTS.get_objs_in_tile(new_xy)
    for obj in possible_interact:
        if type(obj) == game_objects.WallObject:
            # dist_old = game_objects.dist(old_xy, obj.logic.xy)
            # dist_new = game_objects.dist(new_xy, obj.logic.xy)
            # if dist_new < dist_old:
            #     return old_xy
            return old_xy
    return new_xy


def process_pygame_event(event, pressed_keys: set):
    if event.type == pygame.KEYDOWN:
        pressed_keys.add(event.key)
    elif event.type == pygame.KEYUP:
        pressed_keys.remove(event.key)
    pass


pygame.init()
CLOCK = pygame.time.Clock()
print(asciicels.sand_background)
print(screen)
MAIN_DISPLAY = pygame.display.set_mode(screen.SIZE)
MAIN_DISPLAY.fill(colors.DEFAULT_BACKGROUND_COLOR)

draftsman = visualisation.IDraftsman()
visualisation_core = visualisation.IVisualisationCore(MAIN_DISPLAY, 4, draftsman)

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
screen_xy = (0, 0)
tmp = 0.0
keys_pressed = set()


class KeyboardInput:
    def __init__(self):
        self._keys_pressed = {}

    def press_key(self, key):
        self._keys_pressed[key] = time.time()

    def release_key(self, key):
        if key in self._keys_pressed:
            self._keys_pressed.pop(key)

    @property
    def keys_pressed(self):
        return self._keys_pressed


def is_movement_key(key):
    return key == pygame.K_UP or key == pygame.K_DOWN or key == pygame.K_LEFT or key == pygame.K_RIGHT


class InputHandler:
    def __init__(self, input_device, commands):
        self._input_device = input_device
        self._key_pressed_time = {}
        self.__commands = commands

    def handle(self):
        self._eval_time_pressed()
        self._pressed_time_to_commands.append()
        raise NotImplementedError

    def _eval_time_pressed(self):
        self._key_pressed_time.clear()
        curr_time = time.time()
        for key in self._input_device.keys_pressed:
            elapsed_time = curr_time - self._input_device.keys_pressed[key]
            self._key_pressed_time[key] = elapsed_time

    def _pressed_time_to_commands(self):
        for key in self._key_pressed_time:
            if is_movement_key(key):
                pass
            else:
                raise NotImplementedError
        pass

    def _movement_to_command(self):
        pass


def handle_pygame_events(events, input_device):
    for event in events:
        if event.type == pygame.QUIT:
            print("User quit the game")
            exit()
        elif event.type == pygame.KEYUP:
            input_device.release_key(event.key)
        elif event.type == pygame.KEYDOWN:
            input_device.press_key(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
        elif event.type == pygame.MOUSEMOTION:
            pass
        elif event.type == pygame.MOUSEWHEEL:
            pass


def handle_keyboard_input(input_keyboard: KeyboardInput, input_mouse=None):
    curr_time = time.time()
    for key in input.keys_pressed:
        elapsed_time = curr_time - input.keys_pressed[key]


class GameEventHandler:

    def move_character(self, delta_xy):
        pass

    def create(self, obj):
        pass

    def destroy(self, obj):
        pass

    def hit(self, obj1):
        pass


while True:
    tmp = (tmp + 0.1) % (2 * math.pi)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("User quit the game")
            exit()
        else:
            process_pygame_event(event, keys_pressed)
    for key in keys_pressed:
        game_objects.main_hero.logic.set_xy(manage_xy_pyg(game_objects.main_hero.logic.xy, key))
        game_objects.main_hero.visual.set_xy(game_objects.main_hero.logic.xy)

    # for obj in game_objects.ACTIVE_OBJECTS:
    #     # obj.handler(e, visualisation_core)  # здесь может меняться visualisation. Дальше объекты надо отрисовать
    #     pass
    # game_objects.super_go.visual._xy = (game_objects.xy[0] + 50 * math.cos(tmp), game_objects.xy[1] + 50 * math.sin(tmp))

    visualisation_core.draw_all()

    pygame.display.update()
    CLOCK.tick(screen.FPS)
