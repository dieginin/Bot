from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, List, TypeVar

T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


@dataclass
class Icon:
    id: int

    @staticmethod
    def from_dict(obj: Any) -> "Icon":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        return Icon(id)


class Role(Enum):
    MEMBER = "Miembro"
    PRESIDENT = "Presidente"
    SENIOR = "Veterano"
    VICE_PRESIDENT = "Vice Presidente"


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


@dataclass
class Club:
    tag: str
    name: str
    description: str
    type: str
    badge_id: int
    required_trophies: int
    trophies: int
    members: List[Member]

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
            tag, name, description, type, badge_id, required_trophies, trophies, members
        )
