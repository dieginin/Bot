import discord
import requests
from discord import app_commands

from decorators.in_club import in_club
from models.BrawlDatum import BrawlDatum
from models.Events import Events

url = "https://api.brawlapi.com/v1"


class Eventos(app_commands.Group):
    @app_commands.command(
        description="Ve los brawlers con más indice de victorias de los eventos activos"
    )
    @in_club()
    async def activos(self, interaction: discord.Interaction):
        await interaction.response.defer()
        eventsDB = Events.from_dict(requests.get(url + "/events").json())
        brawlersDB = [
            BrawlDatum.from_dict(b)
            for b in requests.get(url + "/brawlers").json()["list"]
        ]

        foco = eventsDB.active
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

    @app_commands.command(
        description="Ve los brawlers con más indice de victorias de los eventos próximos"
    )
    @in_club()
    async def proximos(self, interaction: discord.Interaction):
        await interaction.response.defer()
        eventsDB = Events.from_dict(requests.get(url + "/events").json())
        brawlersDB = [
            BrawlDatum.from_dict(b)
            for b in requests.get(url + "/brawlers").json()["list"]
        ]

        foco = eventsDB.upcoming
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
    bot.tree.add_command(Eventos())
