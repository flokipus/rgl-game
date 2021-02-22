from settings import screen, colors
from graphics.cell_sprites import sprite_ascii, predef

import pygame

cells_count_x = 100
cells_count_y = 50
map_size = (cells_count_x * screen.CELL_WIDTH, cells_count_y * screen.CELL_HEIGHT)
walls_xy = [(5 + i, 10) for i in range(16)]
walls_xy.extend([(5, 10 + i) for i in range(11)])
walls_xy.extend([(20, 10 + i) for i in range(11)])
walls_xy.extend([(5 + i, 20) for i in range(10)])
walls_xy.extend([(5 + i, 20) for i in range(11, 16)])
print("cells count. Hor: {}, Vert: {}.".format(cells_count_x, cells_count_y))

pygame.init()
FONT = pygame.font.Font(None, screen.FONT_SIZE)
cell_creator = sprite_ascii.AsciiCellCreator(FONT, screen.CELL_SIZE)


def form_walls_xy():
    walls_xy = [(5 + i, 10) for i in range(16)]
    walls_xy.extend([(5, 10 + i) for i in range(11)])
    walls_xy.extend([(20, 10 + i) for i in range(11)])
    walls_xy.extend([(5 + i, 20) for i in range(10)])
    walls_xy.extend([(5 + i, 20) for i in range(11, 16)])
    for i in range(len(walls_xy)):
        x, y = walls_xy[i]
        walls_xy[i] = (x, y)
    return walls_xy


def create_map_sprite(map_size):
    map_sprite = pygame.Surface(map_size, pygame.SRCALPHA)
    sand_bck = cell_creator.create('', colors.SAND, colors.SAND)
    wall_sprite = predef.wall
    empty_cell_sprite = predef.dot
    walls_xy = form_walls_xy()
    for i in range(cells_count_x):
        for j in range(cells_count_y):
            pos = (i * screen.CELL_WIDTH, j * screen.CELL_HEIGHT)
            map_sprite.blit(sand_bck, pos)
            if pos not in walls_xy:
                map_sprite.blit(empty_cell_sprite, pos)
    for xy in walls_xy:
        x, y = xy
        wall_sprite_xy = (x * screen.CELL_WIDTH, y * screen.CELL_WIDTH)
        map_sprite.blit(wall_sprite, wall_sprite_xy)
    return map_sprite


# def create_main_char(xy):
#     char_sprite = predef.human
#     main_char = gobject.GameObject(xy=xy, graphics=char_sprite, layer=3)
#     return main_char
#
#
# def create_monster_dragon(xy):
#     char_sprite = predef.dragon
#     dragon = gobject.NPC(xy=xy, graphics=char_sprite, layer=3)
#     return dragon
#
#
# def create_obstacles(xys):
#     result = []
#     for xy in xys:
#         result.append(gobject.GameObject(xy, None))
#     return result


map_sprite = create_map_sprite(map_size)
# map_gobj = gobject.GameObject(xy=(0, 0), graphics=map_sprite, layer=0)
# main_char = create_main_char((0, 0))
# dragon = create_monster_dragon((3, 10))
# walls = create_obstacles(form_walls_xy())
