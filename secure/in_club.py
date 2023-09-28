import discord
from discord import app_commands

from connections import BrawlStars


def in_club():
    members_data = BrawlStars().get_club_members("#2JUCPV8PR")

    def predicate(interaction: discord.Interaction):
        nick = interaction.user.nick  # type: ignore

        return (
            True if nick and nick in [member.name for member in members_data] else False
        )

    return app_commands.check(predicate)
