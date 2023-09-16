import sys
import traceback
import discord
from discord.ext import commands


class Errors(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener("on_app_command_error")
    async def on_command_error(self, interaction, error):
        embed = discord.Embed(
            title="Error", description="", color=discord.Color.dark_red()
        )

        if isinstance(error, commands.CheckFailure):
            embed.description = f"Primero debes lanzar el comando **`/vincular`** para vincular tu perfil\nNo posees nick o tu nick no pertenece al club"
        else:
            print(
                "Ignoring exception in command {}:".format(interaction.command),
                file=sys.stderr,
            )
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr
            )
            # raise error

        await interaction.send(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Errors(bot))
