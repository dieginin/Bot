import discord
from discord.ext import commands

from config import TOKEN_BOT

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

    cogs = ["commands.extras", "errors.errors"]
    for cog in cogs:
        await bot.load_extension(cog)
        print(f"cog: {cog} loaded")
    print(f'El bot "{bot.user}" está listo')

    print(f"Sincronizado {len(await bot.tree.sync())} comandos")


bot.run(f"{TOKEN_BOT}")
