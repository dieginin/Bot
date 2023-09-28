from dataclasses import dataclass
from typing import Any, Optional

from helpers import from_bool, from_int, from_list, from_none, from_str, from_union
from models import Brawler


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
    exp_level: int
    exp_points: int
    is_qualified: bool
    the_3_vs3_victories: int
    solo_victories: int
    duo_victories: int
    best_robo_rumble_time: int
    best_time_as_big_brawler: int
    brawlers: list[Brawler]
    club: Optional[Club] = None
    highest_power_play_points: Optional[int] = None

    @property
    def brawlers_count(self):
        return len(self.brawlers)

    @property
    def brawlers_9(self):
        return [brawler for brawler in self.brawlers if brawler.power == 9]

    @property
    def brawlers_10(self):
        return [brawler for brawler in self.brawlers if brawler.power == 10]

    @property
    def brawlers_11(self):
        return [brawler for brawler in self.brawlers if brawler.power == 11]

    @property
    def grade(self):
        # Ponderación para cada criterio
        total_brawlers = 72
        weight_brawlers_count = 0.2 * (len(self.brawlers) / total_brawlers)
        weight_brawlers_power_11 = 0.3
        weight_brawlers_power_10 = 0.2
        weight_brawlers_power_9 = 0.1
        weight_trophies = 0.2

        # Calcular calificación en base a los criterios
        score = (
            (self.brawlers_count * weight_brawlers_count)
            + (len(self.brawlers_9) * weight_brawlers_power_9)
            + (len(self.brawlers_10) * weight_brawlers_power_10)
            + (len(self.brawlers_11) * weight_brawlers_power_11)
            + (self.trophies * weight_trophies)
        )

        # Si los trofeos son mayores a 25000, mejorar la calificación
        if self.trophies > 25000:
            score *= 1.2  # Incremento del 20% en la calificación

        # Ajustar la calificación en una escala de 1 a 10
        final_rating = max(1, min(10, score / 1000))

        if isinstance(final_rating, int):
            return str(final_rating)
        else:
            return f"{final_rating:.2f}"

    @staticmethod
    def from_dict(obj: Any) -> "Player":
        assert isinstance(obj, dict)
        tag = from_str(obj.get("tag"))
        name = from_str(obj.get("name"))
        try:
            name_color = from_str(obj.get("nameColor"))
        except:
            name_color = "#ffffff"
        icon = Icon.from_dict(obj.get("icon"))
        trophies = from_int(obj.get("trophies"))
        highest_trophies = from_int(obj.get("highestTrophies"))
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
        try:
            club = Club.from_dict(obj.get("club"))
        except:
            club = None
        highest_power_play_points = from_union(
            [from_int, from_none], obj.get("highestPowerPlayPoints")
        )
        return Player(
            tag,
            name,
            name_color,
            icon,
            trophies,
            highest_trophies,
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
            highest_power_play_points,
        )
