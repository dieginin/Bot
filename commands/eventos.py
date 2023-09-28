from datetime import datetime, timezone

import discord
from discord import app_commands
from discord.ext import commands

from connections import BrawlApi, BrawlStars
from secure import in_club

url = "https://api.brawlapi.com/v1"


class Eventos(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="eventos",
        description="Ve los brawlers con más indice de victorias de los eventos activos",
    )
    @in_club()
    async def eventos(
        self,
        interaction: discord.Interaction,
    ):
        await interaction.response.defer()
        bs = BrawlStars()
        ba = BrawlApi()

        events = bs.get_events()
        embeds = []

        for event in events:
            try:
                edata = ba.get_map(str(event.event.id))
            except:
                continue

            dif = event.end_time - datetime.utcnow().replace(tzinfo=timezone.utc)
            horas = dif.days * 24 + dif.seconds // 3600
            minutos = (dif.seconds % 3600) // 60
            embed = discord.Embed(
                title=event.event.map,
                description=f"Faltan {horas} horas y {minutos} minutos",
                color=discord.Color.from_str(edata.game_mode.bg_color),
            )
            embed.set_author(
                name=event.event.mode,
                icon_url=edata.game_mode.image_url,
                url=edata.link,
            )
            embed.set_image(url=edata.environment.image_url)
            embed.set_thumbnail(url=edata.image_url)

            embeds.append(embed)

        await interaction.followup.send(embeds=embeds)


async def setup(bot):
    await bot.add_cog(Eventos(bot))
