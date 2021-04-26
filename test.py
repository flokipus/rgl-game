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
    m_spr = predef.CELL_CREATOR.create('@', colors.WHITE, colors.TRANSPARENT_COLOR)
    input_channel = command_channel.UserCommandChannel()
    main_hero = GameObject(pos=Vec2i(8, 18), name='main_char', sprite=m_spr)
    actors[main_hero] = input_channel
    d_spr = predef.CELL_CREATOR.create('D', colors.BLUE, colors.TRANSPARENT_COLOR)
    dragon_gobj = GameObject(pos=Vec2i(10, 18), name='dragon', sprite=d_spr)
    ai_com_chan = command_channel.AIRandMoveCC()
    actors[dragon_gobj] = ai_com_chan
    n_spr = predef.CELL_CREATOR.create('@', colors.BW_GREY, colors.TRANSPARENT_COLOR)
    necro_gobj = GameObject(pos=Vec2i(12, 18), name='necromancer', sprite=n_spr)
    actors[necro_gobj] = ai_com_chan
    return actors, main_hero


if __name__ == '__main__':

    """THIS SHOULD BE CONTROLLER!"""

    pygame.init()
    clock = pygame.time.Clock()

    tile_map = test_tile_map()
    actors, main_hero = predefined_actors()
    model_game = model.ModelGame(init_actors=actors, tile_map=tile_map, items=set(), player_character=main_hero)
    tile_size_pixels = Vec2i(screen.CELL_SIZE[0], screen.CELL_SIZE[1])
    view_game = view.ViewGame(model=model_game, screen_size=screen.SCREEN_SIZE, tile_size_pixels=tile_size_pixels, fps=30)

    time_end = pygame.time.get_ticks()

    frame_counter = 0

    while True:
        # print('------')
        time_begin = pygame.time.get_ticks()
        # print('still_have_ticks: {}'.format(time_begin - time_end))
        # print(time_begin)

        frame_counter += 1

        command_from_user = view_game.get_user_commands()
        if command_from_user == view.PlayerCommand.EXIT_GAME:
            exit()
        elif command_from_user is not None:
            print('COMAND from user -> model: frame {}'.format(frame_counter))
            command_for_model = controller.USER_MOVES_TO_COMMAND[command_from_user]
            model_game.put_user_command(controller.USER_MOVES_TO_COMMAND[command_from_user])

        if view_game.is_ready():
            model_game.one_cycle_turns()
        events_from_model = model_game.unload_events()
        view_game.update(events_from_model)

        time_end = pygame.time.get_ticks()
        elapsed = time_end - time_begin
        # print(time_end)
        # print('##########', elapsed)
        # print('##########', clock.get_fps())
        clock.tick(view_game.fps)
