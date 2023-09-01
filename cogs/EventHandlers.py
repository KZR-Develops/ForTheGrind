import discord
import platform
import time

from colorama import Back, Fore, Style
from discord.ext import commands


class EventsHandler(commands.Cog):
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