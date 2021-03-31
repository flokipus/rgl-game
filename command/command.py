from utils.utils import Vec2i


class Command:
    pass


class MoveCommand(Command):
    def __init__(self, dij: Vec2i):
        self.dij = dij
