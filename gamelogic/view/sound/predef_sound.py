import pygame
import pathlib


pygame.init()
game_root = pathlib.Path(__file__).parent.parent.parent.parent
swing_sound_path = game_root/'_gamedata'/'swing.wav'
axe_sound = pygame.mixer.Sound(swing_sound_path)
