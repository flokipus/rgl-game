# -*- coding: utf-8 -*-

from __future__ import annotations
import pygame

from common.gameobj.basegobj import GameObject
from common.gameobj.characters.base_character import Character, CharacterAttributes, CharacterItems
from common.gameobj.items.items import OneHandAxe

from common.gameobj.map.tilemaps import test_tile_map
from common import global_parameters
from common.utils.utils import Vec2i
from gamelogic.controller import controller
from gamelogic.model import model  # ModelGame
from gamelogic.model import intention_channel  # PlayerCommand
from gamelogic.view import view  # PlayerCommand
from gamelogic.view.graphics.cell_sprites import predef
from gamelogic.view.settings import colors, screen
from gamelogic.view.timings.timings import Timings

from _DEBUG_perf import PERFOMANCE_DATA


def predefined_actors():
    actors = dict()

    input_channel = intention_channel.UserIntentionChannel()
    viking_sprite = pygame.image.load('./_gamedata/test2.png')

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
    print(new_sprite.get_size())
    main_hero_items = CharacterItems()
    main_hero_items.right_hand.put_item(OneHandAxe())
    main_hero = Character(pos=Vec2i(8, 18), name='main_char',
                          sprite=new_sprite,
                          attributes=CharacterAttributes(16, 14, 15, 10, 10),
                          inventory_capacity=20,
                          base_hp=1000,
                          character_items=main_hero_items)
    actors[main_hero] = input_channel

    d_spr = predef.CELL_CREATOR.create('D', colors.BLUE, colors.TRANSPARENT_COLOR)
    dragon_gobj = Character(pos=Vec2i(10, 18), name='dragon', sprite=d_spr,
                            attributes=CharacterAttributes(10, 10, 10, 10, 10),
                            inventory_capacity=20,
                            base_hp=100,
                            character_items=CharacterItems())
    ai_com_chan = intention_channel.AIRandMoveIC()
    actors[dragon_gobj] = ai_com_chan

    n_spr = predef.CELL_CREATOR.create('@', colors.BW_GREY, colors.TRANSPARENT_COLOR)
    necro_gobj = Character(pos=Vec2i(12, 18), name='necromancer', sprite=n_spr,
                           attributes=CharacterAttributes(10, 10, 10, 10, 10),
                           inventory_capacity=20,
                           base_hp=100,
                           character_items=CharacterItems())
    actors[necro_gobj] = ai_com_chan
    return actors, main_hero


def predefined_actors_2():
    actors = dict()
    m_spr = predef.CELL_CREATOR.create('@', colors.WHITE, colors.TRANSPARENT_COLOR)
    input_channel = intention_channel.UserIntentionChannel()
    main_hero = GameObject(pos=Vec2i(8, 18), name='main_char', sprite=m_spr)
    actors[main_hero] = input_channel
    return actors, main_hero


if __name__ == '__main__':

    """THIS SHOULD BE CONTROLLER!"""

    pygame.init()
    clock = pygame.time.Clock()

    tile_map = test_tile_map()
    actors, main_hero = predefined_actors()

    model_game = model.ModelGame(init_actors=actors, tile_map=tile_map, items=set(), player_character=main_hero)
    timings = Timings(time_to_move=0.3, time_to_attack=0.3, fps=60)
    view_game = view.ViewGame(model=model_game, screen_size=screen.SCREEN_SIZE, tile_size_pixels=screen.CELL_SIZE,
                              timings=timings, layers_num=4)

    model_game.register_observer(view_game)

    PERFOMANCE_DATA.fps = timings.fps
    PERFOMANCE_DATA.global_start()
    while True:
        PERFOMANCE_DATA.new_frame()
        global_parameters.current_frame_time_ms = pygame.time.get_ticks()
        # print(f'Begin frame: {global_parameters.current_frame_time_ms}ms')
        command_from_user = view_game.get_user_commands()
        if command_from_user == view.PlayerCommand.EXIT_GAME:
            PERFOMANCE_DATA.global_end()
            PERFOMANCE_DATA.print_finish_info()
            exit()
        elif command_from_user is not None and view_game.is_ready():
            PERFOMANCE_DATA.start_model()
            command_for_model = controller.USER_MOVES_TO_COMMAND[command_from_user]
            model_game.put_user_command(controller.USER_MOVES_TO_COMMAND[command_from_user])
            model_game.one_cycle_turns()
            PERFOMANCE_DATA.end_model()

        view_game.update()

        new_frame_time = pygame.time.get_ticks()
        frame_ms = new_frame_time - global_parameters.current_frame_time_ms
        if frame_ms > 1000 / view_game.timings.fps:
            print('=========================================')
            print(f'Frame drop: frame elapsed time: {frame_ms}')
            draw_elapsed = PERFOMANCE_DATA.draw_time_stamp_end - PERFOMANCE_DATA.draw_time_stamp_begin
            model_elapsed = PERFOMANCE_DATA.model_time_stamp_end - PERFOMANCE_DATA.model_time_stamp_begin
            layers_elapsed = PERFOMANCE_DATA.layer_build_stamp_end - PERFOMANCE_DATA.layer_build_stamp_begin
            visual_elapsed = PERFOMANCE_DATA.visuals_time_stamp_end - PERFOMANCE_DATA.visuals_time_stamp_begin
            bliting_elapsed = PERFOMANCE_DATA.blit_last_elapsed
            display_elapsed = PERFOMANCE_DATA.display_update_end - PERFOMANCE_DATA.display_update_begin
            print(f'Time for model {model_elapsed}ms; for view {visual_elapsed}ms; \n'
                  f'for layer building {layers_elapsed}ms; for drawing {draw_elapsed}ms;\n'
                  f'for bliting: {bliting_elapsed}ms; for display update: {display_elapsed}')
        else:
            # print(f'End frame: elapsed {frame_ms}ms')
            pass

        clock.tick(view_game.timings.fps)
