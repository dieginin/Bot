from dataclasses import dataclass
from typing import Any, Callable, List, TypeVar

T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


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
    path: str
    version: int
    description: str
    description_html: str
    image_url: str
    released: bool

    @staticmethod
    def from_dict(obj: Any) -> "Gadget":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        path = from_str(obj.get("path"))
        version = from_int(obj.get("version"))
        description = from_str(obj.get("description"))
        description_html = from_str(obj.get("descriptionHtml"))
        image_url = from_str(obj.get("imageUrl"))
        released = from_bool(obj.get("released"))
        return Gadget(
            id, name, path, version, description, description_html, image_url, released
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
class BrawlDatum:
    id: int
    avatar_id: int
    name: str
    hash: str
    path: str
    released: bool
    version: int
    link: str
    image_url: str
    image_url2: str
    image_url3: str
    brawl_class: Class
    rarity: Rarity
    unlock: None
    description: str
    description_html: str
    star_powers: List[Gadget]
    gadgets: List[Gadget]
    videos: List[Any]

    @staticmethod
    def from_dict(obj: Any) -> "BrawlDatum":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        avatar_id = from_int(obj.get("avatarId"))
        name = from_str(obj.get("name"))
        hash = from_str(obj.get("hash"))
        path = from_str(obj.get("path"))
        released = from_bool(obj.get("released"))
        version = from_int(obj.get("version"))
        link = from_str(obj.get("link"))
        image_url = from_str(obj.get("imageUrl"))
        image_url2 = from_str(obj.get("imageUrl2"))
        image_url3 = from_str(obj.get("imageUrl3"))
        brawl_class = Class.from_dict(obj.get("class"))
        rarity = Rarity.from_dict(obj.get("rarity"))
        unlock = from_none(obj.get("unlock"))
        description = from_str(obj.get("description"))
        description_html = from_str(obj.get("descriptionHtml"))
        star_powers = from_list(Gadget.from_dict, obj.get("starPowers"))
        gadgets = from_list(Gadget.from_dict, obj.get("gadgets"))
        videos = from_list(lambda x: x, obj.get("videos"))
        return BrawlDatum(
            id,
            avatar_id,
            name,
            hash,
            path,
            released,
            version,
            link,
            image_url,
            image_url2,
            image_url3,
            brawl_class,
            rarity,
            unlock,
            description,
            description_html,
            star_powers,
            gadgets,
            videos,
        )
