from __future__ import annotations
import pygame
from typing import Union, overload

from gameobj.states import BaseState
from gameobj.basegobj import GameObject
from command.command_channel import Command, CommandChannel, UserCommandChannel


class Actor:
    """Actor is just a 2-tuple: game object and a channel associated with this actor: from this channel
    one could receive commands for the actor.
    """
    def __init__(self, gobj: GameObject, command_channel: CommandChannel) -> None:
        self._gobj = gobj
        self._command_channel = command_channel
        self._last_command = None

    def __hash__(self):
        return self._gobj.__hash__()

    def __eq__(self, other: Actor) -> bool:
        return self._gobj.id == other._gobj.id

    def request_command(self) -> Union[None, Command]:
        """Equivalent to actor.get_command_channel().request_command()"""
        return self._command_channel.request_command()

    def set_command_channel(self, command_channel) -> CommandChannel:
        prev_ch = self._command_channel
        self._command_channel = command_channel
        return prev_ch

    def get_last_command(self) -> Command:
        return self._last_command

    def get_command_channel(self) -> CommandChannel:
        return self._command_channel

    def get_gobj(self) -> GameObject:
        return self._gobj

    def controlled_by_player(self) -> bool:
        return isinstance(self._command_channel, UserCommandChannel)
