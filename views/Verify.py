import asyncio
import discord

from discord.ext import commands

class Verify(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Verify", style=discord.ButtonStyle.blurple, custom_id="verify:blurple")
    async def verify(self, interaction: discord.Interaction, button: discord.Button):
        unverified_id = 1146684980563558440
        verified_id = 1145298592173662269
        defaults_id = 1145298529183604778

        embedVerified = discord.Embed(description="Great! You have been verified.\n\nYou can now start talking to other members.", color=0x00ff00)
        channel = interaction.channel
        user = interaction.user
        verified = discord.utils.get(user.guild.roles, id=verified_id)
        defaults = discord.utils.get(user.guild.roles, id=defaults_id)
        unverified = discord.utils.get(user.guild.roles, id=unverified_id)
        
        await user.remove_roles(unverified)
        await user.add_roles(verified)
        await user.add_roles(defaults)
        await interaction.response.send_message(embed=embedVerified, ephemeral=True)
