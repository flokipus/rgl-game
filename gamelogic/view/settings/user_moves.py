# -*- coding: utf-8 -*-

import enum


class PlayerCommand(enum.Enum):
    MOVE_UP = 0
    MOVE_DOWN = 1
    MOVE_LEFT = 2
    MOVE_RIGHT = 3
    MOVE_WAIT = 4
    EXIT_GAME = 5
