import pygame


class PerfomanceData:
    def __init__(self, fps):
        pygame.init()
        self.global_time_begin = 0
        self.global_time_end = 0

        self.fps = fps

        self.frame_counter = 0

        self.model_time_stamp_begin = 0
        self.model_time_stamp_end = 0
        self.model_total = 0

        self.visuals_time_stamp_begin = 0
        self.visuals_time_stamp_end = 0
        self.visuals_total = 0

        self.layer_build_stamp_begin = 0
        self.layer_build_stamp_end = 0
        self.layer_build_total = 0

        self.draw_time_stamp_begin = 0
        self.draw_time_stamp_end = 0
        self.draw_total = 0

    def global_start(self):
        self.global_time_begin = pygame.time.get_ticks()

    def global_end(self):
        self.global_time_end = pygame.time.get_ticks()

    def new_frame(self):
        self.frame_counter += 1

    def start_layer_build(self):
        self.layer_build_stamp_begin = pygame.time.get_ticks()

    def end_layer_build(self):
        self.layer_build_stamp_end = pygame.time.get_ticks()
        elapsed = self.layer_build_stamp_end - self.layer_build_stamp_begin
        if elapsed >= 0:
            self.layer_build_total += elapsed
        else:
            raise AssertionError('Code error')

    def start_model(self):
        self.model_time_stamp_begin = pygame.time.get_ticks()

    def end_model(self):
        self.model_time_stamp_end = pygame.time.get_ticks()
        elapsed = self.model_time_stamp_end - self.model_time_stamp_begin
        if elapsed >= 0:
            self.model_total += elapsed
        else:
            raise AssertionError('Code error')

    def start_visuals(self):
        self.visuals_time_stamp_begin = pygame.time.get_ticks()

    def end_visuals(self):
        self.visuals_time_stamp_end = pygame.time.get_ticks()
        elapsed = self.visuals_time_stamp_end - self.visuals_time_stamp_begin
        if elapsed >= 0:
            self.visuals_total += elapsed
        else:
            raise AssertionError('Code error')

    def start_draw(self):
        self.draw_time_stamp_begin = pygame.time.get_ticks()

    def end_draw(self):
        self.draw_time_stamp_end = pygame.time.get_ticks()
        elapsed = self.draw_time_stamp_end - self.draw_time_stamp_begin
        if elapsed >= 0:
            self.draw_total += elapsed
        else:
            raise AssertionError('Code error')

    def print_finish_info(self):
        total_elapsed = self.global_time_end - self.global_time_begin
        total_elapsed_sec = total_elapsed / 1000
        expected_frames = total_elapsed_sec * self.fps
        print('Time elapsed={}s; frames={}; expected frames={}'.format(
            total_elapsed_sec,
            self.frame_counter,
            expected_frames)
        )
        print('Total time for model: {}ms; total time for view: {}ms; total time for drawing: {}ms'.format(
            self.model_total,
            self.visuals_total,
            self.draw_total)
        )
        print('Average time per frame for model: {}ms; for view: {}ms;'
              ' for layer building: {}ms; for drawing: {}ms'.format(
            self.model_total / self.frame_counter,
            self.visuals_total / self.frame_counter,
            self.layer_build_total / self.frame_counter,
            self.draw_total / self.frame_counter)
        )


PERFOMANCE_DATA = PerfomanceData(fps=30)
