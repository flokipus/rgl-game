# -*- coding: utf-8 -*-

from typing import Union, overload
import random

from . import actor_intention
from common.utils import utils as utils


class IntentionChannel:
    """
    Base class for command channel
    """
    @overload
    def request_command(self) -> Union[None, actor_intention.ActorIntention]: ...

    @overload
    def put_command(self, new_command: actor_intention.ActorIntention) -> None: ...

    def request_command(self) -> Union[None, actor_intention.ActorIntention]:
        pass

    def put_command(self, new_command: actor_intention.ActorIntention) -> None:
        pass


class UserIntentionChannel(IntentionChannel):
    """TODO: Гибкая настройка key_map -> command, обработка gui + mouse"""
    def __init__(self) -> None:
        self.command_buffer = list()
        self.max_buffer_len = 1

    def request_command(self) -> Union[None, actor_intention.ActorIntention]:
        if len(self.command_buffer) == 0:
            return None
        else:
            curr_command = self.command_buffer[0]
            self.command_buffer.pop(0)
            return curr_command

    def put_command(self, new_command: actor_intention.ActorIntention) -> None:
        if len(self.command_buffer) == self.max_buffer_len:
            self.command_buffer.pop(0)
        self.command_buffer.append(new_command)


class AIRandMoveIC(IntentionChannel):
    __moves = [
        actor_intention.ActorWaitIntention(),  # Stand
        actor_intention.ActorMoveIntention(utils.Vec2i(1, 0)),  # Move right
        actor_intention.ActorMoveIntention(utils.Vec2i(-1, 0)),  # Move left
        actor_intention.ActorMoveIntention(utils.Vec2i(0, 1)),  # Move top
        actor_intention.ActorMoveIntention(utils.Vec2i(0, -1)),  # Move bot
    ]

    def request_command(self) -> Union[None, actor_intention.ActorIntention]:
        move_num = random.randint(0, 4)
        return self.__moves[move_num]
