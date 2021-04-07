from __future__ import annotations
import pygame
from typing import Union, overload

from gameobj.states import BaseState
from gameobj.basegobj import GameObject
from command.command_channel import Command, CommandChannel


class Actor:
    """Actor is just a 3-tuple: game object, its state (for example, Standing, Moving, Attacking, Spellcasting,
        etc.) and a channel associated with this actor: from this channel one could receive commands for the
        actor."""
    def __init__(self, gobj: GameObject, state: BaseState,
                 command_channel: CommandChannel) -> None:
        self._gobj = gobj
        self._state = state
        self._command_channel = command_channel
        self._last_command = None

    def __hash__(self):
        return self._gobj.__hash__()

    def __eq__(self, other: Actor) -> bool:
        return self._gobj.id == other._gobj.id

    def update(self) -> None:
        """Update is actually made by _state"""
        return_state = self._state.update(gobj=self._gobj)
        if return_state is not None:
            self.set_new_state(return_state)

    def set_new_state(self, new_state: BaseState) -> None:
        self._state.exit(gobj=self._gobj, next_state=new_state)
        old_state = self._state
        self._state = new_state
        self._state.enter(gobj=self._gobj, old_state=old_state)

    def handle_command(self, command: Command) -> None:
        self._last_command = command
        return_state = self._state.handle_command(gobj=self._gobj, command=self._last_command)
        if return_state is not None:
            self.set_new_state(return_state)

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

    def get_state(self) -> BaseState:
        return self._state

    def get_gobj(self) -> GameObject:
        return self._gobj

    def ready_to_move(self) -> bool:
        return self._state.ready()
