import discord
from colorama import Fore
from discord.ext import commands

from config import TOKEN_BOT
from errors import on_error
from functions import cog_loader

# Creación del bot
bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())


@bot.command(hidden=True)
async def sync(ctx):
    await ctx.send("Sincronizando...")
    await bot.tree.sync()
    await ctx.send("Listo")


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening, name="a los dioses"
        )
    )

    await cog_loader(bot)
    print(Fore.LIGHTBLUE_EX + "BOT" + Fore.RESET + f' "{bot.user}" listo')

    print(Fore.LIGHTGREEN_EX + "CMD" + Fore.RESET + " sincronizando")
    print(
        Fore.LIGHTGREEN_EX
        + "CMD"
        + Fore.RESET
        + f" {len(await bot.tree.sync())} sincronizado"
    )


bot.tree.on_error = on_error


bot.run(f"{TOKEN_BOT}")
