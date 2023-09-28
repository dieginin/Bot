from dataclasses import dataclass
from enum import Enum
from typing import Any

from helpers import from_int, from_list, from_str


@dataclass
class Icon:
    id: int

    @staticmethod
    def from_dict(obj: Any) -> "Icon":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        return Icon(id)


class Role(Enum):
    Miembro = "member"
    Presidente = "president"
    Veterano = "senior"
    Vice_Presidente = "vicePresident"


@dataclass
class Member:
    tag: str
    name: str
    name_color: str
    role: Role
    trophies: int
    icon: Icon

    @staticmethod
    def from_dict(obj: Any) -> "Member":
        assert isinstance(obj, dict)
        tag = from_str(obj.get("tag"))
        name = from_str(obj.get("name"))
        name_color = from_str(obj.get("nameColor"))
        role = Role(obj.get("role"))
        trophies = from_int(obj.get("trophies"))
        icon = Icon.from_dict(obj.get("icon"))
        return Member(tag, name, name_color, role, trophies, icon)


def from_member(x: Any) -> Member:
    assert isinstance(x, Member)
    return x


@dataclass
class Club:
    tag: str
    name: str
    description: str
    type: str
    badge_id: int
    required_trophies: int
    trophies: int
    members: list[Member]

    @property
    def member_count(self):
        return len(self.members)

    @property
    def president(self):
        return next(
            (member for member in self.members if member.role == Role.Presidente)
        )

    @property
    def vice_presidents(self):
        return [
            member for member in self.members if member.role == Role.Vice_Presidente
        ]

    @property
    def veterans(self):
        return [member for member in self.members if member.role == Role.Veterano]

    @staticmethod
    def from_dict(obj: Any) -> "Club":
        assert isinstance(obj, dict)
        tag = from_str(obj.get("tag"))
        name = from_str(obj.get("name"))
        description = from_str(obj.get("description"))
        type = from_str(obj.get("type"))
        badge_id = from_int(obj.get("badgeId"))
        required_trophies = from_int(obj.get("requiredTrophies"))
        trophies = from_int(obj.get("trophies"))
        members = from_list(Member.from_dict, obj.get("members"))
        return Club(
            tag,
            name,
            description,
            type,
            badge_id,
            required_trophies,
            trophies,
            members,
        )
