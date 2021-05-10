"""
Проблема: при движении персонаж заикается (дублируется кадр нахождения в клетке).

Здесь находятся вспомогательная информация для поиска бага данной ошибки.
"""


frame_counter = 0
current_frame_xy = (0, 0)
current_frame_r = 0.0
current_frame_event_handler_len = None
current_frame_command_to_model = None
current_frame_state = None


def print_info():

    if current_frame_command_to_model:
        print('\n This frame command occured!')

    print('Current frame: {};\t xy: {};\t r: {};\t e_h_len: {};\t main_hero_state: {}'.format(
        frame_counter,
        current_frame_xy,
        current_frame_r,
        current_frame_event_handler_len,
        current_frame_state)
    )


def zeroing():
    global current_frame_xy
    global current_frame_r
    global current_frame_command_to_model
    global current_frame_state
    global current_frame_event_handler_len
    current_frame_xy = (0, 0)
    current_frame_r = 0.0
    current_frame_command_to_model = None
    current_frame_state = None
    current_frame_event_handler_len = None
