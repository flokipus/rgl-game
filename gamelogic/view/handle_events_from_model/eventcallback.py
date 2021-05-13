# -*- coding: utf-8 -*-

from common.event import event
from common.utils import utils
from gamelogic.view.camera import camera_states
from gamelogic.view.visualisation import visualisation_states as visual_states
from gamelogic.view.visualisation.visual_container import VisualisationsContainer
from gamelogic.view.sound import axe_sound


class GobjEventsCallbacks:
    def __init__(self, timings, tile_size_pixels: utils.Vec2i):
        self._timings = timings
        self._tile_size_pixels = tile_size_pixels

    def gobj_wait_callback(self,
                           event_occured: event.GobjWaitEvent,
                           visualisations: VisualisationsContainer) -> None:
        pass

    def gobj_move_callback(self,
                           event_occured: event.GobjMoveEvent,
                           visualisations: VisualisationsContainer) -> None:
        new_xy = visualisations.cell_ij_to_pixel(event_occured.to_ij)
        dxy = visualisations.cell_ij_to_pixel(event_occured.to_ij - event_occured.from_ij)
        assert visualisations.get_gobj_visual(event_occured.turn_maker).ready(), 'Code error'

        visualisations.set_visual_state(
            event_occured.turn_maker,
            visual_states.BouncingMotion(
                dxy,
                time_to_move=self._timings.time_to_move,
                amplitude=3,
                fps=self._timings.fps
            )
        )

        if isinstance(event_occured, event.PlayerMoveEvent):
            new_camera_state = camera_states.CameraMovingWithDelay(new_xy,
                                                                   time_to_move=self._timings.time_to_move,
                                                                   delay_ratio=0.0,
                                                                   fps=self._timings.fps
                                                                   )
            current_camera = visualisations.get_camera()
            current_camera.set_new_state(new_camera_state)

    def gobj_attack_callback(self,
                             event_occured: event.GobjMeleeAttackEvent,
                             visualisations: VisualisationsContainer) -> None:
        dxy = (event_occured.attack_to_ij - event_occured.attack_from_ij).dot(self._tile_size_pixels)
        visualisations.set_visual_state(
            event_occured.turn_maker,
            visual_states.MeleeAttacking(dxy,
                                         time_to_attack=self._timings.time_to_attack,
                                         max_amplitude_ratio=0.05,
                                         fps=self._timings.fps)
        )
        if isinstance(event_occured, event.PlayerMeleeAttackEvent):
            current_camera = visualisations.get_camera()
            current_camera.set_new_state(camera_states.CameraShaking(
                decay_time=self._timings.time_to_attack,
                delay=self._timings.time_to_attack / 2,
                amplitude=5,
                fps=self._timings.fps)
            )
            # TODO: Sound mixer!
            axe_sound.play()

    def apply_event(self, event_occured: event.Event, visualisations: VisualisationsContainer):
        if isinstance(event_occured, event.GobjMoveEvent):
            self.gobj_move_callback(event_occured, visualisations)
        elif isinstance(event_occured, event.GobjMeleeAttackEvent):
            self.gobj_attack_callback(event_occured, visualisations)
        elif isinstance(event_occured, event.GobjWaitEvent):
            self.gobj_wait_callback(event_occured, visualisations)
