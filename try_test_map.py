from settings import screen
from user_input import keyboard_processor
import sandmap
import gobject
import sparse_index
import graphics
import pygame

###########
# Form actors
ACTORS = gobject.GOContainer(indexing=sparse_index.SparseIndexing(sandmap.cells_count_x, sandmap.cells_count_y))
STATIC = gobject.GOContainer(indexing=sparse_index.SparseIndexing(sandmap.cells_count_x, sandmap.cells_count_y))

ACTORS.add_object(sandmap.dragon)
ACTORS.add_object(sandmap.main_char)
for w in sandmap.walls:
    ACTORS.add_object(w)
STATIC.add_object(sandmap.map_gobj)
###########

###########
# Form draftsman
pygame.init()
MAIN_DISPLAY = pygame.display.set_mode(screen.SIZE)
draftsman = graphics.Draftsman()
visualisation_core = graphics.Graphics(MAIN_DISPLAY, 10, draftsman)
for id_obj in ACTORS.container:
    gobj = ACTORS.get_obj_by_id(id_obj)
    visualisation_core.add_obj_to_dynamic_layer(gobj, gobj.layer)
for id_obj in STATIC.container:
    gobj = STATIC.get_obj_by_id(id_obj)
    visualisation_core.add_obj_to_static_layer(gobj, gobj.layer)
###########

# Start main circle
game_data = gobject.GameData()
game_data.main_char_id = sandmap.main_char.id
game_data.camera_xy = (0, 0)
game_data.actors = ACTORS
# game_state.id_turn = game_state.main_char_id
game_data.id_turn = sandmap.dragon.id
game_data.battle_flag = True
game_data.map_size = (sandmap.cells_count_x, sandmap.cells_count_y)

kproc = keyboard_processor.UserKeyboardProcessor(delay=0.5)
move_keys = {pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT}

CLOCK = pygame.time.Clock()
turns_queue = list(ACTORS.container)
this_turn_ind = turns_queue.index(game_data.main_char_id)
main_char = sandmap.main_char
print(sandmap.dragon.id)
print(sandmap.main_char.id)


while True:
    # корректная обработка input'а
    ckey = kproc.process_input(pygame.event.get(keyboard_processor.user_keyboard_events))

    if ckey in move_keys and game_data.main_hero_move:
        move_xy = (0, 0)
        if ckey in [pygame.K_RIGHT, pygame.K_KP6]:
            move_xy = (1, 0)
        if ckey in [pygame.K_LEFT, pygame.K_KP4]:
            move_xy = (-1, 0)
        if ckey in [pygame.K_UP, pygame.K_KP8]:
            move_xy = (0, -1)
        if ckey in [pygame.K_DOWN, pygame.K_KP2]:
            move_xy = (0, 1)
        x, y = main_char.xy

        ACTORS.get_control_of_obj(main_char.id)
        new_x, new_y = x + move_xy[0], y + move_xy[1]
        if gobject.check_if_in_map((new_x, new_y), game_data.map_size):
            main_char.set_xy((new_x, new_y))
        ACTORS.return_control_of_obj(main_char)
        game_data.main_hero_move = False
    elif not game_data.main_hero_move:
        for gid in ACTORS.container:
            game_data.id_turn = gid
            gobj = ACTORS.get_control_of_obj(gid)
            gobj.update(game_data)
            ACTORS.return_control_of_obj(gobj)
        game_data.main_hero_move = True
    visualisation_core.draw_all()
    pygame.display.update()
    CLOCK.tick(screen.FPS)
    pass
