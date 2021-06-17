from gamelogic.view.settings.user_moves import PlayerCommand
from gamelogic.model import actor_intention
from common.utils import utils


USER_MOVES_TO_COMMAND = {
    PlayerCommand.MOVE_UP: actor_intention.ActorMoveIntention(utils.Vec2i(0, 1)),
    PlayerCommand.MOVE_DOWN: actor_intention.ActorMoveIntention(utils.Vec2i(0, -1)),
    PlayerCommand.MOVE_LEFT: actor_intention.ActorMoveIntention(utils.Vec2i(-1, 0)),
    PlayerCommand.MOVE_RIGHT: actor_intention.ActorMoveIntention(utils.Vec2i(1, 0)),
    PlayerCommand.MOVE_WAIT: actor_intention.ActorWaitIntention()
}
