from event import event


def gobj_wait_callback(event_occured: event.GobjWaitEvent, game_model) -> None:
    actors = game_model.get_actors()
    assert event_occured.turn_maker == actors.current_gobj(), 'Only current actor can move!'
    actors.make_turn(event_occured.turn_time)


def gobj_move_callback(event_occured: event.GobjMoveEvent, game_model) -> None:
    actors = game_model.get_actors()
    assert event_occured.turn_maker == actors.current_gobj(), 'Only current actor can move!'
    actors.make_turn(event_occured.turn_time)
    event_occured.turn_maker.set_pos(event_occured.to_ij)


def gobj_attack_callback(event_occured: event.GobjMeleeAttackEvent, game_model) -> None:
    # TODO: DO SOMETHING!!!
    actors = game_model.get_actors()
    assert event_occured.turn_maker == actors.current_gobj(), 'Only current actor can move!'
    actors.make_turn(event_occured.turn_time)


EVENT_TYPE_TO_CALLBACK = {
    event.GobjWaitEvent: gobj_wait_callback,
    event.GobjMoveEvent: gobj_move_callback,
    event.GobjMeleeAttackEvent: gobj_attack_callback
}


def apply_event(event_occured: event.Event, game_model) -> None:
    EVENT_TYPE_TO_CALLBACK[type(event_occured)](event_occured, game_model)
