import discord
from discord import app_commands
from discord.ext import commands

from connections import BrawlApi
from secure import in_club


class Extras(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="emoji", description="Te mando el emoji de tu brawler favorito"
    )
    @in_club()
    async def emoji(self, interaction: discord.Interaction, nombre: str):
        bws = BrawlApi().get_brawlers()
        try:
            emoji = next(b.emoji_url for b in bws if b.name.lower() == nombre.lower())

            await interaction.response.send_message(emoji)
        except:
            await interaction.response.send_message(
                f"El brawler {nombre} no existe.", ephemeral=True, delete_after=5
            )


async def setup(bot):
    await bot.add_cog(Extras(bot))
