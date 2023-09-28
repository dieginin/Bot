from dataclasses import dataclass
from typing import Any, Optional

from helpers import from_int, from_none, from_str, from_union, game_modes


@dataclass
class Environment:
    id: int
    name: str
    image_url: str

    @staticmethod
    def from_dict(obj: Any) -> "Environment":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        image_url = from_str(obj.get("imageUrl"))
        return Environment(id, name, image_url)


@dataclass
class GameMode:
    name: str
    color: str
    bg_color: str
    link: str
    image_url: str
    id: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "GameMode":
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        name = game_modes.get(name, name)
        color = from_str(obj.get("color"))
        bg_color = from_str(obj.get("bgColor"))
        link = from_str(obj.get("link"))
        image_url = from_str(obj.get("imageUrl"))
        id = from_union([from_int, from_none], obj.get("id"))
        return GameMode(name, color, bg_color, link, image_url, id)


@dataclass
class Map:
    id: int
    name: str
    link: str
    image_url: str
    environment: Environment
    game_mode: GameMode
    credit: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Map":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        link = from_str(obj.get("link"))
        image_url = from_str(obj.get("imageUrl"))
        environment = Environment.from_dict(obj.get("environment"))
        game_mode = GameMode.from_dict(obj.get("gameMode"))
        credit = from_union([from_none, from_str], obj.get("credit"))
        return Map(
            id,
            name,
            link,
            image_url,
            environment,
            game_mode,
            credit,
        )
