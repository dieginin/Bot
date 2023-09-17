import discord
from discord import Interaction, app_commands

from decorators.in_club import in_club

class Brawlers(app_commands.Group):
    @app_commands.command()
    async def actuales(self, interaction: discord.Interaction):
        await interaction.response.send_message('No esta listo')
        
    @app_commands.command()
    @in_club()
    async def mejores(self, interaction: discord.Interaction):
        await interaction.response.send_message('No esta listo')

async def setup(bot):
    bot.tree.add_command(Brawlers())
        