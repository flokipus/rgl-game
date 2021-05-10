from __future__ import annotations
import pygame

from common.gameobj.basegobj import GameObject
from common.gameobj.map.tilemaps import test_tile_map
from common.utils.utils import Vec2i
from gamelogic.controller import controller
from gamelogic.model import model  # ModelGame
from gamelogic.model import command_channel  # PlayerCommand
from gamelogic.view import view  # PlayerCommand
from gamelogic.view.graphics.cell_sprites import predef
from gamelogic.view.settings import colors, screen


def predefined_actors():
    actors = dict()

    input_channel = command_channel.UserCommandChannel()
    viking_sprite = pygame.image.load('./_gamedata/test2.png')
    print(viking_sprite.get_size())

    w, h = viking_sprite.get_size()
    scale = 2
    new_sprite = pygame.Surface((w * scale, h * scale), flags=pygame.SRCALPHA)
    viking_sprite.get_colorkey()
    for i in range(32):
        for j in range(32):
            pi_color = viking_sprite.get_at((i, j))
            for i_new in range(scale):
                for j_new in range(scale):
                    new_pos = (scale * i + i_new, scale * j + j_new)
                    new_sprite.set_at(new_pos, pi_color)

    main_hero = GameObject(pos=Vec2i(8, 18), name='main_char', sprite=new_sprite)
    actors[main_hero] = input_channel

    d_spr = predef.CELL_CREATOR.create('D', colors.BLUE, colors.TRANSPARENT_COLOR)
    dragon_gobj = GameObject(pos=Vec2i(10, 18), name='dragon', sprite=d_spr)
    ai_com_chan = command_channel.AIRandMoveCC()
    actors[dragon_gobj] = ai_com_chan

    n_spr = predef.CELL_CREATOR.create('@', colors.BW_GREY, colors.TRANSPARENT_COLOR)
    necro_gobj = GameObject(pos=Vec2i(12, 18), name='necromancer', sprite=n_spr)
    actors[necro_gobj] = ai_com_chan
    return actors, main_hero


def predefined_actors_2():
    actors = dict()
    m_spr = predef.CELL_CREATOR.create('@', colors.WHITE, colors.TRANSPARENT_COLOR)
    input_channel = command_channel.UserCommandChannel()
    main_hero = GameObject(pos=Vec2i(8, 18), name='main_char', sprite=m_spr)
    actors[main_hero] = input_channel
    return actors, main_hero


if __name__ == '__main__':

    """THIS SHOULD BE CONTROLLER!"""

    pygame.init()
    clock = pygame.time.Clock()

    tile_map = test_tile_map()
    actors, main_hero = predefined_actors()
    # actors, main_hero = predefined_actors_2()
    model_game = model.ModelGame(init_actors=actors, tile_map=tile_map, items=set(), player_character=main_hero)
    tile_size_pixels = Vec2i(screen.CELL_SIZE[0], screen.CELL_SIZE[1])
    view_game = view.ViewGame(model=model_game, screen_size=screen.SCREEN_SIZE, tile_size_pixels=tile_size_pixels,
                              fps=60)

    model_game.register_observer(view_game)

    time_end = pygame.time.get_ticks()

    frame_counter = 0

    time_intro = pygame.time.get_ticks()

    time_stamp_model1 = 0
    time_stamp_model2 = 0
    time_stamp_model_total = 0

    time_stamp_view1 = 0
    time_stamp_view2 = 0
    time_stamp_view_total = 0

    time_stamp_draw1 = 0
    time_stamp_draw2 = 0
    time_stamp_draw_total = 0

    while True:
        # print('------')
        time_begin = pygame.time.get_ticks()
        # print('still_have_ticks: {}'.format(time_begin - time_end))
        # print(time_begin)

        frame_counter += 1

        command_from_user = view_game.get_user_commands()
        if command_from_user == view.PlayerCommand.EXIT_GAME:
            curr_time = pygame.time.get_ticks()
            elapsed = curr_time - time_intro
            elapsed_sec = elapsed / 1000
            expected_frames = elapsed_sec * view_game.fps
            print('Time elapsed={}s; frames={}; expected frames={}'.format(elapsed_sec, frame_counter, expected_frames))
            print('Total time for model: {}ms; total time for view: {}ms; total time for drawing: {}ms'.format(time_stamp_model_total,
                                                                                 time_stamp_view_total,
                                                                                 time_stamp_draw_total))
            print('Per frame for model: {}ms; for view: {}ms; for drawing: {}ms'.format(time_stamp_model_total / frame_counter,
                                                                                        time_stamp_view_total / frame_counter,
                                                                                        time_stamp_draw_total / frame_counter))
            exit()
        elif command_from_user is not None and view_game.is_ready():
            # print('COMAND from user -> model: frame {}'.format(frame_counter))
            command_for_model = controller.USER_MOVES_TO_COMMAND[command_from_user]
            model_game.put_user_command(controller.USER_MOVES_TO_COMMAND[command_from_user])
            # if view_game.is_ready():
            #

        if view_game.is_ready():
            time_stamp_model1 = pygame.time.get_ticks()
            model_game.one_cycle_turns()
            time_stamp_model2 = pygame.time.get_ticks()
            time_stamp_model_total += (time_stamp_model2 - time_stamp_model1)

        time_stamp_view1 = pygame.time.get_ticks()
        view_game._gobj_event_handler.flush_event_queue()
        view_game._gobj_event_handler.apply_events_block()
        view_game.update_animations()
        view_game._gobj_event_handler.remove_finished_events()
        view_game._camera.update()
        time_stamp_view2 = pygame.time.get_ticks()
        time_stamp_view_total += (time_stamp_view2 - time_stamp_view1)

        # view_game.update()
        time_stamp_draw1 = pygame.time.get_ticks()
        view_game.redraw()
        time_stamp_draw2 = pygame.time.get_ticks()
        time_stamp_draw_total += (time_stamp_draw2 - time_stamp_draw1)



        time_end = pygame.time.get_ticks()
        elapsed = time_end - time_begin

        # print(time_end)
        # print('########## elapsed {} ms; game still has {} ms'.format(elapsed, (1000/view_game.fps - elapsed)))
        # print('##########', clock.get_fps())

        # DEBUG_stuttering.print_info()

        clock.tick(view_game.fps)
