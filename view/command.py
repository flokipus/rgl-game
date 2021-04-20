from utils.utils import Vec2i


class ViewCommand:
    pass


class ExitCommand(ViewCommand):
    pass


class SaveAndExitCommand(ViewCommand):
    pass


class MoveCommand(ViewCommand):
    def __init__(self, dij: Vec2i):
        self.dij = dij


MOVE_ONE_TILE = {
    'UP': MoveCommand(Vec2i(0, 1)),
    'DOWN': MoveCommand(Vec2i(0, -1)),
    'LEFT': MoveCommand(Vec2i(-1, 0)),
    'RIGHT': MoveCommand(Vec2i(1, 0)),
    'WAIT': MoveCommand(Vec2i(0, 0))
}
