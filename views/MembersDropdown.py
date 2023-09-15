import discord
import requests
from dotenv import dotenv_values

settings = dotenv_values()
brawlAPI = 'https://bsproxy.royaleapi.dev/v1/'

class MembersDropdown(discord.ui.Select):
    def __init__(self, grupo):
        options = []
        data = requests.get(brawlAPI + 'clubs/%232JUCPV8PR', headers={"Authorization": f"Bearer {settings['BRAWL_API']}"}).json()
        members = data['members']
        
        for i, member in enumerate(members):
            if grupo == 1 and i < 15:
                options.append(discord.SelectOption(label = member['name']))
            elif grupo == 2 and i >= 15:
                options.append(discord.SelectOption(label = member['name']))
        
        super().__init__(placeholder = 'Selecciona tu perfil' , options = options)
        
    async def callback(self, interaction: discord.Interaction):
        try:
            await interaction.user.edit(nick = self.values[0]) # type: ignore
            await interaction.response.edit_message(content = self.values[0], view = None) # type: ignore
        except:
            await interaction.response.edit_message(content = f'{self.values[0]}\nNo pude cambiarte el nick.', view = None) # type: ignore
