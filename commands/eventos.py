from typing import Optional

import discord
import requests
from discord import app_commands
from discord.ext import commands

from decorators.in_club import in_club
from models.BrawlDatum import BrawlDatum
from models.Events import Events

url = "https://api.brawlapi.com/v1"


class Eventos(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="eventos",
        description="Ve los brawlers con más indice de victorias de los eventos activos o próximos",
    )
    @app_commands.describe(
        estatus="Seleciona si quieres ver los eventos activos o los próximos eventos"
    )
    @app_commands.choices(
        estatus=[
            app_commands.Choice(name="Eventos Activos", value="act"),
            app_commands.Choice(name="Próximos Eventos", value="upc"),
        ]
    )
    @in_club()
    async def eventos(
        self,
        interaction: discord.Interaction,
        estatus: Optional[app_commands.Choice[str]],
    ):
        await interaction.response.defer()
        if not estatus:
            estatus = app_commands.Choice(name="Eventos Activos", value="act")

        eventsDB = Events.from_dict(requests.get(url + "/events").json())
        brawlersDB = [
            BrawlDatum.from_dict(b)
            for b in requests.get(url + "/brawlers").json()["list"]
        ]

        foco = eventsDB.active if estatus.value == "act" else eventsDB.upcoming
        embeds = []

        for event in foco:
            embed = discord.Embed(
                title=event.map.name,
                description=event.map.environment.name,
                color=discord.Color.from_str(event.map.game_mode.bg_color),
            )
            embed.set_author(
                name=event.map.game_mode.name,
                icon_url=event.map.game_mode.image_url,
                url=event.map.link,
            )
            embed.set_image(url=event.map.environment.image_url)
            embed.set_thumbnail(url=event.map.image_url)

            for br in event.map.stats[:6]:
                brawler = next(
                    (member for member in brawlersDB if member.id == br.brawler)
                )
                embed.add_field(name=brawler.name, value=f"{br.win_rate}%")

            embeds.append(embed)

        await interaction.followup.send(embeds=embeds)


async def setup(bot):
    await bot.add_cog(Eventos(bot))
