from settings import colors
import game_objects


def true_for_everything(*largs):
    return True


class IDraftsman:
    def __init__(self, draw_if=true_for_everything):
        self._draw_if = draw_if

    def draw_visual_obj(self, screen, visual_obj: game_objects.IVisualObject):
        if self._draw_if(visual_obj, screen):
            screen.blit(visual_obj.sprite, visual_obj.xy)

    def set_draw_if(self, draw_if):
        self._draw_if = draw_if

    @property
    def get_draw_if(self):
        return self._draw_if


class IVisualisationCore:
    def __init__(self, screen, num_of_layers, draftsman: IDraftsman):
        self._num_of_layers = num_of_layers
        self._layers_static = [[] for i in range(num_of_layers)]
        self._layers_dynamic = [set() for i in range(num_of_layers)]
        self._screen = screen
        self._draftsman = draftsman

    def draw(self, visual_obj):
        self._draftsman.draw_visual_obj(self._screen, visual_obj)

    def draw_all(self):
        self._screen.fill(colors.DEFAULT_BACKGROUND_COLOR)
        for i in range(self._num_of_layers):
            current_static_layer = self._layers_static[i]
            for obj in current_static_layer:
                self.draw(visual_obj=obj)
            current_dynamic_layer = self._layers_dynamic[i]
            for obj in current_dynamic_layer:
                self.draw(visual_obj=obj)

    def clear(self):
        self._layers_static = [[] for i in range(self._num_of_layers)]
        self._layers_dynamic = [set() for i in range(self._num_of_layers)]

    def add_visual_obj_to_static_layer(self, visual_obj, layer_num):
        self._layers_static[layer_num].append(visual_obj)

    def add_visual_obj_to_dynamic_layer(self, visual_obj, layer_num):
        self._layers_dynamic[layer_num].add(visual_obj)

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
