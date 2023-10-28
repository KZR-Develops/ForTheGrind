import discord
import platform
import time

from colorama import Back, Fore, Style
from discord.ext import commands


class EventsHandler(commands.Cog):
<<<<<<< HEAD
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.prefix = (
            Style.BRIGHT
            + Back.BLACK
            + Fore.GREEN
            + "["
            + time.strftime("%H:%M:%S", time.gmtime())
            + "]"
            + Back.RESET
            + Fore.WHITE
            + Style.BRIGHT
        )

    @commands.Cog.listener()
    async def on_connect(self):
        print("─" * 70)
        print(f"{self.prefix} The client has successfully connected to Discord.")
        print("─" * 70)

    @commands.Cog.listener()
    async def on_resume(self):
        print("─" * 70)
        print(f"{self.prefix} The client has resume its session to Discord.")
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
=======
    def __init__(self, bot:commands.Bot):
        self.bot = bot

        self.prefix = (Style.BRIGHT + Back.BLACK + Fore.GREEN + '[' + time.strftime("%H:%M:%S", time.gmtime()) + ']' + Back.RESET + Fore.WHITE + Style.BRIGHT)

    @commands.Cog.listener()
    async def on_connect(self):

        print('─' * 70)
        print(f'{self.prefix} The client has successfully connected to Discord.')
        print('─' * 70)

    @commands.Cog.listener()
    async def on_resume(self):

        print('─' * 70)
        print(f'{self.prefix} The client has resume its session to Discord.')
        print('─' * 70)


async def setup(bot:commands.Bot):
    await bot.add_cog(EventsHandler(bot))
>>>>>>> e200e1035f2a61a8df79874c40551ca6c26cbd3d
