# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from common.gameobj.characters.base_character import Character
from common.utils.utils import Vec2i
from gamelogic.model import actions


class ActorIntention(ABC):
    @abstractmethod
    def interpret(self, model, character: Character) -> actions.Action:
        pass


class ActorMoveIntention(ActorIntention):
    def __init__(self, delta_ij: Vec2i):
        self._delta_ij = delta_ij

    def interpret(self, model, character: Character) -> actions.Action:
        current_tile_ij = character.get_pos()
        new_tile_ij = current_tile_ij + self._delta_ij
        target_tile = model.get_tile(new_tile_ij)
        if target_tile is None:
            if character == model.player_character:
                return actions.PlayerUnableToMadeWalk(from_tile_ij=current_tile_ij,
                                                      to_tile_ij=new_tile_ij)
            else:
                return actions.WaitAction(character)
        else:
            actors = model.get_actors()
            for actor in actors.get_all_actors_view():
                if actor.get_pos() == new_tile_ij:
                    return actions.MeleeAttackAction(character, actor)
        return actions.MoveAction(character, dij=(new_tile_ij - current_tile_ij))


class ActorWaitIntention(ActorIntention):
    def interpret(self, model, character: Character) -> actions.Action:
        return actions.WaitAction(character)
