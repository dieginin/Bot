from colorama import Fore
from discord.ext import commands

from config import COGS


async def cog_loader(bot: commands.Bot):
    for cog in COGS:
        try:
            await bot.load_extension(cog)
        except:
            pass
        print(Fore.MAGENTA + "COG" + Fore.RESET + f" {cog} cargados")
