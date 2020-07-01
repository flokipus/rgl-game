import pygame
from settings import colors
from settings import screen
import gobject


def true_for_everything(*largs):
    return True


class Draftsman:
    def __init__(self, draw_if=true_for_everything):
        self._draw_if = draw_if

    def draw_obj(self, where_to_draw: pygame.Surface, obj: gobject.GameObject, camera_xy: tuple):
        if self._draw_if(obj, where_to_draw) and obj.sprite is not None:
            x, y = obj.xy
            cx, cy = camera_xy
            nx, ny = x - cx, y - cy
            where_to_draw.blit(obj.sprite, (nx * screen.CELL_WIDTH, ny * screen.CELL_HEIGHT))

    def set_draw_if(self, draw_if):
        self._draw_if = draw_if

    @property
    def get_draw_if(self):
        return self._draw_if


class Graphics:
    def __init__(self, where_to_draw, num_of_layers, draftsman: Draftsman):
        self._num_of_layers = num_of_layers
        self._layers_static = [[] for i in range(num_of_layers)]
        self._layers_dynamic = [set() for i in range(num_of_layers)]
        self._screen = where_to_draw
        self._draftsman = draftsman

    def draw(self, obj, camera_xy=(0, 0)):
        self._draftsman.draw_obj(self._screen, obj, camera_xy)

    def draw_all(self):
        self._screen.fill(colors.DEFAULT_BACKGROUND_COLOR)
        for i in range(self._num_of_layers):
            current_static_layer = self._layers_static[i]
            for obj in current_static_layer:
                self.draw(obj=obj)
            current_dynamic_layer = self._layers_dynamic[i]
            for obj in current_dynamic_layer:
                self.draw(obj=obj)

    def clear(self):
        self._layers_static = [[] for i in range(self._num_of_layers)]
        self._layers_dynamic = [set() for i in range(self._num_of_layers)]

    def add_obj_to_static_layer(self, obj, layer_num):
        self._layers_static[layer_num].append(obj)

    def add_obj_to_dynamic_layer(self, obj, layer_num):
        self._layers_dynamic[layer_num].add(obj)

    @property
    def get_num_of_layers(self):
        return self._num_of_layers

    @property
    def get_static_layers(self):
        return self._layers_static

    @property
    def get_dynamic_layers(self):
        return self._layers_dynamic

    @property
    def get_draftsman(self):
        return self._draftsman
