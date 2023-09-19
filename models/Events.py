from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, List, Optional, TypeVar

import dateutil.parser
from deep_translator import GoogleTranslator

T = TypeVar("T")
traductor = GoogleTranslator(source="en", target="es")

mode = {
    "wipeout": "Aniquilación",
    "siege": "Asedio",
    "heist": "Atraco",
    "gem grab": "Atrapagemas",
    "brawl gall": "Balón Brawl",
    "basket brawl": "Basketbrawl",
    "bot drop": "Bowdrop",
    "bounty": "Caza Estelar",
    "unknown": "Desconocido",
    "duels": "Duelo",
    "big game": "Gran Juego",
    "hold the trophy": "Hold The Throphy",
    "hunters": "Hunters",
    "trophy thieves": "Ladrones Trofeos",
    "lone star": "Lone Star",
    "knockout": "Noqueo",
    "payload": "Payload",
    "boss fight": "Pelea de Jefe",
    "present plunder": "Present Plunder",
    "robo rumble": "Robo Rumble",
    "snowtel thieves": "Snowtel Thieves",
    "super city rampage": "Super City Rampage",
    "duo showdown": "Supervivencia Duo",
    "solo showdown": "Supervivencia Solo",
    "takedown": "Takedown",
    "last stand": "Último en Pie",
    "volley brawl": "Volleybrawl",
    "hot zone": "Zona Restringida",
}


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
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


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


@dataclass
class Environment:
    id: int
    name: str
    hash: str
    path: str
    version: int
    image_url: str

    @staticmethod
    def from_dict(obj: Any) -> "Environment":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        name = traductor.translate(name)
        hash = from_str(obj.get("hash"))
        path = from_str(obj.get("path"))
        version = from_int(obj.get("version"))
        image_url = from_str(obj.get("imageUrl"))
        return Environment(id, name, hash, path, version, image_url)


@dataclass
class GameMode:
    id: int
    name: str
    hash: str
    version: int
    color: str
    bg_color: str
    link: str
    image_url: str

    @staticmethod
    def from_dict(obj: Any) -> "GameMode":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        name = mode.get(name.lower(), name)
        hash = from_str(obj.get("hash"))
        version = from_int(obj.get("version"))
        color = from_str(obj.get("color"))
        bg_color = from_str(obj.get("bgColor"))
        link = from_str(obj.get("link"))
        image_url = from_str(obj.get("imageUrl"))
        return GameMode(id, name, hash, version, color, bg_color, link, image_url)


@dataclass
class Stat:
    brawler: int
    win_rate: float
    use_rate: float

    @staticmethod
    def from_dict(obj: Any) -> "Stat":
        assert isinstance(obj, dict)
        brawler = from_int(obj.get("brawler"))
        win_rate = from_float(obj.get("winRate"))
        use_rate = from_float(obj.get("useRate"))
        return Stat(brawler, win_rate, use_rate)


@dataclass
class Map:
    id: int
    new: bool
    disabled: bool
    name: str
    hash: str
    version: int
    link: str
    image_url: str
    environment: Environment
    game_mode: GameMode
    last_active: int
    data_updated: int
    stats: List[Stat]
    team_stats: List[Any]
    credit: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Map":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        new = from_bool(obj.get("new"))
        disabled = from_bool(obj.get("disabled"))
        name = from_str(obj.get("name"))
        name = traductor.translate(name)
        hash = from_str(obj.get("hash"))
        version = from_int(obj.get("version"))
        link = from_str(obj.get("link"))
        image_url = from_str(obj.get("imageUrl"))
        environment = Environment.from_dict(obj.get("environment"))
        game_mode = GameMode.from_dict(obj.get("gameMode"))
        last_active = from_int(obj.get("lastActive"))
        data_updated = from_int(obj.get("dataUpdated"))
        stats = from_list(Stat.from_dict, obj.get("stats"))
        team_stats = from_list(lambda x: x, obj.get("teamStats"))
        credit = from_union([from_none, from_str], obj.get("credit"))
        return Map(
            id,
            new,
            disabled,
            name,
            hash,
            version,
            link,
            image_url,
            environment,
            game_mode,
            last_active,
            data_updated,
            stats,
            team_stats,
            credit,
        )


@dataclass
class Slot:
    id: int
    name: str
    emoji: str
    hash: str
    list_alone: bool
    hideable: bool
    background: None
    hide_for_slot: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "Slot":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        emoji = from_str(obj.get("emoji"))
        hash = from_str(obj.get("hash"))
        list_alone = from_bool(obj.get("listAlone"))
        hideable = from_bool(obj.get("hideable"))
        background = from_none(obj.get("background"))
        hide_for_slot = from_union([from_int, from_none], obj.get("hideForSlot"))
        return Slot(
            id, name, emoji, hash, list_alone, hideable, background, hide_for_slot
        )


@dataclass
class Active:
    slot: Slot
    predicted: bool
    start_time: datetime
    end_time: datetime
    reward: int
    map: Map
    modifier: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Active":
        assert isinstance(obj, dict)
        slot = Slot.from_dict(obj.get("slot"))
        predicted = from_bool(obj.get("predicted"))
        start_time = from_datetime(obj.get("startTime"))
        end_time = from_datetime(obj.get("endTime"))
        reward = from_int(obj.get("reward"))
        map = Map.from_dict(obj.get("map"))
        modifier = from_union([from_none, from_str], obj.get("modifier"))
        return Active(slot, predicted, start_time, end_time, reward, map, modifier)


@dataclass
class Upcoming:
    slot: Slot
    predicted: bool
    history_length: int
    start_time: datetime
    end_time: datetime
    reward: int
    map: Map
    modifier: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Upcoming":
        assert isinstance(obj, dict)
        slot = Slot.from_dict(obj.get("slot"))
        predicted = from_bool(obj.get("predicted"))
        history_length = from_int(obj.get("historyLength"))
        start_time = from_datetime(obj.get("startTime"))
        end_time = from_datetime(obj.get("endTime"))
        reward = from_int(obj.get("reward"))
        map = Map.from_dict(obj.get("map"))
        modifier = from_union([from_none, from_str], obj.get("modifier"))
        return Upcoming(
            slot, predicted, history_length, start_time, end_time, reward, map, modifier
        )


@dataclass
class Events:
    active: List[Active]
    upcoming: List[Upcoming]

    @staticmethod
    def from_dict(obj: Any) -> "Events":
        assert isinstance(obj, dict)
        active = from_list(Active.from_dict, obj.get("active"))
        upcoming = from_list(Upcoming.from_dict, obj.get("upcoming"))
        return Events(active, upcoming)
