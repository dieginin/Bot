from dataclasses import dataclass
from typing import Any

from helpers import from_int, from_list, from_str


@dataclass
class Class:
    id: int
    name: str

    @staticmethod
    def from_dict(obj: Any) -> "Class":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        return Class(id, name)


@dataclass
class Gadget:
    id: int
    name: str
    image_url: str

    @staticmethod
    def from_dict(obj: Any) -> "Gadget":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        image_url = from_str(obj.get("imageUrl"))

        return Gadget(
            id,
            name,
            image_url,
        )


@dataclass
class Rarity:
    id: int
    name: str
    color: str

    @staticmethod
    def from_dict(obj: Any) -> "Rarity":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        color = from_str(obj.get("color"))
        return Rarity(id, name, color)


@dataclass
class BrawlerData:
    id: int
    avatar_id: int
    name: str
    link: str
    image_url: str
    emoji_url: str
    brawler_class: Class
    rarity: Rarity
    star_powers: list[Gadget]
    gadgets: list[Gadget]

    @staticmethod
    def from_dict(obj: Any) -> "BrawlerData":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        avatar_id = from_int(obj.get("avatarId"))
        name = from_str(obj.get("name"))
        link = from_str(obj.get("link"))
        image_url = from_str(obj.get("imageUrl2"))
        emoji_url = from_str(obj.get("imageUrl3"))
        brawler_class = Class.from_dict(obj.get("class"))
        rarity = Rarity.from_dict(obj.get("rarity"))
        star_powers = from_list(Gadget.from_dict, obj.get("starPowers"))
        gadgets = from_list(Gadget.from_dict, obj.get("gadgets"))
        return BrawlerData(
            id,
            avatar_id,
            name,
            link,
            image_url,
            emoji_url,
            brawler_class,
            rarity,
            star_powers,
            gadgets,
        )
