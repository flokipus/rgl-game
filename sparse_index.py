import settings.screen

DIAM = max(settings.screen.CELL_WIDTH, settings.screen.CELL_HEIGHT)
COUNT_HOR = settings.screen.MAP_WIDTH // DIAM + 1
COUNT_VERT = settings.screen.MAP_HEIGHT // DIAM + 1


class SparseIndexing:
    def __init__(self, count_hor=COUNT_HOR, count_vert=COUNT_VERT, diam=DIAM):
        self._count_hor = count_hor
        self._count_vert = count_vert
        self._diam = diam
        self._obj_table = [set() for i in range(count_hor * count_vert)]

    def get_objs_in_xy(self, xy):
        i, j = self._xy_to_ij(xy)
        return self._obj_table[j * self._count_vert + i]

    def _xy_to_ij(self, xy):
        i = xy[0] // self._diam
        j = xy[1] // self._diam
        return i, j

    def add_obj(self, obj):
        i, j = self._xy_to_ij(obj.logic.xy)
        self._obj_table[j * self._count_vert + i].add(obj.obj_id)

    def remove_obj(self, obj_id, xy_hint=None):
        if xy_hint is not None:
            i, j = self._xy_to_ij(xy_hint)
            if obj_id in self._obj_table[j * self._count_vert + i]:
                self._obj_table[j * self._count_vert + i].remove(obj_id)
        else:
            for i in range(self._count_hor):
                for j in range(self._count_vert):
                    if obj_id in self._obj_table[j * self._count_vert + i]:
                        self._obj_table[j * self._count_vert + i].remove()
                        return
