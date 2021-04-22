from __future__ import annotations
import pygame

from model.model import ModelGame
from view.view import ViewGame
from view.user_moves import PlayerCommand
from model.command_channel import UserCommandChannel, AIRandMoveCC
from graphics.cell_sprites.sprite_ascii import AsciiCellCreator
from gameobj.basegobj import GameObject
from gameobj.map.tilemaps import test_tile_map
from settings import colors
from settings.screen import FONT_SIZE, CELL_SIZE, SCREEN_SIZE
from utils.utils import Vec2i

from controller import controller


def predefined_actors():
    actors = dict()
    m_spr = AsciiCellCreator(pygame.font.Font(None, FONT_SIZE), CELL_SIZE).create(
        '@',
        colors.WHITE,
        colors.TRANSPARENT_COLOR
    )
    input_channel = UserCommandChannel()
    main_hero = GameObject(pos=Vec2i(8, 18), name='main_char', sprite=m_spr)
    actors[main_hero] = input_channel
    d_spr = AsciiCellCreator(pygame.font.Font(None, FONT_SIZE), CELL_SIZE).create(
        'D',
        colors.BLUE,
        colors.TRANSPARENT_COLOR
    )
    dragon_gobj = GameObject(pos=Vec2i(10, 18), name='dragon', sprite=d_spr)
    ai_com_chan = AIRandMoveCC()
    actors[dragon_gobj] = ai_com_chan
    n_spr = AsciiCellCreator(pygame.font.Font(None, FONT_SIZE), CELL_SIZE).create(
        '@',
        colors.BLACK_GREY,
        colors.TRANSPARENT_COLOR
    )
    necro_gobj = GameObject(pos=Vec2i(12, 18), name='necromancer', sprite=n_spr)
    actors[necro_gobj] = ai_com_chan
    return actors, main_hero


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()

    tile_map = test_tile_map()
    actors, main_hero = predefined_actors()
    model_game = ModelGame(init_actors=actors, tile_map=tile_map, items=set(), player_character=main_hero)
    tile_size_pixels = Vec2i(CELL_SIZE[0], CELL_SIZE[1])
    view_game = ViewGame(model=model_game, screen_size=SCREEN_SIZE, tile_size_pixels=tile_size_pixels)

    time_end = pygame.time.get_ticks()

    frame_counter = 0

    while True:
        # print('------')
        # time_begin = pygame.time.get_ticks()
        # print('still_have_ticks: {}'.format(time_begin - time_end))
        # print(time_begin)

        frame_counter += 1

        command_from_user = view_game.get_user_commands()
        if command_from_user == PlayerCommand.EXIT_GAME:
            exit()
        elif command_from_user is not None:
            print('command from user -> model: frame {}'.format(frame_counter))
            command_for_model = controller.USER_MOVES_TO_COMMAND[command_from_user]
            model_game.put_user_command(controller.USER_MOVES_TO_COMMAND[command_from_user])
        if view_game.is_ready():

            model_game.one_cycle_turns()
            # events_occured = model_game.unload_events()

        # View tick
        view_game.update(frame_counter)

        # time_end = pygame.time.get_ticks()
        # elapsed = time_end - time_begin
        # print(time_end)
        # print(elapsed)
        # print(clock.get_fps())
        clock.tick(30)
