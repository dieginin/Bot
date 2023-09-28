import calendar
import operator
from typing import Optional

import discord
from deep_translator import GoogleTranslator
from discord import app_commands
from discord.ext import commands

from connections import BrawlApi, BrawlStars
from functions import get_member, km_format
from models import Role
from secure import in_club

traductor = GoogleTranslator(source="en", target="es")


class Stats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    club_members = BrawlStars().get_club_members("2JUCPV8PR")

    @app_commands.command(name="club", description="Estadísticas del club")
    @app_commands.describe(tag="Intresa el tag")
    @in_club()
    async def club(self, interaction: discord.Interaction, tag: str | None = None):
        await interaction.response.defer()
        tag = tag if tag else "#2JUCPV8PR"  # type: ignore
        tag = tag.upper()

        bs = BrawlStars()
        club = bs.get_club(tag)

        info = discord.Embed(
            title=f"<:club:1156722302147362856> {club.name} |\u2573| *{club.tag}*",
            description=club.description,
            color=discord.Color.green(),
        )
        info.set_thumbnail(url=f"https://cdn-old.brawlify.com/club/{club.badge_id}.png")
        info.add_field(
            name="Trofeos", value=f"<:trofeos:1156818585151361034> {club.trophies:,}"
        )
        info.add_field(
            name="Miembros", value=f"<:members:1157045953019265134> {club.member_count}"
        )

        mems1 = "\n".join(
            [
                f"{i+1}. [{km_format(club.members[i].trophies):6}]  {club.members[i].name:30}"
                for i in range(15)
            ]
        )
        mems2 = "\n".join(
            [
                f"{i+1}. [{km_format(club.members[i].trophies):6}]  {club.members[i].name:30}"
                for i in range(15, club.member_count)
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
        info.add_field(name="", value="", inline=False)
        info.add_field(name="Vice Presidentes", value=colideres)
        info.add_field(name="Veteranos", value=veteranos)

        miembros = discord.Embed(title="Miembros", color=discord.Color.dark_green())
        miembros.add_field(name="", value=mems1)
        miembros.add_field(name="", value="\u200B")
        miembros.add_field(name="", value=mems2)

        await interaction.followup.send(embeds=[info, miembros])

    @app_commands.command(
        name="perfil",
        description="Obten tus estadísticas, de un miembro o de alguna persona con su tag",
    )
    @app_commands.describe(
        grupo_1="Grupo 1 pertenece a los primero 15",
        grupo_2="Grupo 2 pertenece a partir de los 15",
        tag="Ingresa el tag de la persona (#000000)",
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
        tag: Optional[str],
    ):
        await interaction.response.defer()

        member_tag = get_member(interaction.user.nick).tag if not (grupo_1 or grupo_2) else (grupo_1.value if grupo_1 else (grupo_2.value if grupo_2 else app_commands.Choice(name="", value="").value))  # type: ignore
        tag = tag if tag else member_tag
        tag = tag.upper()

        bs = BrawlStars()

        pd = bs.get_player(tag)
        bwsd = bs.get_brawlers()
        bws = sorted(pd.brawlers, key=operator.attrgetter("trophies"), reverse=True)

        info = discord.Embed(
            colour=discord.Colour.from_str("#" + pd.name_color[4:]),
        )
        info.set_thumbnail(url=f"https://cdn-old.brawlify.com/profile/{pd.icon.id}.png")
        info.add_field(
            name="",
            value="<:champion:1156649552619778058> "
            + ("**Clasificado**" if pd.is_qualified else "**No clasificado**"),
            inline=False,
        )
        info.add_field(
            name="",
            value=f"<:calif:1156756804215259176> **Calificación: {pd.grade}**",
            inline=False,
        )
        info.add_field(name=f"**{pd.name}**", value=pd.tag)
        clumoji = (
            "<:club:1156722302147362856>"
            if pd.club
            else "<:noclub:1156723454083616879>"
        )
        info.add_field(
            name="",
            value=f"{clumoji} {f'**{pd.club.name}**' if pd.club else '_Sin club_'}\n{pd.club.tag if pd.club else ''}",
        )
        b11 = len(pd.brawlers_11)
        b10 = len(pd.brawlers_10)
        b09 = len(pd.brawlers_9)
        sum = b09 + b10 + b11
        v = "<:power:1156764348887351326> **Niveles de Fuerza**\n"
        if sum != pd.brawlers_count:
            v += f"**P. 11**: {b11} -|·|- **P. 10**: {b10} -|·|- **P. 9**: {b09}"
        else:
            if b11 > 0:
                v += f"**P. 11**: {b11} -|·|- "

            if b10 > 0:
                v += f"**P. 10**: {b10} -|·|- "

            if b09 > 0:
                v += f"**P. 9**: {b09}"
            else:
                if v[-6:] == "-|·|- ":
                    v = v[:-6]

        info.add_field(
            name="",
            value=v,
            inline=False,
        )
        info.add_field(
            name="",
            value=f"<:match:1156758036220747787> **3vs3**: {pd.the_3_vs3_victories:,}\n<:solo:1156758468460564490> **Solo**: {pd.solo_victories:,}\n<:duo:1156758660140241017> **Duo**: {pd.duo_victories:,}",
        )
        info.add_field(
            name="",
            value=f"<:player:1156654955101425785> **Actual**: {pd.trophies:,}\n<:tiemp:1156757515724402748> **Máximo**: {pd.highest_trophies:,}\n<:bstars:1156765791501434888> **Brawlers**: {pd.brawlers_count} / {len(bwsd)}",
        )

        brawls = discord.Embed(colour=discord.Colour.from_str("#" + pd.name_color[4:]))

        for b in bws[: min(24, pd.brawlers_count)]:
            name = b.name.replace("-", "").replace(".", "").replace(" ", "").lower()

            emoji = discord.utils.get(self.bot.emojis, name=name)
            emoji = emoji if emoji else name.upper()[:2]

            brawls.add_field(name="", value=f"{emoji} {b.power} | `{b.trophies:,}` ")

        # Trophy Progression
        # :OR: today: +0
        # :AD: this week: -440
        # :AD: this season: -408
        # TODO agrgrar embed que haga eso
        # https://discord.com/channels/1148467971442876416/1149400297278554293/1156462529069985812

        await interaction.followup.send(embeds=[info, brawls])

    @app_commands.command(
        name="brawlers",
        description="Tus mejores brawlers actuales y de trofeos más altos o los de otro miembro",
    )
    @app_commands.describe(
        estatus="Seleciona si quieres ver los mejores brawlers actuales o de trofeos más altos",
        grupo_1="Grupo 1 pertenece a los primero 15",
        grupo_2="Grupo 2 pertenece a partir de los 15",
        tag="Ingresa el tag de la persona (#000000)",
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
        tag: Optional[str],
    ):
        await interaction.response.defer()

        if not estatus:
            estatus = app_commands.Choice(name="Brawlers Actuales", value="act")
        member_tag = get_member(interaction.user.nick).tag if not (grupo_1 or grupo_2) else (grupo_1.value if grupo_1 else (grupo_2.value if grupo_2 else app_commands.Choice(name="", value="").value))  # type: ignore
        tag = tag if tag else member_tag
        tag = tag.upper()
        bs = BrawlStars()
        ba = BrawlApi()

        pd = bs.get_player(tag)
        bws = pd.brawlers
        bws.sort(key=lambda x: x.trophies if estatus.value == "act" else x.highest_trophies, reverse=True)  # type: ignore
        bws_data = ba.get_brawlers()

        color = discord.Colour.from_str("#" + pd.name_color[4:])

        info = discord.Embed(
            title=pd.name,
            description=f"**TOP {estatus.name.upper()}**",
            colour=color,
        )

        brawls = discord.Embed(colour=color)
        for bw in bws[:21]:
            bw_data = next(
                (b for b in bws_data if b.name.lower() == bw.name.lower()), None
            )
            name = bw.name.replace("-", "").replace(".", "").replace(" ", "").lower()

            emoji = discord.utils.get(self.bot.emojis, name=name)
            emoji = emoji if emoji else name.upper()[:2]

            refuerzos = (
                "\n".join([f"{gear.name.name.replace('_',' ')}" for gear in bw.gears])
                if bw.gears
                else None
            )
            leyenda = "**Mejores**:" if estatus.value == "act" else "**Actuales**:"

            brawls.add_field(
                name=f"{emoji} {bw.power} | `{bw.trophies if estatus.value == 'act' else bw.highest_trophies:,}` ",
                value=f"<:trofeos:1156818585151361034> {leyenda} {bw.highest_trophies if estatus.value == 'act' else bw.trophies:,}\n<:estelares:1156818405538680892> **Estelares**: {len(bw.star_powers if bw.star_powers else []):2}/{len(bw_data.star_powers if bw_data else []):2}\n<:gadgets:1156818840194383942> **Gadgets**: {len(bw.gadgets if bw.gadgets else []):2}/{len(bw_data.gadgets if bw_data else []):2}\n<:refuerzos:1156819292185174097> **Refuerzos**: {len(bw.gears if bw.gears else []):2}\n{refuerzos if refuerzos else '*Sin refuerzos*'}\n\u200B",
            )

        await interaction.followup.send(embeds=[info, brawls])

    @app_commands.command(
        name="historial",
        description="Tu historial de batallas de otro miembro",
    )
    @app_commands.describe(
        grupo_1="Grupo 1 pertenece a los primero 15",
        grupo_2="Grupo 2 pertenece a partir de los 15",
        tag="Ingresa el tag de la persona (#000000)",
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
        tag: Optional[str],
    ):
        await interaction.response.defer()

        member_tag = get_member(interaction.user.nick).tag if not (grupo_1 or grupo_2) else (grupo_1.value if grupo_1 else (grupo_2.value if grupo_2 else app_commands.Choice(name="", value="").value))  # type: ignore
        tag = tag if tag else member_tag
        tag = tag.upper()

        bs = BrawlStars()

        pd = bs.get_player(tag)
        bl = bs.get_battlelog(tag)

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

    # @commands.command()
    # async def t(self, ctx: commands.Context):
    #     seer_role = discord.utils.get(ctx.guild.roles, name="The Seer")
    #     admin_role = discord.utils.get(ctx.guild.roles, name="Admin")

    #     if seer_role is None or admin_role is None:
    #         return await ctx.send('No se encontraron los roles "The Seer" o "Admin".')

    #     # Crea la colección de roles
    #     roles_collection = [seer_role, admin_role]

    #     name = "members"

    #     response = requests.get(
    #         "https://cdn.discordapp.com/emojis/1081421351203643432.png"
    #     )

    #     emoji = await ctx.guild.create_custom_emoji(
    #         name=name, image=response.content, roles=roles_collection
    #     )
    #     await ctx.send(f"<{name}    {emoji.id}>")

    # @commands.command(
    #     name="t"
    # )
    # async def t(
    #     self,
    #     ctx: commands.Context,
    #     tag: Optional[str],
    # ):
    #     bs = BrawlApi()
    #     # ifnot tag get member by name
    #     if not tag: tag = '#1'
    #     bd = bs.get_brawlers()

    #     seer_role = discord.utils.get(ctx.guild.roles, name='The Seer')
    #     admin_role = discord.utils.get(ctx.guild.roles, name='Admin')

    #     if seer_role is None or admin_role is None:
    #         return await ctx.send('No se encontraron los roles "The Seer" o "Admin".')

    #     # Crea la colección de roles
    #     roles_collection = [seer_role, admin_role]

    #     for b in bd:
    #         name = b.name.replace("-","").replace(".","").replace(" ","").lower()
    #         # name = name.split()
    #         # if len(name) == 1:
    #         #     name = name[0][:2]
    #         # else:
    #         #     name = name[0][0] + name[1][0]
    #         emoji = discord.utils.get(ctx.guild.emojis, name=name)
    #         if emoji:
    #             await ctx.send(f'<:{name}:{emoji.id}>')
    #             continue

    #         response = requests.get(b.image_url)
    #         by = BytesIO(response.content)
    #         bytes = by.getvalue()
    #         try:
    #             emoji = await ctx.guild.create_custom_emoji(name=name, image=bytes, roles=roles_collection)
    #             await ctx.send(f'<:{name}:{emoji.id}>')
    #         except:
    #             await ctx.send(f'pedo con: {name}')

    #     await ctx.send('ya')


async def setup(bot):
    await bot.add_cog(Stats(bot))
