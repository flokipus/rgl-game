from settings import screen
from settings import colors
import math
import pygame
import asciicels
import visualisation
import game_objects


def manage_xy(old_xy, key):
    x, y = old_xy
    if key == 'up':
        return x, y - 5
    elif key == 'down':
        return x, y + 5
    elif key == 'left':
        return x - 5, y
    elif key == 'right':
        return x + 5, y
    else:
        return x, y


def manage_xy_pyg(old_xy, key):
    x, y = old_xy
    possible_interact = game_objects.get_list_of_close_objects(old_xy, screen.CELL_WIDTH)
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
    for obj in possible_interact:
        if type(obj) == game_objects.WallObject:
            dist_old = game_objects.dist(old_xy, obj.logic.absolute_xy)
            dist_new = game_objects.dist(new_xy, obj.logic.absolute_xy)
            if dist_new < dist_old:
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

for obj in game_objects.STATIC_OBJECTS:
    layer_num = obj.logic.layer_num
    visualisation_core.get_static_layers[layer_num].append(obj.visual)
for obj in game_objects.ACTIVE_OBJECTS:
    layer_num = obj.logic.layer_num
    visualisation_core.get_dynamic_layers[layer_num].add(obj.visual)

#########################################
## MAIN LOOP
#########################################
#########################################
screen_xy = (0, 0)
tmp = 0.0
keys_pressed = set()
while True:
    tmp = (tmp + 0.1) % (2 * math.pi)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("User quit the game")
            exit()
        else:
            process_pygame_event(event, keys_pressed)
    for key in keys_pressed:
        game_objects.main_hero.logic.set_xy(manage_xy_pyg(game_objects.main_hero.logic.absolute_xy, key))
        game_objects.main_hero.visual.set_xy(game_objects.main_hero.logic.absolute_xy)

    # for i in range(len(game_objects.ACTIVE_OBJECTS)):
    #     first_xy = game_objects.ACTIVE_OBJECTS[i].visual._xy
    #     for j in range(i+1, len(game_objects.ACTIVE_OBJECTS)):
    #         second_xy = game_objects.ACTIVE_OBJECTS[j].visual._xy
    #         if abs(first_xy[0] - second_xy[0]) + abs(first_xy[1] - second_xy[1]) < 20:
    #             print("OYOYOYO")
    for obj in game_objects.ACTIVE_OBJECTS:
        # obj.handler(e, visualisation_core)  # здесь может меняться visualisation. Дальше объекты надо отрисовать
        pass
    game_objects.super_go.visual._xy = (game_objects.xy[0] + 50 * math.cos(tmp), game_objects.xy[1] + 50 * math.sin(tmp))

    visualisation_core.draw_all()

    pygame.display.update()
    CLOCK.tick(screen.FPS)
