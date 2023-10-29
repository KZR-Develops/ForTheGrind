import discord
import platform
import time

from colorama import Back, Fore, Style
from discord.ext import commands


class EventsHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(self):
        print("─" * 70)
        print(f"[DISCORD] The client has successfully connected to Discord.")
        print("─" * 70)

    @commands.Cog.listener()
    async def on_resume(self):
        print("─" * 70)
        print(f"[DISCORD] The client has resume its session to Discord.")
        print("─" * 70)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        role_id = 1146684980563558440  # Replace with the actual role ID

        role = discord.utils.get(guild.roles, id=role_id)
        await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if not before.premium_since and after.premium_since:
            # The user has just boosted the server
            special_role = discord.utils.get(after.guild.roles, id=1134472266890092607)
            if special_role:
                await after.add_roles(special_role)

async def setup(bot: commands.Bot):
    await bot.add_cog(EventsHandler(bot))
