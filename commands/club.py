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
from functions.human_format import human_format
from models.BattleLog import BattleLog
from models.Brawler import Brawler
from models.Club import Club, Role
from models.Player import Player

club_members = Club.from_dict(
    requests.get(
        ROYALE_URL + "clubs/%232JUCPV8PR",
        headers={"Authorization": f"Bearer {TOKEN_API}"},
    ).json()
).members

traductor = GoogleTranslator(source="en", target="es")


class ClubCmds(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="club", description="Estadísticas del club")
    @app_commands.describe(tag="Intresa el tag")
    @in_club()
    async def club(self, interaction: discord.Interaction, tag: str | None = None):
        await interaction.response.defer()
        if tag:
            if tag[0] == "#":
                tag = tag[1:]
            club_data = requests.get(
                ROYALE_URL + f"clubs/%23{tag}",
                headers={"Authorization": f"Bearer {TOKEN_API}"},
            )

            if club_data.status_code != 200:
                await interaction.followup.send(
                    embed=discord.Embed(
                        title="No existe",
                        description=f"El club con tag {tag} no existe",
                        color=discord.Color.dark_red(),
                    )
                )

            club = Club.from_dict(club_data.json())
        else:
            club = Club.from_dict(
                requests.get(
                    ROYALE_URL + "clubs/%232JUCPV8PR",
                    headers={"Authorization": f"Bearer {TOKEN_API}"},
                ).json()
            )

        info = discord.Embed(
            title=club.name,
            description=club.description,
            color=discord.Color.green(),
        )
        info.set_thumbnail(url=f"https://cdn-old.brawlify.com/club/{club.badge_id}.png")
        info.add_field(name="Tag", value=club.tag)
        info.add_field(name="Trophies", value=f"{club.trophies:,}")
        info.add_field(name="Members", value=club.members_count)

        mems1 = "\n".join(
            [
                f"{i+1}. [{human_format(club.members[i].trophies):6}]  {club.members[i].name:30}"
                for i in range(15)
            ]
        )
        mems2 = "\n".join(
            [
                f"{i+1}. [{human_format(club.members[i].trophies):6}]  {club.members[i].name:30}"
                for i in range(15, club.members_count)
            ]
        )

        colideres = "\n".join(
            [
                f"- {member.name}"
                for member in club.members
                if member.role == Role.Vice_Presidente
            ]
        )
        veteranos = "\n".join(
            [
                f"- {member.name}"
                for member in club.members
                if member.role == Role.Veterano
            ]
        )

        info.set_author(
            name=f"Presidente: {club.president.name if club.president else ''}",
            icon_url=f"https://cdn-old.brawlify.com/profile/{club.president.icon.id if club.president else 0}.png",
        )

        info.add_field(name="Vice Presidentes", value=colideres)
        info.add_field(name="Veteranos", value=veteranos)

        miembros = discord.Embed(title="Miembros", color=discord.Color.dark_green())
        miembros.add_field(name="", value=mems1)
        miembros.add_field(name="", value="\u200B")
        miembros.add_field(name="", value=mems2)

        await interaction.followup.send(embeds=[info, miembros])

    @app_commands.command(
        name="perfil",
        description="Obten tus estadísticas o la de un miembro",
    )
    @app_commands.describe(
        grupo_1="Grupo 1 pertenece a los primero 15",
        grupo_2="Grupo 2 pertenece a partir de los 15",
    )
    @app_commands.choices(
        grupo_1=[
            app_commands.Choice(name=member.name, value=member.tag)
            for member in club_members[:15]
        ],
        grupo_2=[
            app_commands.Choice(name=member.name, value=member.tag)
            for member in club_members[15:]
        ],
    )
    @in_club()
    async def perfil(
        self,
        interaction: discord.Interaction,
        grupo_1: Optional[app_commands.Choice[str]],
        grupo_2: Optional[app_commands.Choice[str]],
    ):
        await interaction.response.defer()

        if not (grupo_1 or grupo_2):
            tag, _ = get_member_info(interaction.user.nick)  # type: ignore
            member = app_commands.Choice(name=interaction.user.nick, value=tag)  # type: ignore
        else:
            member = grupo_1 if grupo_1 else grupo_2

        if member:
            tag, role = get_member_info(member.name)

            pd = Player.from_dict(
                requests.get(
                    ROYALE_URL + f"players/%23{member.value[1:]}",
                    headers={"Authorization": f"Bearer {TOKEN_API}"},
                ).json()
            )
            bl_data = requests.get(
                ROYALE_URL + f"players/%23{member.value[1:]}/battlelog",
                headers={"Authorization": f"Bearer {TOKEN_API}"},
            ).json()["items"]
            bl = [BattleLog.from_dict(bt) for bt in bl_data]
            bws_data = requests.get(
                ROYALE_URL + f"brawlers",
                headers={"Authorization": f"Bearer {TOKEN_API}"},
            ).json()["items"]
            bws = [Brawler.from_dict(bw) for bw in bws_data]

            info = discord.Embed(
                colour=discord.Colour.from_str("#" + pd.name_color[4:]),
            )
            info.set_thumbnail(
                url=f"https://cdn-old.brawlify.com/profile/{pd.icon.id}.png"
            )
            info.add_field(name=f"**{pd.name}**", value=pd.tag)
            info.add_field(
                name="",
                value=f"**Posición**: {role.name.replace('_',' ')}\n**Clasificado**: {'Si' if pd.is_qualified_from_championship_challenge else 'No'}",
            )

            bests = sorted(
                pd.brawlers, key=operator.attrgetter("trophies"), reverse=True
            )
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
                title="**BRAWLERS**",
                colour=discord.Colour.from_str("#" + pd.name_color[4:]),
            )

            actual_top = "\n".join(
                [
                    f"{i+1}. [{bws.power:2}] - {bws.trophies:,^3} || **{bws.name}**"
                    for i, bws in enumerate(bests)
                    if i < 15
                ]
            )
            best_top = "\n".join(
                [
                    f"{i+1}. [{bws.power:2}] - {bws.highest_trophies:,^3} || **{bws.name}**"
                    for i, bws in enumerate(alltime)
                    if i < 15
                ]
            )
            tops.add_field(name="Top 15 Copas Actuales", value=actual_top)
            tops.add_field(name="Top 15 Mejores Copas", value=best_top)

            blh = discord.Embed(
                title="**HISTORIAL DE BATALLAS**",
                colour=discord.Colour.from_str("#" + pd.name_color[4:]),
            )
            for i, battle_data in enumerate(bl[:3]):
                title, data = "", ""
                battle = battle_data.battle
                event = battle_data.event

                fecha = f"{battle_data.battle_time[6:8]} {calendar.month_name[int(battle_data.battle_time[4:6])]}"
                result = (
                    battle.result.name if battle.result else f"RANGO: {battle.rank}"
                )
                trophyChange = battle.trophy_change if battle.trophy_change else 0

                mode = battle.mode.name.replace("_", " ")
                mapa = traductor.translate(event.map) if event.map else None
                tipo = battle.type.name.replace("_", " ") if mapa else "Amistosa"
                duration = battle.duration / 60 if battle.duration else 0

                starPlayer = battle.star_player if battle.star_player else None
                if starPlayer:
                    starPlayer = f"\n★ **MVP**: __{starPlayer.name}__ - {starPlayer.brawler.name} [{starPlayer.brawler.power}]"

                if i > 0:
                    title = "\n\u200B\n" + title
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

                player = None
                teams = (
                    battle.teams
                    if battle.teams
                    else battle.players
                    if battle.players
                    else []
                )

                for team in teams:
                    for team in teams:
                        if isinstance(team, list):
                            player_data = next(
                                (p for p in team if p.name == pd.name), None
                            )
                        else:
                            player_data = (
                                team if team.name == pd.name == pd.name else None
                            )
                        if player_data:
                            player = f"**{player_data.name}** --> [{player_data.brawler.power}] - {player_data.brawler.trophies:,} || {player_data.brawler.name}"
                    if player:
                        data += f"\n{player}"
                        break

                blh.add_field(name=title, value=data, inline=False)

            await interaction.followup.send(embeds=[info, tops, blh])

    @app_commands.command(
        name="brawlers",
        description="Tus mejores brawlers actuales y de trofeos más altos o los de otro miembro",
    )
    @app_commands.describe(
        estatus="Seleciona si quieres ver los mejores brawlers actuales o de trofeos más altos",
        grupo_1="Grupo 1 pertenece a los primero 15",
        grupo_2="Grupo 2 pertenece a partir de los 15",
    )
    @app_commands.choices(
        estatus=[
            app_commands.Choice(name="Brawlers Actuales", value="act"),
            app_commands.Choice(name="Trofeos más altos", value="tma"),
        ],
        grupo_1=[
            app_commands.Choice(name=member.name, value=member.tag)
            for member in club_members[:15]
        ],
        grupo_2=[
            app_commands.Choice(name=member.name, value=member.tag)
            for member in club_members[15:]
        ],
    )
    @in_club()
    async def brawlers(
        self,
        interaction: discord.Interaction,
        estatus: Optional[app_commands.Choice[str]],
        grupo_1: Optional[app_commands.Choice[str]],
        grupo_2: Optional[app_commands.Choice[str]],
    ):
        await interaction.response.defer()
        if not estatus:
            estatus = app_commands.Choice(name="Brawlers Actuales", value="act")
        if not (grupo_1 or grupo_2):
            tag, _ = get_member_info(interaction.user.nick)  # type: ignore
            member = app_commands.Choice(name=interaction.user.nick, value=tag)  # type: ignore
        else:
            member = (
                grupo_1
                if grupo_1
                else grupo_2
                if grupo_2
                else app_commands.Choice(name="", value="")
            )

        pd = Player.from_dict(
            requests.get(
                ROYALE_URL + f"players/%23{member.value[1:]}",
                headers={"Authorization": f"Bearer {TOKEN_API}"},
            ).json()
        )
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
            title=member.name,
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

    @app_commands.command(
        name="historial",
        description="Tu historial de batallas de otro miembro",
    )
    @app_commands.describe(
        grupo_1="Grupo 1 pertenece a los primero 15",
        grupo_2="Grupo 2 pertenece a partir de los 15",
    )
    @app_commands.choices(
        grupo_1=[
            app_commands.Choice(name=member.name, value=member.tag)
            for member in club_members[:15]
        ],
        grupo_2=[
            app_commands.Choice(name=member.name, value=member.tag)
            for member in club_members[15:]
        ],
    )
    @in_club()
    async def historial(
        self,
        interaction: discord.Interaction,
        grupo_1: Optional[app_commands.Choice[str]],
        grupo_2: Optional[app_commands.Choice[str]],
    ):
        await interaction.response.defer()

        if not (grupo_1 or grupo_2):
            tag, _ = get_member_info(interaction.user.nick)  # type: ignore
            member = app_commands.Choice(name=interaction.user.nick, value=tag)  # type: ignore
        else:
            member = (
                grupo_1
                if grupo_1
                else grupo_2
                if grupo_2
                else app_commands.Choice(name="", value="")
            )

        pd = Player.from_dict(
            requests.get(
                ROYALE_URL + f"players/%23{member.value[1:]}",
                headers={"Authorization": f"Bearer {TOKEN_API}"},
            ).json()
        )
        bl_data = requests.get(
            ROYALE_URL + f"players/%23{member.value[1:]}/battlelog",
            headers={"Authorization": f"Bearer {TOKEN_API}"},
        ).json()["items"]
        bl = [BattleLog.from_dict(bt) for bt in bl_data]

        color = discord.Colour.from_str("#" + pd.name_color[4:])

        info = discord.Embed(
            title=member.name, description="**HISTORIAL DE BATALLAS**", colour=color
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

    @app_commands.command(
        name="tag",
        description="Obten el tag de un miembro",
    )
    @app_commands.describe(
        grupo_1="Grupo 1 pertenece a los primero 15",
        grupo_2="Grupo 2 pertenece a partir de los 15",
    )
    @app_commands.choices(
        grupo_1=[
            app_commands.Choice(name=member.name, value=member.tag)
            for member in club_members[:15]
        ],
        grupo_2=[
            app_commands.Choice(name=member.name, value=member.tag)
            for member in club_members[15:]
        ],
    )
    @in_club()
    async def tag(
        self,
        interaction: discord.Interaction,
        grupo_1: Optional[app_commands.Choice[str]],
        grupo_2: Optional[app_commands.Choice[str]],
    ):
        await interaction.response.defer()

        if not (grupo_1 or grupo_2):
            await interaction.followup.send("Necesitas indicar la persona")
        else:
            member = (
                grupo_1
                if grupo_1
                else grupo_2
                if grupo_2
                else app_commands.Choice(name="", value="")
            )
            await interaction.followup.send(member.value)


async def setup(bot):
    await bot.add_cog(ClubCmds(bot))
