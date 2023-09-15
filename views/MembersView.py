import discord

from views.MembersDropdown import MembersDropdown

class MembersView(discord.ui.View):
    def __init__(self, grupo, timeout = 10):
        super().__init__(timeout=timeout)
        self.add_item(MembersDropdown(grupo))
