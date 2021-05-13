# -*- coding: utf-8 -*-

class Timings:
    """Класс-контейнер, содержит информацию о времени анимаций различных действий"""
    def __init__(self, time_to_move: float, time_to_attack: float, fps: int):
        self.time_to_move = time_to_move
        self.time_to_attack = time_to_attack
        self.fps = fps
