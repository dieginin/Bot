import discord
from discord import app_commands


async def on_error(interaction: discord.Interaction, error):
    embed = discord.Embed(title="Error", description="", color=discord.Color.dark_red())

    if isinstance(error, app_commands.CheckFailure):
        embed.description = "Primero debes lanzar el comando **`/vincular`** para vincular tu perfil\nNo posees nick o tu nick no pertenece al club"
    elif isinstance(error, Exception):
        embed.description = "No existe el tag que indicaste"
    else:
        embed.description = "Tuve un :dash:, perdón\nIntentalo de nuevo"
        await interaction.followup.send(embed=embed, ephemeral=True)
        raise error

    await interaction.followup.send(embed=embed, ephemeral=True)
