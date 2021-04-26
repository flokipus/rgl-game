from common.event import event
from . import visualisaton_state


def gobj_wait_callback(event_occured: event.GobjWaitEvent, game_view) -> None:
    pass


def gobj_move_callback(event_occured: event.GobjMoveEvent, game_view) -> None:
    # print('view event: {}'.format(event_occured.who_am_i()))

    dxy = (event_occured.to_ij - event_occured.from_ij).dot(game_view.tile_size_pixels)
    dxy[1] = -dxy[1]  # hack. In pygame y-dimension oriented from top to bot
    game_view.set_new_animation_state(
        event_occured.turn_maker,
        visualisaton_state.Moving(
            dxy,
            time_to_move=game_view.time_to_move,
            fps=game_view.fps
        )
    )
    game_view.add_gobj_to_wait_animation(event_occured.turn_maker)


def gobj_attack_callback(event_occured: event.GobjMeleeAttackEvent, game_view) -> None:
    dxy = (event_occured.attack_to_ij - event_occured.attack_from_ij).dot(game_view.tile_size_pixels)
    dxy[1] = -dxy[1]
    game_view.set_new_animation_state(
        event_occured.turn_maker,
        visualisaton_state.MeleeAttacking(dxy,
                                          time_to_attack=game_view.time_to_move,
                                          max_amplitude_ratio=0.1,
                                          fps=game_view.fps)
    )
    game_view.add_gobj_to_wait_animation(event_occured.turn_maker)


EVENT_TYPE_TO_CALLBACK = {
    event.GobjWaitEvent: gobj_wait_callback,
    event.GobjMoveEvent: gobj_move_callback,
    event.GobjMeleeAttackEvent: gobj_attack_callback
}


def apply_event(event_occured: event.Event, game_view) -> None:
    event_type = type(event_occured)
    callback = EVENT_TYPE_TO_CALLBACK[event_type]
    callback(event_occured, game_view)
