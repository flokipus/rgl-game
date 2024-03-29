# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import List, Tuple
import pygame

from common.utils import utils
from gamelogic.view.visualisation.visualisation import Visualisation
from gamelogic.view.visualisation.visual_container import VisualisationsContainer

from _DEBUG_perf import PERFOMANCE_DATA


class Layers:
    def __init__(self, num_layers: int):
        self._layers = [[] for i in range(num_layers)]

    def add_visualisation(self, visualisation):
        layer_num = visualisation.get_layer()
        self._layers[layer_num].append(visualisation)

    def get_layer(self, i: int) -> List[Visualisation]:
        return self._layers[i]

    def num_layers(self) -> int:
        return len(self._layers)

    def clear(self) -> None:
        for layer in self._layers:
            layer.clear()


class Display:
    def __init__(self, screen_size: Tuple[int, int], layers_num: int):
        self._screen_size = utils.Vec2i(*screen_size)
        self._monitor_center: utils.Vec2i = self._screen_size // 2
        self._display: pygame.Surface = pygame.display.set_mode(screen_size)
        self._layers: Layers = Layers(layers_num)

    def redraw(self, visuals: VisualisationsContainer) -> None:
        PERFOMANCE_DATA.end_visuals()
        PERFOMANCE_DATA.start_layer_build()
        self._fill_layers(visuals)
        PERFOMANCE_DATA.end_layer_build()
        self._display.fill((0, 0, 0))
        camera_center = visuals.get_camera().get_center()
        PERFOMANCE_DATA.start_draw()
        self._draw_layers(camera_center)
        PERFOMANCE_DATA.end_draw()
        PERFOMANCE_DATA.display_start()
        pygame.display.update()
        PERFOMANCE_DATA.display_end()

    def _fill_layers(self, visuals: VisualisationsContainer) -> None:
        self._layers.clear()
        for visual in visuals.get_all_visuals():
            self._layers.add_visualisation(visual)

    def _draw_layers(self, center: utils.Vec2i) -> None:
        PERFOMANCE_DATA.blit_last_elapsed = 0
        screen_size = self._screen_size  # optimization is important
        monitor_center = self._monitor_center
        center_tuple = center.to_tuple()
        p_xy = [0, 0]
        for i in range(self._layers.num_layers()):
            layer = self._layers.get_layer(i)
            for visual in layer:
                sprite = visual.get_sprite()

                p_xy[0], p_xy[1] = visual.get_corner_xy().to_tuple()
                p_xy[0] -= center_tuple[0]
                p_xy[1] -= center_tuple[1]
                p_xy[1] = screen_size[1] - p_xy[1] - monitor_center[1]
                p_xy[0] += monitor_center[0]

                t_begin = pygame.time.get_ticks()
                self._display.blit(sprite, p_xy)
                t_end = pygame.time.get_ticks()
                PERFOMANCE_DATA.blit_last_elapsed += (t_end - t_begin)
        PERFOMANCE_DATA.blit_total += PERFOMANCE_DATA.blit_last_elapsed

    def descartes_to_monitor(self, xy_desc: utils.Vec2i) -> utils.Vec2i:
        new_xy = xy_desc.copy()
        new_xy[1] = self._screen_size[1] - new_xy[1] - self._monitor_center[1]
        new_xy[0] += self._monitor_center[0]
        return new_xy
