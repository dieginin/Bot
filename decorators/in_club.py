import discord
import requests
from discord import app_commands
from dotenv import dotenv_values

settings = dotenv_values()
brawlAPI = "https://bsproxy.royaleapi.dev/v1/"


def in_club():
    members_data = requests.get(
        brawlAPI + "clubs/%232JUCPV8PR",
        headers={"Authorization": f"Bearer {settings['BRAWL_API']}"},
    ).json()["members"]

    def predicate(interaction: discord.Interaction):
        nick = interaction.user.nick  # type: ignore

        return (
            True
            if nick and nick in [member["name"] for member in members_data]
            else False
        )

    return app_commands.check(predicate)
