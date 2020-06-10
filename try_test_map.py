from settings import screen
from user_input import keyboard_processor
import test_map
import game_objects
import sparse_index
import visualisation
import pygame

###########
# Form actors
ACTORS = game_objects.GOContainer(indexing=sparse_index.SparseIndexing())
STATIC = game_objects.GOContainer(indexing=sparse_index.SparseIndexing())

ACTORS.add_object(test_map.dragon)
ACTORS.add_object(test_map.main_char)
for w in test_map.walls:
    ACTORS.add_object(w)
STATIC.add_object(test_map.map_gobj)
###########

###########
# Form draftsman
pygame.init()
MAIN_DISPLAY = pygame.display.set_mode(screen.SIZE)
draftsman = visualisation.IDraftsman()
visualisation_core = visualisation.IVisualisationCore(MAIN_DISPLAY, 10, draftsman)
for id_obj in ACTORS.container:
    gobj = ACTORS.get_obj_by_id(id_obj)
    visualisation_core.add_visual_obj_to_dynamic_layer(gobj.visual, gobj.visual.layer_num)
for id_obj in STATIC.container:
    gobj = STATIC.get_obj_by_id(id_obj)
    visualisation_core.add_visual_obj_to_static_layer(gobj.visual, gobj.visual.layer_num)
###########

# Start main circle
game_state = game_objects.GameState()
game_state.main_char_id = test_map.main_char.obj_id
game_state.camera_xy = (0, 0)
game_state.actors = ACTORS
# game_state.id_turn = game_state.main_char_id
game_state.id_turn = test_map.dragon.obj_id
game_state.battle_flag = True

kproc = keyboard_processor.UserKeyboardProcessor(delay=0.5)
move_keys = {pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT}

CLOCK = pygame.time.Clock()
turns_queue = list(ACTORS.container)
this_turn_ind = turns_queue.index(game_state.main_char_id)
main_char = test_map.main_char
print(test_map.dragon.obj_id)
print(test_map.main_char.obj_id)
while True:
    game_state.id_turn = turns_queue[this_turn_ind]

    # print(game_state.id_turn)
    # game_state.id_turn = all_ids[obj_index]
    ckey = kproc.process_input(pygame.event.get(keyboard_processor.user_keyboard_events))
    if ckey in move_keys and game_state.main_hero_move:
        move_xy = (0, 0)
        if ckey in [pygame.K_RIGHT, pygame.K_KP6]:
            move_xy = (screen.CELL_WIDTH, 0)
        if ckey in [pygame.K_LEFT, pygame.K_KP4]:
            move_xy = (-screen.CELL_WIDTH, 0)
        if ckey in [pygame.K_UP, pygame.K_KP8]:
            move_xy = (0, -screen.CELL_HEIGHT)
        if ckey in [pygame.K_DOWN, pygame.K_KP2]:
            move_xy = (0, screen.CELL_HEIGHT)
        x, y = main_char.logic.xy
        main_char.logic.set_xy((x + move_xy[0], y + move_xy[1]))
        main_char.visual.set_xy((x + move_xy[0], y + move_xy[1]))
        this_turn_ind = (this_turn_ind + 1) % len(turns_queue)
        game_state.main_hero_move = False
    elif not game_state.main_hero_move:
        for gid in ACTORS.container:
            game_state.id_turn = gid
            gobj = ACTORS.container[gid]
            gobj.update(game_state)
        game_state.main_hero_move = True

    visualisation_core.draw_all()
    pygame.display.update()
    CLOCK.tick(screen.FPS)
    pass
