import requests

from config import ROYALE_URL, TOKEN_API
from models.Club import Role


def get_member_info(nick: str) -> tuple[str, Role]:
    members_data = requests.get(
        ROYALE_URL + "clubs/%232JUCPV8PR",
        headers={"Authorization": f"Bearer {TOKEN_API}"},
    ).json()["members"]

    if nick and nick in [member["name"] for member in members_data]:
        return next(
            (member["tag"] for member in members_data if member["name"] == nick)
        ), next((member["role"] for member in members_data if member["name"] == nick))
    return '', Role.Miembro
