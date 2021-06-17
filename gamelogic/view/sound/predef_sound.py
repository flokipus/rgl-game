# -*- coding: utf-8 -*-

import pygame
import pathlib


pygame.init()
game_root = pathlib.Path(__file__).parent.parent.parent.parent
swing_sound_path = game_root/'_gamedata'/'swing.wav'
gore_sound_path = game_root/'_gamedata'/'gore_hit.wav'
axe_sound = pygame.mixer.Sound(swing_sound_path)
gore_sound = pygame.mixer.Sound(gore_sound_path)

