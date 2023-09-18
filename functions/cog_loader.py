import os

from colorama import Fore
from discord.ext import commands


async def cog_loader(bot: commands.Bot):
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"commands.{filename[:-3]}")
                print(
                    Fore.MAGENTA
                    + "COG"
                    + Fore.RESET
                    + f" commands.{filename[:-3]} cargados"
                )
            except:
                pass
