import pygame

from gamelogic.view.settings.user_moves import PlayerCommand


KEY_TO_COMMAND = {
    pygame.K_UP: PlayerCommand.MOVE_UP,
    pygame.K_w: PlayerCommand.MOVE_UP,
    pygame.K_DOWN: PlayerCommand.MOVE_DOWN,
    pygame.K_s: PlayerCommand.MOVE_DOWN,
    pygame.K_LEFT: PlayerCommand.MOVE_LEFT,
    pygame.K_a: PlayerCommand.MOVE_LEFT,
    pygame.K_RIGHT: PlayerCommand.MOVE_RIGHT,
    pygame.K_d: PlayerCommand.MOVE_RIGHT,
    pygame.K_SPACE: PlayerCommand.MOVE_WAIT,
    pygame.K_ESCAPE: PlayerCommand.EXIT_GAME
}
