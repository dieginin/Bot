import discord
from discord.ext import commands


class Errors(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        embed = discord.Embed(
            title="Error", description="", color=discord.Color.dark_red()
        )

        if isinstance(err, commands.CheckFailure):
            embed.description = f"Primero debes lanzar el comando **`/vincular`** para vincular tu perfil\nNo posees nick o tu nick no pertenece al club"
        else:
            raise err

        await ctx.send(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Errors(bot))
