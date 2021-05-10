import pygame
import os


pygame.init()
swing_path = os.path.dirname(os.path.realpath(__file__))
axe_sound = pygame.mixer.Sound(swing_path + '../../../../_gamedata/swing.wav')
