from typing import List
from abc import ABC, abstractmethod
from random import randint

from common.gameobj.characters.base_character import Character
from common.event import event
from common.utils.utils import Vec2i


class Action(ABC):
    @abstractmethod
    def apply(self, model) -> List[event.Event]: ...


class WaitAction(Action):
    def __init__(self, who: Character):
        self.who = who

    def apply(self, model) -> List[event.Event]:
        events_list = []
        actors = model.get_actors()
        assert self.who == actors.current_actor(), 'Only current actor can move!'
        # TODO: THERE MUST BE NO MAGIC CONSTANTS! FFS
        wait_cost = 80
        actors.make_turn(wait_cost)
        events_list.append(event.CharacterWaitTurn(self.who))
        return events_list


class MeleeAttackAction(Action):
    def __init__(self, who: Character, whom: Character):
        self.who = who
        self.whom = whom

    def apply(self, model) -> List[event.Event]:
        events_list = []
        actors = model.get_actors()
        assert self.who == actors.current_actor(), 'Only current actor can move!'
        weapon = self.who.wearing_items.right_hand.item

        accuracy_mult = self.who.base_attributes.dexterity / 10
        accuracy = max(1, int(weapon.chance_to_hit() * accuracy_mult))

        dodge_mult = self.whom.base_attributes.dexterity / 10
        armor = self.whom.wearing_items.torso.item
        dodge = max(1, int(armor.chance_to_avoid_hit() * dodge_mult))

        min_dice = min(dodge - accuracy, 95)
        dice = randint(0, 100)

        print(f'Attacker: {self.who.get_name()}; Attack accuracy: {accuracy}; dodge: {dodge}; to_hit: {dodge - accuracy}; dice: {dice}')

        does_hit = False
        is_critical = False
        damage = 0
        if dice >= min_dice or dice >= 95:
            does_hit = True
            if dice >= 95:
                is_critical = True
            damage_mult = self.who.base_attributes.strength / 10
            damage = max(1, int(weapon.base_damage() * damage_mult - armor.damage_reduction()))

        accured_event = event.CharacterMadeMeleeAttack(who=self.who, whom=self.whom,
                                                       target_tile_ij=self.whom.get_pos(),
                                                       from_tile_ij=self.who.get_pos(),
                                                       damage=damage, does_hit_target=does_hit,
                                                       is_critical=is_critical)
        events_list.append(accured_event)
        self.whom.hp -= damage
        if self.whom.hp <= 0:
            events_list.append(event.CharacterDied(self.whom))
            model.get_actors().remove_actor(self.whom)
        wait_time = 100
        actors.make_turn(wait_time)
        return events_list


class MoveAction(Action):
    def __init__(self, who: Character, dij: Vec2i):
        self.who = who
        self.dij = dij

    def apply(self, model) -> List[event.Event]:
        new_pos = self.who.get_pos() + self.dij
        event_list = [
            event.CharacterMadeMove(self.who,
                                    old_tile_ij=self.who.get_pos(),
                                    new_tile_ij=new_pos)
        ]
        self.who.set_pos(new_pos)
        model.get_actors().make_turn(turn_time=80)
        return event_list


class PlayerUnableToMadeWalk(Action):
    def __init__(self, from_tile_ij: Vec2i, to_tile_ij: Vec2i):
        self.from_tile_ij = from_tile_ij
        self.to_tile_ij = to_tile_ij

    def apply(self, model) -> List[event.Event]:
        event_list = [
            event.PlayerUnableToMadeWalk(from_tile_ij=self.from_tile_ij,
                                         target_tile_ij=self.to_tile_ij)
        ]
        return event_list
