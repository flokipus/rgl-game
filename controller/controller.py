from view.user_moves import PlayerCommand
from model import command
from utils import utils


USER_MOVES_TO_COMMAND = {
    PlayerCommand.MOVE_UP: command.MoveGobjCommand(utils.Vec2i(0, 1)),
    PlayerCommand.MOVE_DOWN: command.MoveGobjCommand(utils.Vec2i(0, -1)),
    PlayerCommand.MOVE_LEFT: command.MoveGobjCommand(utils.Vec2i(-1, 0)),
    PlayerCommand.MOVE_RIGHT: command.MoveGobjCommand(utils.Vec2i(1, 0)),
    PlayerCommand.MOVE_WAIT: command.GobjWaitCommand()
}
