from event import event
from . import visualisaton_state


def gobj_wait_callback(event_occured: event.GobjWaitEvent, game_view) -> None:
    pass


def gobj_move_callback(event_occured: event.GobjMoveEvent, game_view) -> None:
    dxy = (event_occured.to_ij - event_occured.from_ij).dot(game_view.tile_size_pixels)
    dxy[1] = -dxy[1]  # hack. In pygame y-dimension oriented from top to bot
    game_view.set_new_animation_state(event_occured.turn_maker, visualisaton_state.Moving(dxy, time_to_move=0.1))
    game_view.add_gobj_to_wait(event_occured.turn_maker, lambda x: x.ready())


EVENT_TYPE_TO_CALLBACK = {
    event.GobjWaitEvent: gobj_wait_callback,
    event.GobjMoveEvent: gobj_move_callback,
    event.GobjMeleeAttackEvent: gobj_wait_callback  # TODO: This should be attack!
}


def apply_event(event_occured: event.Event, game_view) -> None:
    event_type = type(event_occured)
    callback = EVENT_TYPE_TO_CALLBACK[event_type]
    callback(event_occured, game_view)
