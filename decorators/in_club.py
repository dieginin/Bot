import discord
import requests
from discord import app_commands

from config import ROYALE_URL, TOKEN_API


def in_club():
    members_data = requests.get(
        ROYALE_URL + "clubs/%232JUCPV8PR",
        headers={"Authorization": f"Bearer {TOKEN_API}"},
    ).json()["members"]

    def predicate(interaction: discord.Interaction):
        nick = interaction.user.nick  # type: ignore

        return (
            True
            if nick and nick in [member["name"] for member in members_data]
            else False
        )

    return app_commands.check(predicate)
