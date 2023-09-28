from connections import BrawlStars
from models import Member


def get_member(nick: str) -> Member:
    members_data = BrawlStars().get_club_members("#2JUCPV8PR")

    member = next(member for member in members_data if member.name == nick)

    return member
