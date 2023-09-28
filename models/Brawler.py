from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from helpers import from_int, from_list, from_none, from_str, from_union


@dataclass
class Gadget:
    id: int
    name: str

    @staticmethod
    def from_dict(obj: Any) -> "Gadget":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        return Gadget(id, name)


class GearName(Enum):
    Aceite_pegajoso = "STICKY OIL"
    Blindaje = "SHIELD"
    Cabeza_gruesa = "THICC HEAD"
    Carga_de_gadget = "GADGET CHARGE"
    Cuadruplos = "QUADRUPLETS"
    Daño = "DAMAGE"
    Hablar_con_la_mano = "TALK TO THE HAND"
    Humo_permanente = "LINGERING SMOKE"
    Picos_pegajosos = "STICKY SPIKES"
    Poder_para_mascotas = "PET POWER"
    Salud = "HEALTH"
    Súper_carga = "SUPER CHARGE"
    Súper_torreta = "SUPER TURRET"
    Tormenta_agotadora = "EXHAUSTING STORM"
    Toxinas_duraderas = "ENDURING TOXINS"
    Velocidad = "SPEED"
    Velocidad_de_recarga = "RELOAD SPEED"
    Visión = "VISION"


@dataclass
class Gear:
    id: int
    name: GearName
    level: int

    @staticmethod
    def from_dict(obj: Any) -> "Gear":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = GearName(obj.get("name"))
        level = from_int(obj.get("level"))
        return Gear(id, name, level)


@dataclass
class Brawler:
    id: int
    name: str
    star_powers: Optional[list[Gadget]] = None
    gadgets: Optional[list[Gadget]] = None
    power: Optional[int] = None
    trophies: Optional[int] = None
    rank: Optional[int] = None
    highest_trophies: Optional[int] = None
    gears: Optional[list[Gear]] = None

    @staticmethod
    def from_dict(obj: Any) -> "Brawler":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        star_powers = from_union(
            [lambda x: from_list(Gadget.from_dict, x), from_none], obj.get("starPowers")
        )
        gadgets = from_union(
            [lambda x: from_list(Gadget.from_dict, x), from_none], obj.get("gadgets")
        )
        power = from_union([from_int, from_none], obj.get("power"))
        trophies = from_union([from_int, from_none], obj.get("trophies"))
        rank = from_union([from_int, from_none], obj.get("rank"))
        highest_trophies = from_union([from_int, from_none], obj.get("highestTrophies"))
        gears = from_union(
            [lambda x: from_list(Gear.from_dict, x), from_none], obj.get("gears")
        )
        return Brawler(
            id,
            name,
            star_powers,
            gadgets,
            power,
            trophies,
            rank,
            highest_trophies,
            gears,
        )
