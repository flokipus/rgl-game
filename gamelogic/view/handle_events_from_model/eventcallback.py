# -*- coding: utf-8 -*-

from common.event import event
from common.utils import utils
from gamelogic.view.camera import camera_states
from gamelogic.view.visualisation import visualisation_states as visual_states
from gamelogic.view.visualisation.visual_container import VisualisationsContainer
from gamelogic.view.sound import predef_sound


class GobjEventsCallbacks:
    def __init__(self, timings, tile_size_pixels: utils.Vec2i):
        self._timings = timings
        self._tile_size_pixels = tile_size_pixels

    def character_wait_callback(self,
                                event_occured: event.CharacterWaitTurn,
                                visualisations: VisualisationsContainer) -> None:
        pass

    def character_move_callback(self,
                                event_occured: event.CharacterMadeMove,
                                visualisations: VisualisationsContainer) -> None:
        new_xy = visualisations.cell_ij_to_pixel(event_occured.new_tile_ij)
        dxy = visualisations.cell_ij_to_pixel(event_occured.new_tile_ij - event_occured.old_tile_ij)
        assert visualisations.get_gobj_visual(event_occured.who).ready(), 'Code error'

        visualisations.set_visual_state(
            event_occured.who,
            visual_states.BouncingMotion(
                dxy,
                time_to_move=self._timings.time_to_move,
                amplitude=3,
                fps=self._timings.fps
            )
        )
        if event_occured.who == visualisations.player_character:
            new_camera_state = camera_states.CameraMovingWithDelay(new_xy,
                                                                   time_to_move=self._timings.time_to_move,
                                                                   delay_ratio=0.0,
                                                                   fps=self._timings.fps
                                                                   )
            current_camera = visualisations.get_camera()
            current_camera.set_new_state(new_camera_state)

    def character_attack_callback(self,
                             event_occured: event.CharacterMadeMeleeAttack,
                             visualisations: VisualisationsContainer) -> None:
        dxy = (event_occured.target_tile_ij - event_occured.from_tile_ij).dot(self._tile_size_pixels)
        visualisations.set_visual_state(
            event_occured.who,
            visual_states.MeleeAttacking(dxy,
                                         time_to_attack=self._timings.time_to_attack,
                                         max_amplitude_ratio=0.05,
                                         fps=self._timings.fps)
        )
        print(f'Attack event: {event_occured.who.get_name()} attacks {event_occured.whom.get_name()}; '
              f'Damage made: {event_occured.damage}; Hp after: {event_occured.whom.hp}')
        if event_occured.who == visualisations.player_character:
            predef_sound.axe_sound.play()
            if event_occured.does_hit_target:
                predef_sound.gore_sound.play()
                current_camera = visualisations.get_camera()
                amplitude = 5  # base amplitude
                if event_occured.is_critical:
                    amplitude = 10
                current_camera.set_new_state(camera_states.CameraShaking(
                    decay_time=self._timings.time_to_attack,
                    delay=self._timings.time_to_attack / 2,
                    amplitude=amplitude,
                    fps=self._timings.fps)
                )
            # TODO: Sound mixer!

    def player_unable_move(self, event_occured: event.PlayerUnableToMadeWalk, visualisations: VisualisationsContainer):
        dxy = (event_occured.target_tile_ij - event_occured.from_tile_ij).dot(self._tile_size_pixels)
        visualisations.set_visual_state(
            visualisations.player_character,
            visual_states.MeleeAttacking(dxy,
                                         time_to_attack=self._timings.time_to_attack,
                                         max_amplitude_ratio=0.05,
                                         fps=self._timings.fps)
        )

    def character_died(self, event_occured: event.CharacterDied, visualisations: VisualisationsContainer):
        visualisations.remove_gobj_visual(event_occured.who)

    def apply_event(self, event_occured: event.Event, visualisations: VisualisationsContainer):
        if isinstance(event_occured, event.CharacterDied):
            self.character_died(event_occured, visualisations)
        elif isinstance(event_occured, event.CharacterMadeMeleeAttack):
            self.character_attack_callback(event_occured, visualisations)
        elif isinstance(event_occured, event.CharacterMadeMove):
            self.character_move_callback(event_occured, visualisations)
        elif isinstance(event_occured, event.CharacterWaitTurn):
            self.character_wait_callback(event_occured, visualisations)
        elif isinstance(event_occured, event.PlayerUnableToMadeWalk):
            self.player_unable_move(event_occured, visualisations)
