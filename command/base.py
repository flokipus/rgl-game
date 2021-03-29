from utils import Vec2i


class Command:
    pass


class MoveCommand(Command):
    def __init__(self, ij_from: Vec2i, ij_to: Vec2i):
        self.ij_from = ij_from
        self.ij_to = ij_to
