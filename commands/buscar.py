import calendar
import operator
from typing import Optional

import discord
import requests
from deep_translator import GoogleTranslator
from discord import app_commands
from discord.ext import commands

from config import ROYALE_URL, TOKEN_API
from decorators.in_club import in_club
from functions.get_member_info import get_member_info
from functions.rate import rate
from models.BattleLog import BattleLog
from models.Brawler import Brawler
from models.Player import Player

url = "https://api.brawlapi.com/v1"

traductor = GoogleTranslator(source="en", target="es")


class Buscar(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description="Valora tu perfil o el de otra persona")
    @app_commands.describe(tag="Intresa el tag")
    @in_club()
    async def valorar(
        self, interaction: discord.Interaction, tag: Optional[str] = None
    ):
        if not tag:
            tag, _ = get_member_info(interaction.user.nick)  # type: ignore
        else:
            await interaction.response.defer()

        if tag[0] != "#":
            tag = "#" + tag
        pd_data = requests.get(
            ROYALE_URL + f"players/%23{tag[1:]}",
            headers={"Authorization": f"Bearer {TOKEN_API}"},
        )

        if pd_data.status_code != 200:
            await interaction.followup.send(
                embed=discord.Embed(
                    title="No existe",
                    description=f"El perfil con tag {tag} no existe",
                    color=discord.Color.dark_red(),
                )
            )
            return

        pd = Player.from_dict(pd_data.json())
        bws_data = requests.get(
            ROYALE_URL + f"brawlers",
            headers={"Authorization": f"Bearer {TOKEN_API}"},
        ).json()["items"]
        bws = [Brawler.from_dict(bw) for bw in bws_data]

        info = discord.Embed(
            title=f"Calificación: {rate(pd)}",
            colour=discord.Colour.from_str("#" + pd.name_color[4:]),
        )
        info.set_thumbnail(url=f"https://cdn-old.brawlify.com/profile/{pd.icon.id}.png")
        info.add_field(name=f"**{pd.name}**", value=pd.tag.upper())
        info.add_field(
            name="",
            value=f"**Club**: {pd.club.tag if pd.club else 'No'}\n**Clasificado**: {'Si' if pd.is_qualified_from_championship_challenge else 'No'}",
        )

        bests = sorted(pd.brawlers, key=operator.attrgetter("trophies"), reverse=True)
        alltime = sorted(
            pd.brawlers, key=operator.attrgetter("highest_trophies"), reverse=True
        )

        bb = bests[0]
        info.add_field(
            name=f"Mejor brawler: __**{bb.name.capitalize()}**__",
            value=f"*Trofeos*: {bb.trophies:,} ·|· *Power*: {bb.power}\n*Mejores*: {bb.highest_trophies:,} ·|· *Rango*: {bb.rank}",
            inline=False,
        )

        info.add_field(
            name="",
            value=f"**3vs3**: {pd.the_3_vs3_victories:,}\n**Solo**: {pd.solo_victories:,}\n**Duo**: {pd.duo_victories:,}",
        )
        info.add_field(
            name="",
            value=f"**Actual**: {pd.trophies:,}\n**Máximo**: {pd.highest_trophies:,}\n**Brawlers**: {len(pd.brawlers)} / {len(bws)}",
        )

        tops = discord.Embed(
            colour=discord.Colour.from_str("#" + pd.name_color[4:]),
        )

        actual_top = "\n".join(
            [
                f"{i+1}. [{bws.power:2}] - {bws.trophies:,^3} || **{bws.name}**"
                for i, bws in enumerate(bests)
                if i < 10
            ]
        )
        best_top = "\n".join(
            [
                f"{i+1}. [{bws.power:2}] - {bws.highest_trophies:,^3} || **{bws.name}**"
                for i, bws in enumerate(alltime)
                if i < 10
            ]
        )
        tops.add_field(name="Top 10 Copas Actuales", value=actual_top)
        tops.add_field(name="Top 10 Mejores Copas", value=best_top)

        await interaction.followup.send(embeds=[info, tops])

    @app_commands.command(description="Ve los brawlers de otra persona")
    @app_commands.describe(
        tag="Intresa el tag",
        estatus="Seleciona si quieres ver los mejores brawlers actuales o de trofeos más altos",
    )
    @app_commands.choices(
        estatus=[
            app_commands.Choice(name="Brawlers Actuales", value="act"),
            app_commands.Choice(name="Trofeos más altos", value="tma"),
        ]
    )
    @in_club()
    async def vbrawlers(
        self,
        interaction: discord.Interaction,
        tag: str,
        estatus: Optional[app_commands.Choice[str]],
    ):
        await interaction.response.defer()
        if not estatus:
            estatus = app_commands.Choice(name="Brawlers Actuales", value="act")
        if tag[0] == "#":
            tag = tag[1:]
        pd_data = requests.get(
            ROYALE_URL + f"players/%23{tag[1:]}",
            headers={"Authorization": f"Bearer {TOKEN_API}"},
        )

        if pd_data.status_code != 200:
            await interaction.followup.send(
                embed=discord.Embed(
                    title="No existe",
                    description=f"El perfil con tag {tag} no existe",
                    color=discord.Color.dark_red(),
                )
            )
            return

        pd = Player.from_dict(pd_data.json())
        bws = pd.brawlers
        bws.sort(key=lambda x: x.trophies if estatus.value == "act" else x.highest_trophies, reverse=True)  # type: ignore
        bws_data = [
            Brawler.from_dict(b)
            for b in requests.get(
                ROYALE_URL + f"brawlers",
                headers={"Authorization": f"Bearer {TOKEN_API}"},
            ).json()["items"]
        ]

        color = discord.Colour.from_str("#" + pd.name_color[4:])

        info = discord.Embed(
            title=pd.name,
            description=f"**TOP {estatus.name.upper()}**",
            colour=color,
        )

        brawls = discord.Embed(colour=color)
        for i, bw in enumerate(bws[:16]):
            bw_data = next((br for br in bws_data if br.name == bw.name))
            refuerzos = (
                "\n".join([f"{gear.name.name.replace('_','')}" for gear in bw.gears])
                if bw.gears
                else None
            )
            leyenda = (
                "**Mejores Trofeos**: "
                if estatus.value == "act"
                else "**Trofeos Actuales**: "
            )
            brawls.add_field(
                name=f"[{bw.power}] - {bw.trophies if estatus.value == 'act' else bw.highest_trophies} || **{bw.name}**",
                value=leyenda
                + f"{bw.highest_trophies if estatus.value == 'act' else bw.trophies:,} [{bw.rank:2}]\n**Estelares**: {len(bw.star_powers if bw.star_powers else []):2}/{len(bw_data.star_powers if bw_data.star_powers else []):2}\n**Gadgets**: {len(bw.gadgets if bw.gadgets else []):2}/{len(bw_data.gadgets if bw_data.gadgets else []):2}\n**Refuerzos**: {len(bw.gears if bw.gears else []):2}\n{refuerzos if refuerzos else '*Sin refuerzos*'}\n\u200B",
            )

            if i % 2 == 0:
                brawls.add_field(name="", value="")
        await interaction.followup.send(embeds=[info, brawls])

    @app_commands.command(description="Ve el historial de otra persona")
    @app_commands.describe(tag="Intresa el tag")
    @in_club()
    async def vhistorial(self, interaction: discord.Interaction, tag: str):
        await interaction.response.defer()
        if tag[0] == "#":
            tag = tag[1:]
        pd_data = requests.get(
            ROYALE_URL + f"players/%23{tag[1:]}",
            headers={"Authorization": f"Bearer {TOKEN_API}"},
        )

        if pd_data.status_code != 200:
            await interaction.followup.send(
                embed=discord.Embed(
                    title="No existe",
                    description=f"El perfil con tag {tag} no existe",
                    color=discord.Color.dark_red(),
                )
            )
            return

        pd = Player.from_dict(pd_data.json())
        bl_data = requests.get(
            ROYALE_URL + f"players/%23{tag}/battlelog",
            headers={"Authorization": f"Bearer {TOKEN_API}"},
        ).json()["items"]
        bl = [BattleLog.from_dict(bt) for bt in bl_data]

        color = discord.Colour.from_str("#" + pd.name_color[4:])

        info = discord.Embed(
            title=pd.name, description="**HISTORIAL DE BATALLAS**", colour=color
        )
        battles = [info]
        for battle_data in bl[:7]:
            title, data = "", ""
            battle = battle_data.battle
            event = battle_data.event

            fecha = f"{battle_data.battle_time[6:8]} {calendar.month_name[int(battle_data.battle_time[4:6])]}"
            result = battle.result.name if battle.result else f"RANGO: {battle.rank}"
            trophyChange = battle.trophy_change if battle.trophy_change else 0

            mode = battle.mode.name.replace("_", " ")
            mapa = traductor.translate(event.map) if event.map else None
            tipo = battle.type.name.replace("_", " ") if mapa else "Amistosa"
            duration = battle.duration / 60 if battle.duration else 0

            if result == "GANADA" or trophyChange > 0:
                color = "#2ECC71"
            elif result == "PERDIDA" or trophyChange < 0:
                color = "#E74C3C"
            elif result == "EMPATE" or trophyChange == 0:
                color = "#FEE75C"
            else:
                color = "#" + pd.name_color[4:]

            embed = discord.Embed(colour=discord.Colour.from_str(color))
            starPlayer = battle.star_player if battle.star_player else None
            if starPlayer:
                starPlayer = f"\n★ **MVP**: __{starPlayer.name}__ - {starPlayer.brawler.name} [{starPlayer.brawler.power}]"

            title += f"{fecha} || {result}"
            if tipo == "Normal" and mapa:
                title += f" | Trofeos: {trophyChange}"

            data += f"Modo: {mode} | Tipo: {tipo}\n"
            data += f"Mapa: {mapa}" if mapa else ""

            if battle.duration:
                data += (
                    f" | Duración: {duration:.2f} mins"
                    if mapa
                    else f"Duración: {duration:.2f} mins"
                )
            data += starPlayer if starPlayer else ""
            data += "\n" + "-·-" * 17

            embed.add_field(name=title, value=data, inline=False)

            teams = (
                battle.teams
                if battle.teams
                else battle.players
                if battle.players
                else []
            )

            for i, team in enumerate(teams):
                if isinstance(team, list):
                    normal_match = False
                    blue_team, red_team = "", ""
                    for j, player in enumerate(team):
                        data = f"**__{player.name}__**\n[{player.brawler.power}] - {player.brawler.trophies:,} | {player.brawler.name}\n"

                        if len(team) == 2:
                            if j == 1:
                                blue_team += data
                            else:
                                red_team += data
                        else:
                            normal_match = True
                            if i == 1:
                                blue_team += data
                            else:
                                red_team += data
                    if blue_team:
                        embed.add_field(
                            name="**》 EQUIPO AZUL**" if normal_match else "",
                            value=blue_team,
                        )
                    if not normal_match:
                        embed.add_field(name="-", value="")
                    if red_team:
                        embed.add_field(
                            name="**》 EQUIPO ROJO**" if normal_match else "",
                            value=red_team,
                        )
                else:
                    embed.add_field(
                        name="",
                        value=f"**__{team.name}__**\n[{team.brawler.power}] - {team.brawler.trophies:,} | {team.brawler.name}",
                    )
                    if i % 2 == 0:
                        embed.add_field(name="", value="")
            battles.append(embed)

        await interaction.followup.send(embeds=battles)


async def setup(bot):
    await bot.add_cog(Buscar(bot))
