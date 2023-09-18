import random

import discord
import pyjokes
from discord import app_commands
from discord.ext import commands


class Extras(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="chiste", description="Te cuento un chiste")
    async def chiste(self, interaction: discord.Interaction):
        joke = pyjokes.get_jokes(language="es", category="all")
        rnd = random.randint(0, len(joke) - 1)
        await interaction.response.send_message(joke[rnd])

    @app_commands.command(name="ynfo", description="Información del servidor")
    async def ynfo(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=interaction.guild,
            description="_*Valhalla*_ es una creencia nórdica dónde se hace semejanza a la esperanza, la lucha, la creencia, la unión. El _*valhalla*_ es lo que todo vikingo deseaba, es como la gente que añora llegar al cielo.",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="Dueño del Server", value=interaction.guild.owner)  # type: ignore
        embed.add_field(name="Server ID", value=interaction.guild_id)
        embed.add_field(name="", value="")
        embed.add_field(name="Server Creado", value=interaction.guild.created_at.strftime("%d %B  %Y"))  # type: ignore
        embed.add_field(name="Miembros", value=interaction.guild.member_count)  # type: ignore
        embed.set_thumbnail(url=interaction.guild.icon)  # type: ignore
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Extras(bot))
