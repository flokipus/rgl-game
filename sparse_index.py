

class SparseIndexing:
    def __init__(self, size_hor, size_vert):
        self._count_hor = size_hor
        self._count_vert = size_vert
        self._obj_table = [set() for i in range(size_hor * size_vert)]

    def get_objs_in_xy(self, xy):
        x, y = xy
        return self._obj_table[y * self._count_vert + x]

    def add_obj(self, obj):
        x, y = obj.xy
        self._obj_table[y * self._count_vert + x].add(obj.id)

    def remove_obj(self, obj_id, xy_hint=None):
        if xy_hint is not None:
            x, y = xy_hint
            if obj_id in self._obj_table[y * self._count_vert + x]:
                self._obj_table[y * self._count_vert + x].remove(obj_id)
        else:
            for i in range(self._count_hor):
                for j in range(self._count_vert):
                    if obj_id in self._obj_table[j * self._count_vert + i]:
                        self._obj_table[j * self._count_vert + i].remove()
                        return
