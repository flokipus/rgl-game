from __future__ import annotations
from typing import Union
from time import time
from math import sin, cos, pi

from gamelogic.view.visualisation.visualisation import Visualisation
from .basic import VisualState
from common.utils import utils


class Standing(VisualState):
    def __init__(self, amplitude: float = 3, time_to_move: float = 2):
        self.amplitude = amplitude
        self.enter_time = None
        self.time_to_move = time_to_move
        self.original_xy = None

    def enter(self, *, owner: Visualisation, old_state: VisualState) -> None:
        self.enter_time = time()
        self.original_xy = owner.get_corner_xy()

    def update(self, *, owner: Visualisation) -> Union[None, VisualState]:
        current_time = time()
        elapsed = current_time - self.enter_time
        r = elapsed / self.time_to_move
        new_pose = utils.Vec2i(0, -abs(self.amplitude * sin(pi * r) ** 2)) + self.original_xy
        owner.set_corner_xy(new_pose)
        return None

    def exit(self, *, owner: Visualisation, next_state: VisualState) -> None:
        owner.set_corner_xy(self.original_xy)

    def ready(self) -> bool:
        return True


class Moving(VisualState):
    def __init__(self,
                 dxy: utils.Vec2i,
                 time_to_move: float,
                 fps: int):
        self.dxy = dxy
        self.time_to_move = time_to_move
        self.initial_offset_xy = None
        self.time_begin = 0.0
        self.fps = fps

    def update(self, *, owner: Visualisation) -> Union[None, VisualState]:
        current_time = time()
        elapsed_time = current_time - self.time_begin
        r = min(1.0, elapsed_time / self.time_to_move)
        # #####
        # _DEBUG_stuttering.current_frame_state = type(self)
        # _DEBUG_stuttering.current_frame_r = r
        # #####
        owner.set_corner_xy((self.initial_offset_xy + self.dxy * r))
        if elapsed_time > self.time_to_move:
            return Standing()
        else:
            return None

    def enter(self, *, owner: Visualisation, old_state: VisualState) -> None:
        self.time_begin = time() - 1/self.fps
        self.initial_offset_xy = owner.get_corner_xy()

    def exit(self, *, owner: Visualisation, next_state: VisualState) -> None:
        owner.set_corner_xy(self.initial_offset_xy + self.dxy)

    def ready(self) -> bool:
        return False


class BouncingMotion(VisualState):
    def __init__(self,
                 dxy: utils.Vec2i,
                 time_to_move: float,
                 amplitude: float,
                 fps: int):
        self.ready_flag = False
        self.dxy = dxy
        self.time_to_move = time_to_move
        self.initial_offset_xy = None
        self.time_begin = 0.0
        self.amplitude = amplitude
        self.fps = fps

    def enter(self, *, owner: Visualisation, old_state: VisualState) -> None:
        self.time_begin = time() - 1/self.fps
        self.initial_offset_xy = owner.get_corner_xy()
        self.ready_flag = False

    def exit(self, *, owner: Visualisation, next_state: VisualState) -> None:
        owner.set_corner_xy(self.initial_offset_xy + self.dxy)

    def update(self, *, owner: Visualisation) -> Union[None, VisualState]:
        if self.ready_flag:
            return Standing()
        current_time = time()
        elapsed_time = current_time - self.time_begin
        if elapsed_time > self.time_to_move:
            self.ready_flag = True
        r = min(1.0, elapsed_time / self.time_to_move)
        #####
        # _DEBUG_stuttering.current_frame_state = type(self)
        # _DEBUG_stuttering.current_frame_r = r
        #####
        new_pose = utils.Vec2i(0, -abs(self.amplitude * sin(pi*r)**2)) + self.initial_offset_xy + (self.dxy * r)
        owner.set_corner_xy(new_pose)
        return None

    def ready(self) -> bool:
        return self.ready_flag


class MeleeAttacking(VisualState):
    def __init__(self, dxy: utils.Vec2i, time_to_attack: float, max_amplitude_ratio: float, fps: int) -> None:
        self.dxy = dxy
        self.time_to_attack = time_to_attack
        self.max_amplitude_ratio = max_amplitude_ratio
        self.fps = fps
        self.time_begin = None
        self.initial_offset_xy = None
        self.ready_flag = False

    def enter(self, *, owner: Visualisation, old_state: VisualState) -> None:
        self.time_begin = time() - 1/self.fps
        self.initial_offset_xy = owner.get_corner_xy()
        self.ready_flag = False

    def exit(self, *, owner: Visualisation, next_state: VisualState) -> None:
        owner.set_corner_xy(self.initial_offset_xy)

    @staticmethod
    def amplitude(r: float) -> float:
        return sin(2 * pi * r)

    def update(self, *, owner: Visualisation) -> Union[None, VisualState]:
        if self.ready_flag:
            return Standing()
        current_time = time()
        elapsed_time = current_time - self.time_begin
        r = min(1.0, elapsed_time / self.time_to_attack)
        if r < 1.0:
            delta_offset = self.dxy * MeleeAttacking.amplitude(r) * self.max_amplitude_ratio
            old_offset = owner.get_corner_xy()
            owner.set_corner_xy(old_offset + delta_offset)
            return None
        else:
            self.ready_flag = True

    def ready(self) -> bool:
        return self.ready_flag
