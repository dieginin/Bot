import discord
from discord import app_commands


async def on_error(interaction: discord.Interaction, error):
    embed = discord.Embed(title="Error", description="", color=discord.Color.dark_red())

    if isinstance(error, app_commands.CheckFailure):
        embed.description = f"Primero debes lanzar el comando **`/vincular`** para vincular tu perfil\nNo posees nick o tu nick no pertenece al club"
    else:
        raise error

    await interaction.response.send_message(embed=embed, ephemeral=True)
