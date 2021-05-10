from common.event import event
from gamelogic.view.visualisation.visualisation_states import derived as visual_states
from gamelogic.view.camera.camera_states import derived as camera_states
from gamelogic.view.sound import axe_sound


class ViewEventCallback:
    def __init__(self, real_time: float, function_to_call, **function_args):
        self.time: float = 0.0
        self.function = function_to_call
        self.function_args = function_args

    def __call__(self):
        self.function(**self.function_args)


def form_callback(event_occured: event.GobjEvent, game_view) -> ViewEventCallback:
    if type(event_occured) == event.GobjWaitEvent:
        pass
    pass


def gobj_wait_callback(event_occured: event.GobjWaitEvent, game_view) -> None:
    pass


def gobj_move_callback(event_occured: event.GobjMoveEvent, game_view) -> None:
    dxy = (event_occured.to_ij - event_occured.from_ij).dot(game_view.tile_size_pixels)
    dxy[1] = -dxy[1]  # hack. In pygame y-dimension oriented from top to bot
    new_xy = game_view._gobjs_to_animations[event_occured.turn_maker].get_pixel_offset() + dxy

    game_view.set_new_animation_state(
        event_occured.turn_maker,
        visual_states.BouncingMotion(
            dxy,
            time_to_move=game_view._time_to_move,
            amplitude=3,
            fps=game_view.fps
        )
    )
    if event_occured.turn_maker == game_view.get_player():
        game_view._camera.set_new_state(camera_states.CameraMovingWithDelay(new_xy,
                                                                            time_to_move=game_view._time_to_move,
                                                                            delay_ratio=0.0,
                                                                            fps=game_view.fps
                                                                            )
                                        )


def gobj_attack_callback(event_occured: event.GobjMeleeAttackEvent, game_view) -> None:
    dxy = (event_occured.attack_to_ij - event_occured.attack_from_ij).dot(game_view.tile_size_pixels)
    dxy[1] = -dxy[1]
    game_view.set_new_animation_state(
        event_occured.turn_maker,
        visual_states.MeleeAttacking(dxy,
                                     time_to_attack=game_view._time_to_attack,
                                     max_amplitude_ratio=0.05,
                                     fps=game_view.fps)
    )
    if event_occured.turn_maker == game_view.get_player():
        game_view._camera.set_new_state(camera_states.CameraShaking(
            decay_time=game_view._time_to_attack,
            delay=game_view._time_to_attack/2,
            amplitude=5,
            fps=game_view.fps)
        )
        axe_sound.play()



EVENT_TYPE_TO_CALLBACK = {
    event.GobjWaitEvent: gobj_wait_callback,
    event.GobjMoveEvent: gobj_move_callback,
    event.GobjMeleeAttackEvent: gobj_attack_callback
}


def apply_event(event_occured: event.Event, game_view) -> None:
    event_type = type(event_occured)
    # print('Occured event type: {};'.format(event_occured.who_am_i()))

    callback = EVENT_TYPE_TO_CALLBACK[event_type]
    callback(event_occured, game_view)
