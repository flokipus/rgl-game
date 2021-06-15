from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from ..basegobj import GameObject
from common.utils import utils


class IItem(ABC, GameObject):
    @abstractmethod
    def weight(self) -> int:
        pass


@dataclass
class RequirementCheckAnswer:
    result: bool
    message_reason: str


class IEquipment(IItem, ABC):
    """You can put this on your character"""
    @abstractmethod
    def check_requirements_to_wield(self, target_character) -> RequirementCheckAnswer:
        """But sometimes you can't"""
        pass


class IWeapon(IEquipment):
    @abstractmethod
    def base_damage(self) -> int:
        """Base damage: a positive value"""

    @abstractmethod
    def chance_to_hit(self) -> int:
        """Additional chance to hit target. From 0 to 100.
        Characters attributes are taken into account"""


class BareFist(IWeapon):
    def __init__(self):
        GameObject.__init__(self, pos=utils.Vec2i(0, 0), name='fist', sprite=None)

    def weight(self) -> int:
        return 0

    def base_damage(self) -> int:
        return 1

    def check_requirements_to_wield(self, target_character) -> RequirementCheckAnswer:
        return RequirementCheckAnswer(result=True, message_reason='')

    def chance_to_hit(self) -> int:
        return 50


class OneHandAxe(IWeapon):
    def __init__(self):
        GameObject.__init__(self, pos=utils.Vec2i(0, 0), name='one hand axe', sprite=None)

    def weight(self) -> int:
        return 2000

    def check_requirements_to_wield(self, target_character) -> RequirementCheckAnswer:
        result = target_character.base_attributes.strength >= 8
        if result:
            message_reason = ''
        else:
            message_reason = 'Not enough strength'
        return RequirementCheckAnswer(result, message_reason)

    def base_damage(self) -> int:
        return 10

    def chance_to_hit(self) -> int:
        return 50


class IArmor(IEquipment):
    @abstractmethod
    def chance_to_avoid_hit(self) -> int:
        """From 0 to 100. Characters attributes are taken into account"""

    @abstractmethod
    def damage_reduction(self, target_character) -> int:
        pass


class BareArmor(IArmor):
    def __init__(self):
        GameObject.__init__(self, pos=utils.Vec2i(0, 0), name='bare body', sprite=None)

    def weight(self) -> int:
        return 0

    def check_requirements_to_wield(self, target_character) -> RequirementCheckAnswer:
        return RequirementCheckAnswer(result=True, message_reason='')

    def chance_to_avoid_hit(self) -> int:
        return 0

    def damage_reduction(self, target_character) -> int:
        return 0


class HeadArmor(BareArmor):
    pass


class TorsoArmor(BareArmor):
    pass


class ShieldArmor(BareArmor):
    pass


class LegsArmor(BareArmor):
    pass
