from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, List, Optional, Type, TypeVar

from models.Brawler import Brawler

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


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


class Mode(Enum):
    Aniquilación = "wipeout"
    Asedio = "siege"
    Atraco = "heist"
    Atrapagemas = "gemGrab"
    Balón_Brawl = "brawlBall"
    Basketbrawl = "basketBrawl"
    Bowdrop = "botDrop"
    Caza_Estelar = "bounty"
    Desconocido = "unknown"
    Duelo = "duels"
    Gran_Juego = "bigGame"
    Hold_The_Throphy = "holdTheTrophy"
    Hunters = "hunters"
    Ladrones_Trofeos = "trophyThieves"
    Lone_Star = "loneStar"
    Noqueo = "knockout"
    Payload = "payload"
    Pelea_de_Jefe = "bossFight"
    Present_Plunder = "presentPlunder"
    Robo_Rumble = "roboRumble"
    Snowtel_Thieves = "snowtelThieves"
    Super_City_Rampage = "superCityRampage"
    Supervivencia_Duo = "duoShowdown"
    Supervivencia_Solo = "soloShowdown"
    Takedown = "takedown"
    Último_Vido = "lastStand"
    Volleybrawl = "volleyBrawl"
    Zona_Restringida = "hotZone"


class Result(Enum):
    EMPATE = 'draw'
    GANADA = "victory"
    PERDIDA = "defeat"


@dataclass
class StarPlayer:
    tag: str
    name: str
    brawler: Brawler

    @staticmethod
    def from_dict(obj: Any) -> 'StarPlayer':
        assert isinstance(obj, dict)
        tag = from_str(obj.get("tag"))
        name = from_str(obj.get("name"))
        brawler = Brawler.from_dict(obj.get("brawler"))
        return StarPlayer(tag, name, brawler)


class TypeEnum(Enum):
    Desafio = "challenge"
    Estelar_Solo = "soloRanked"
    Estelar_Team = "teamRanked"
    Normal = "ranked"


@dataclass
class Battle:
    mode: Mode
    type: TypeEnum
    teams: List[List[StarPlayer]]
    rank: Optional[int] = None
    result: Optional[Result] = None
    duration: Optional[int] = None
    trophy_change: Optional[int] = None
    star_player: Optional[StarPlayer] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Battle':
        assert isinstance(obj, dict)
        mode = Mode(obj.get("mode"))
        type = TypeEnum(obj.get("type"))
        teams = from_list(lambda x: from_list(StarPlayer.from_dict, x), obj.get("teams"))
        rank = from_union([from_int, from_none], obj.get("rank"))
        result = from_union([Result, from_none], obj.get("result"))
        duration = from_union([from_int, from_none], obj.get("duration"))
        trophy_change = from_union([from_int, from_none], obj.get("trophyChange"))
        star_player = from_union([StarPlayer.from_dict, from_none], obj.get("starPlayer"))
        return Battle(mode, type, teams, rank, result, duration, trophy_change, star_player)


@dataclass
class Event:
    id: int
    mode: Mode
    map: str

    @staticmethod
    def from_dict(obj: Any) -> 'Event':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        mode = Mode(obj.get("mode"))
        map = from_str(obj.get("map"))
        return Event(id, mode, map)


@dataclass
class BattleLog:
    battle_time: str
    event: Event
    battle: Battle

    @staticmethod
    def from_dict(obj: Any) -> 'BattleLog':
        assert isinstance(obj, dict)
        battle_time = from_str(obj.get("battleTime"))
        event = Event.from_dict(obj.get("event"))
        battle = Battle.from_dict(obj.get("battle"))
        return BattleLog(battle_time, event, battle)
