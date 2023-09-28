import requests

from config import URL_BRAWLAPI
from models import BrawlerData, Map


class BrawlApi:
    def get_brawler(self, bId: str):
        bId = bId.strip()

        url = URL_BRAWLAPI + "brawlers/" + bId
        req = requests.get(url)
        if req.status_code == 200:
            return BrawlerData.from_dict(req.json())
        else:
            raise Exception("Error en petición")

    def get_brawlers(self):
        url = URL_BRAWLAPI + "brawlers"
        req = requests.get(url)
        if req.status_code == 200:
            return [BrawlerData.from_dict(b) for b in req.json()["list"]]
        else:
            raise Exception("Error en petición")

    def get_map(self, mId: str):
        mId = mId.strip()

        url = URL_BRAWLAPI + "maps/" + mId
        req = requests.get(url)
        if req.status_code == 200:
            return Map.from_dict(req.json())
        else:
            raise Exception("Error en petición")

    def get_maps(self):
        url = URL_BRAWLAPI + "maps"
        req = requests.get(url)
        if req.status_code == 200:
            return [Map.from_dict(m) for m in req.json()["list"]]
        else:
            raise Exception("Error en petición")
