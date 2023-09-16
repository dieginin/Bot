from dataclasses import dataclass
from typing import Any, Callable, List, Optional, TypeVar

from models.Brawler import Brawler

T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


@dataclass
class Club:
    tag: str
    name: str

    @staticmethod
    def from_dict(obj: Any) -> "Club":
        assert isinstance(obj, dict)
        tag = from_str(obj.get("tag"))
        name = from_str(obj.get("name"))
        return Club(tag, name)


@dataclass
class Icon:
    id: int

    @staticmethod
    def from_dict(obj: Any) -> "Icon":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        return Icon(id)


@dataclass
class Player:
    tag: str
    name: str
    name_color: str
    icon: Icon
    trophies: int
    highest_trophies: int
    highest_power_play_points: int
    exp_level: int
    exp_points: int
    is_qualified_from_championship_challenge: bool
    the_3_vs3_victories: int
    solo_victories: int
    duo_victories: int
    best_robo_rumble_time: int
    best_time_as_big_brawler: int
    brawlers: List[Brawler]
    club: Optional[Club] = None

    @staticmethod
    def from_dict(obj: Any) -> "Player":
        assert isinstance(obj, dict)
        tag = from_str(obj.get("tag"))
        name = from_str(obj.get("name"))
        name_color = from_str(obj.get("nameColor"))
        icon = Icon.from_dict(obj.get("icon"))
        trophies = from_int(obj.get("trophies"))
        highest_trophies = from_int(obj.get("highestTrophies"))
        highest_power_play_points = from_int(obj.get("highestPowerPlayPoints"))
        exp_level = from_int(obj.get("expLevel"))
        exp_points = from_int(obj.get("expPoints"))
        is_qualified_from_championship_challenge = from_bool(
            obj.get("isQualifiedFromChampionshipChallenge")
        )
        the_3_vs3_victories = from_int(obj.get("3vs3Victories"))
        solo_victories = from_int(obj.get("soloVictories"))
        duo_victories = from_int(obj.get("duoVictories"))
        best_robo_rumble_time = from_int(obj.get("bestRoboRumbleTime"))
        best_time_as_big_brawler = from_int(obj.get("bestTimeAsBigBrawler"))
        brawlers = from_list(Brawler.from_dict, obj.get("brawlers"))
        club = from_union([Club.from_dict, from_none], obj.get("club"))
        return Player(
            tag,
            name,
            name_color,
            icon,
            trophies,
            highest_trophies,
            highest_power_play_points,
            exp_level,
            exp_points,
            is_qualified_from_championship_challenge,
            the_3_vs3_victories,
            solo_victories,
            duo_victories,
            best_robo_rumble_time,
            best_time_as_big_brawler,
            brawlers,
            club,
        )
