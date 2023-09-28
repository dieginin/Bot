from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from helpers import from_int, from_list, from_none, from_str, from_union
from models.Brawler import Brawler


@dataclass
class StarPlayer:
    tag: str
    name: str
    brawler: Brawler

    @staticmethod
    def from_dict(obj: Any) -> "StarPlayer":
        assert isinstance(obj, dict)
        tag = from_str(obj.get("tag"))
        name = from_str(obj.get("name"))
        brawler = Brawler.from_dict(obj.get("brawler"))
        return StarPlayer(tag, name, brawler)


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
    Último_en_Pie = "lastStand"
    Volleybrawl = "volleyBrawl"
    Zona_Restringida = "hotZone"


class Result(Enum):
    EMPATE = "draw"
    GANADA = "victory"
    PERDIDA = "defeat"


class TypeEnum(Enum):
    Desafio = "challenge"
    Estelar_Solo = "soloRanked"
    Estelar_Team = "teamRanked"
    Normal = "ranked"


@dataclass
class Battle:
    mode: Mode
    type: TypeEnum
    rank: Optional[int] = None
    trophy_change: Optional[int] = None
    teams: Optional[list[list[StarPlayer]]] = None
    result: Optional[Result] = None
    duration: Optional[int] = None
    star_player: Optional[StarPlayer] = None
    players: Optional[list[StarPlayer]] = None

    @staticmethod
    def from_dict(obj: Any) -> "Battle":
        assert isinstance(obj, dict)
        mode = Mode(obj.get("mode"))
        type = TypeEnum(obj.get("type"))
        rank = from_union([from_int, from_none], obj.get("rank"))
        trophy_change = from_union([from_int, from_none], obj.get("trophyChange"))
        teams = from_union(
            [
                lambda x: from_list(lambda x: from_list(StarPlayer.from_dict, x), x),
                from_none,
            ],
            obj.get("teams"),
        )
        result = from_union([Result, from_none], obj.get("result"))
        duration = from_union([from_int, from_none], obj.get("duration"))
        star_player = from_union(
            [StarPlayer.from_dict, from_none], obj.get("starPlayer")
        )
        players = from_union(
            [lambda x: from_list(StarPlayer.from_dict, x), from_none],
            obj.get("players"),
        )
        return Battle(
            mode,
            type,
            rank,
            trophy_change,
            teams,
            result,
            duration,
            star_player,
            players,
        )


@dataclass
class Event:
    id: int
    mode: Optional[Mode] = None
    map: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Event":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        mode = from_union([from_none, Mode], obj.get("mode"))
        map = from_union([from_str, from_none], obj.get("map"))
        return Event(id, mode, map)


@dataclass
class BattleLog:
    battle_time: str
    event: Event
    battle: Battle

    @staticmethod
    def from_dict(obj: Any) -> "BattleLog":
        assert isinstance(obj, dict)
        battle_time = from_str(obj.get("battleTime"))
        event = Event.from_dict(obj.get("event"))
        battle = Battle.from_dict(obj.get("battle"))
        return BattleLog(battle_time, event, battle)
