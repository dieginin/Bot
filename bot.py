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

    cogs = ["commands.extras"]
    for cog in cogs:
        await bot.load_extension(cog)
        print(f"cog: {cog} loaded")
    print(f'El bot "{bot.user}" está listo')

    print(f"Sincronizado {len(await bot.tree.sync())} comandos")


@bot.event
async def on_command_error(ctx, err):
    embed = discord.Embed(title="Error", description="", color=discord.Color.dark_red())

    if isinstance(err, commands.CheckFailure):
        embed.description = f"Primero debes lanzar el comando **`/vincular`** para vincular tu perfil\nNo posees nick o tu nick no pertenece al club"
    else:
        raise err

    await ctx.send(embed=embed, ephemeral=True)


bot.run(f"{TOKEN_BOT}")
