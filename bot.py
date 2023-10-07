import asyncio
import discord
import logging
import logging.handlers
import os
import json
import time
import platform

from dotenv import  load_dotenv

from views.Ticket import *
from views.ReactionRoles import *
from cogs.ServerHub import *

from colorama import Back, Fore, Style
from discord.ext import commands

# Get the start time 
startTime = time.time()

# Fetch configuration datas
with open('config.json', 'r') as f:
    config = json.load(f)
    
load_dotenv()
dpyToken = os.getenv('dpyToken')
    
# Fetch application datas
with open('prodInfo.json', 'r') as f:
    prodInfo = json.load(f)
    
    
# Discord Logging Setup before Discord Connection
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)
        
class Main(commands.AutoShardedBot):
    def __init__(self) -> None:
        super().__init__(command_prefix=commands.when_mentioned_or(config['prefix']), intents=discord.Intents.all(), case_insensitive=True)
        self.added = False
        self.remove_command("help")
        
    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await bot.load_extension(f'cogs.{filename[:-3]}')
                    print('─' * 70)
                    print(f'{filename[:-3]} has been loaded with no errors.')
                    print('─' * 70)
                except Exception as e:
                    print('Failed to load extension {}\n{}: {}'.format(
                        filename    , type(e).__name__, e))
                    
    async def on_ready(self):
        if not self.added:
            self.add_view(StarupSettings())
            self.add_view(startHub())
            self.add_view(ticketSetup())
            self.add_view(ProfileBuilder())
            self.added = True
        
        endTime = time.time()
        bootTime = endTime - startTime
        
        dpyVersion = discord.__version__
        pythonVersion = platform.python_version()
        prefix = (Style.BRIGHT + Back.BLACK + Fore.GREEN + '[' + time.strftime("%H:%M:%S", time.gmtime()) + ']' + Back.RESET + Fore.WHITE + Style.BRIGHT)
        
        activity = discord.Activity(type=discord.ActivityType.listening, name=f"{config['prefix']}help | FTG")
        await self.change_presence(activity=activity)

        
        print('─' * 70)
        print(prefix + ' It took {:.2f}s to launch the program'.format(bootTime))
        print('─' * 70)
        print(prefix + f' Operating on Python {pythonVersion}')
        print(prefix + f' Running: discord v{dpyVersion}')
        print('─' * 70)
        print(prefix + f' Username: {bot.user}')
        print(prefix + f' ID: {bot.user.id}')
        print('─' * 70)
        
bot = Main()

pid = os.getpid()

bot.run(dpyToken)