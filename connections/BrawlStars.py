import requests

from config import TOKEN_API, URL_ROYALE
from models import BattleLog, Brawler, Club, Member, Player, Rotation


class BrawlStars:
    def get_battlelog(self, tag: str) -> list[BattleLog]:
        tag = tag.strip()
        if tag[0] == "#":
            tag = tag[1:]

        url = URL_ROYALE + "players/%23" + tag + "/battlelog"
        req = requests.get(
            url,
            headers={"Authorization": f"Bearer {TOKEN_API}"},
        )
        if req.status_code == 200:
            return [BattleLog.from_dict(bl) for bl in req.json()["items"]]
        else:
            raise Exception("Error en petición")

    def get_club(self, tag: str) -> Club:
        tag = tag.strip()
        if tag[0] == "#":
            tag = tag[1:]

        url = URL_ROYALE + "clubs/%23" + tag
        req = requests.get(
            url,
            headers={"Authorization": f"Bearer {TOKEN_API}"},
        )

        if req.status_code == 200:
            return Club.from_dict(req.json())
        else:
            raise Exception("Error en petición")

    def get_club_members(self, tag: str) -> list[Member]:
        tag = tag.strip()
        if tag[0] == "#":
            tag = tag[1:]

        url = URL_ROYALE + "clubs/%23" + tag + "/members"
        req = requests.get(
            url,
            headers={"Authorization": f"Bearer {TOKEN_API}"},
        )

        if req.status_code == 200:
            return [Member.from_dict(m) for m in req.json()["items"]]
        else:
            raise Exception("Error en petición")

    def get_brawler(self, bId: str) -> Brawler:
        bId = bId.strip()

        url = URL_ROYALE + "brawlers/" + bId
        req = requests.get(
            url,
            headers={"Authorization": f"Bearer {TOKEN_API}"},
        )
        if req.status_code == 200:
            return Brawler.from_dict(req.json())
        else:
            raise Exception("Error en petición")

    def get_brawlers(self) -> list[Brawler]:
        url = URL_ROYALE + "brawlers"
        req = requests.get(
            url,
            headers={"Authorization": f"Bearer {TOKEN_API}"},
        )
        if req.status_code == 200:
            return [Brawler.from_dict(b) for b in req.json()["items"]]
        else:
            raise Exception("Error en petición")

    def get_player(self, tag: str) -> Player:
        tag = tag.strip()
        if tag[0] == "#":
            tag = tag[1:]

        url = URL_ROYALE + "players/%23" + tag
        req = requests.get(
            url,
            headers={"Authorization": f"Bearer {TOKEN_API}"},
        )
        if req.status_code == 200:
            return Player.from_dict(req.json())
        else:
            raise Exception("Error en petición")

    def get_events(self) -> list[Rotation]:
        url = URL_ROYALE + "events/rotation"
        req = requests.get(
            url,
            headers={"Authorization": f"Bearer {TOKEN_API}"},
        )
        if req.status_code == 200:
            return [Rotation.from_dict(e) for e in req.json()]
        else:
            raise Exception("Error en petición")
