import discord
import requests
from discord import app_commands
from discord.ext import commands

from config import ROYALE_URL, TOKEN_API
from views.MembersView import MembersView


class Settings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="vincular", description="Vilcula tu perfil con el perfil del club"
    )
    @app_commands.describe(grupo="Seleciona al grupo al que perteneces")
    @app_commands.choices(
        grupo=[
            app_commands.Choice(name="Ver Grupos", value=0),
            app_commands.Choice(name="Grupo 1", value=1),
            app_commands.Choice(name="Grupo 2", value=2),
        ]
    )
    async def vincular(
        self, interaction: discord.Interaction, grupo: app_commands.Choice[int]
    ):
        members_data = requests.get(
            ROYALE_URL + "clubs/%232JUCPV8PR",
            headers={"Authorization": f"Bearer {TOKEN_API}"},
        ).json()["members"]

        if grupo.value == 0:
            grupo_1 = "\n".join([f"{members_data[i]['name']:20}" for i in range(15)])
            grupo_2 = "\n".join(
                [f"{members_data[i]['name']:20}" for i in range(15, len(members_data))]
            )

            embed = discord.Embed(color=discord.Color.random())
            embed.add_field(name="Grupo 1", value=grupo_1)
            embed.add_field(name="Grupo 2", value=grupo_2)
            await interaction.response.send_message(
                "Necesitas asociar un grupo, repite el comando con el grupo al que perteneces\nej. /vincular 2",
                embed=embed,
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "Quién eres tu?", view=MembersView(grupo.value), ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(Settings(bot))
