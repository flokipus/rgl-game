# -*- coding: utf-8 -*-

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Union
from math import sin, pi

from .visualisation import Visualisation
from common import global_parameters
from common.utils import utils


class IVisualState(ABC):
    @abstractmethod
    def enter(self, *, visual_owner: Visualisation, old_state: IVisualState) -> None:
        pass

    @abstractmethod
    def update(self, *, visual_owner: Visualisation) -> Union[None, IVisualState]:
        pass

    @abstractmethod
    def exit(self, *, visual_owner: Visualisation, next_state: IVisualState) -> None:
        pass

    @abstractmethod
    def ready(self) -> bool:
        pass


class PassiveStanding(IVisualState):
    """Just do nothing"""
    def enter(self, *, visual_owner: Visualisation, old_state: IVisualState) -> None:
        pass

    def update(self, *, visual_owner: Visualisation) -> Union[None, IVisualState]:
        pass

    def exit(self, *, visual_owner: Visualisation, next_state: IVisualState) -> None:
        pass

    def ready(self) -> bool:
        return True


class Standing(IVisualState):
    def __init__(self, original_xy: utils.Vec2i, amplitude: float = 3, time_to_move: float = 2):
        self.amplitude = amplitude
        self.enter_time = global_parameters.current_frame_time_ms / 1000
        self.time_to_move = time_to_move
        self.original_xy = original_xy

    def enter(self, *, visual_owner: Visualisation, old_state: IVisualState) -> None:
        self.enter_time = global_parameters.current_frame_time_ms / 1000
        self.original_xy = visual_owner.get_corner_xy()

    def update(self, *, visual_owner: Visualisation) -> Union[None, IVisualState]:
        current_time = global_parameters.current_frame_time_ms / 1000
        elapsed = current_time - self.enter_time
        r = elapsed / self.time_to_move
        new_pose = utils.Vec2i(0, abs(self.amplitude * sin(pi * r) ** 2)) + self.original_xy
        visual_owner.set_corner_xy(new_pose)
        return None

    def exit(self, *, visual_owner: Visualisation, next_state: IVisualState) -> None:
        visual_owner.set_corner_xy(self.original_xy)

    def ready(self) -> bool:
        return True


class Moving(IVisualState):
    def __init__(self,
                 dxy: utils.Vec2i,
                 time_to_move: float,
                 fps: int):
        self.dxy = dxy
        self.time_to_move = time_to_move
        self.initial_offset_xy = None
        self.time_begin = None
        self.fps = fps

    def enter(self, *, visual_owner: Visualisation, old_state: IVisualState) -> None:
        self.time_begin = global_parameters.current_frame_time_ms / 1000 - 1 / self.fps
        self.initial_offset_xy = visual_owner.get_corner_xy()

    def update(self, *, visual_owner: Visualisation) -> Union[None, IVisualState]:
        current_time = global_parameters.current_frame_time_ms / 1000
        elapsed_time = current_time - self.time_begin
        r = min(1.0, elapsed_time / self.time_to_move)
        visual_owner.set_corner_xy((self.initial_offset_xy + self.dxy * r))
        if elapsed_time > self.time_to_move:
            return Standing(self.initial_offset_xy + self.dxy)
        else:
            return None

    def exit(self, *, visual_owner: Visualisation, next_state: IVisualState) -> None:
        visual_owner.set_corner_xy(self.initial_offset_xy + self.dxy)

    def ready(self) -> bool:
        return False


class BouncingMotion(IVisualState):
    def __init__(self,
                 dxy: utils.Vec2i,
                 time_to_move: float,
                 amplitude: float,
                 fps: int):
        self.ready_flag = False
        self.dxy = dxy
        self.time_to_move = time_to_move
        self.initial_offset_xy = None
        self.time_begin = None
        self.amplitude = amplitude
        self.fps = fps

    def enter(self, *, visual_owner: Visualisation, old_state: IVisualState) -> None:
        self.time_begin = global_parameters.current_frame_time_ms / 1000 - 1 / self.fps
        self.initial_offset_xy = visual_owner.get_corner_xy()
        self.ready_flag = False

    def update(self, *, visual_owner: Visualisation) -> Union[None, IVisualState]:
        current_time = global_parameters.current_frame_time_ms / 1000
        elapsed_time = current_time - self.time_begin
        if elapsed_time > self.time_to_move:
            self.ready_flag = True
            return Standing(self.initial_offset_xy + self.dxy)
        r = min(1.0, elapsed_time / self.time_to_move)
        new_pose = utils.Vec2i(0, abs(self.amplitude * sin(pi*r)**2)) + self.initial_offset_xy + (self.dxy * r)
        visual_owner.set_corner_xy(new_pose)
        return None

    def exit(self, *, visual_owner: Visualisation, next_state: IVisualState) -> None:
        visual_owner.set_corner_xy(self.initial_offset_xy + self.dxy)

    def ready(self) -> bool:
        return self.ready_flag


class MeleeAttacking(IVisualState):
    def __init__(self, dxy: utils.Vec2i, time_to_attack: float, max_amplitude_ratio: float, fps: int) -> None:
        self.dxy = dxy
        self.time_to_attack = time_to_attack
        self.max_amplitude_ratio = max_amplitude_ratio
        self.fps = fps
        self.time_begin = None
        self.initial_offset_xy = None
        self.ready_flag = False

    def enter(self, *, visual_owner: Visualisation, old_state: IVisualState) -> None:
        self.time_begin = global_parameters.current_frame_time_ms / 1000 - 1 / self.fps
        self.initial_offset_xy = visual_owner.get_corner_xy()
        self.ready_flag = False

    @staticmethod
    def amplitude(r: float) -> float:
        return sin(2 * pi * r)

    def update(self, *, visual_owner: Visualisation) -> Union[None, IVisualState]:
        if self.ready_flag:
            return Standing(self.initial_offset_xy)
        current_time = global_parameters.current_frame_time_ms / 1000
        elapsed_time = current_time - self.time_begin
        r = min(1.0, elapsed_time / self.time_to_attack)
        if r < 1.0:
            delta_offset = self.dxy * MeleeAttacking.amplitude(r) * self.max_amplitude_ratio
            old_offset = visual_owner.get_corner_xy()
            visual_owner.set_corner_xy(old_offset + delta_offset)
            return None
        else:
            self.ready_flag = True

    def exit(self, *, visual_owner: Visualisation, next_state: IVisualState) -> None:
        visual_owner.set_corner_xy(self.initial_offset_xy)

    def ready(self) -> bool:
        return self.ready_flag
