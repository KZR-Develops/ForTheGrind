import discord
import logging
import logging.handlers
import os
import json
import time
import platform
import wavelink

from dotenv import  load_dotenv

from views.Ticket import *
from views.ReactionRoles import *
from cogs.ServerHub import *

from colorama import Back, Fore, Style
from discord.ext import commands
from cogs.utils.utility import set_boot_time

# Get the start time 
startTime = time.time()

# Fetch configuration datas
with open('config.json', 'r') as f:
    config = json.load(f)
    
load_dotenv(override=True)
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

    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node {node.id} is ready!")
        
    async def setup_hook(self):
        # Wavelink 2.0 has made connecting Nodes easier... Simply create each Node
        # and pass it to NodePool.connect with the client/bot.
        node: wavelink.Node = wavelink.Node(uri='lava1.horizxon.tech:443', password='horizxon.tech', secure=True)
        await wavelink.NodePool.connect(client=bot, nodes=[node])
        print("Wavelink initiated...")

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await bot.load_extension(f'cogs.{filename[:-3]}')
                    print('─' * 70)
                    print(f'{filename[:-3]} has been loaded with no errors.')
                    print('─' * 70)
                except Exception as e:
                    print('[STARTUP ERROR] Failed to load extension {}\n{}: {}'.format(filename    , type(e).__name__, e))

            
    async def on_ready(self):
        if config['Restarted'] == "True":
            devChannel = self.get_channel(1134737529443196988)
            await devChannel.send("Restart successful!")

            config['Restarted'] = "False"

            with open('./config.json', 'w') as f:
                json.dump(config, f, indent=4)

        pid = os.getpid()

        # Read the existing .env content
        with open('.env', 'r') as env_file:
            env_content = env_file.read()

        # Check if PID key already exists, update it, otherwise add a new line
        # Format the PID line with the desired format
        pid_line = f'PID="{pid}"'

        # Read the existing .env content
        with open('.env', 'r') as env_file:
            env_content = env_file.read()

        # Check if PID key already exists, update it, otherwise add a new line
        if 'PID=' in env_content:
            env_content = '\n'.join([pid_line if line.startswith('PID=') else line for line in env_content.split('\n')])
        else:
            env_content += f'\n{pid_line}'

        # Write the updated content back to .env
        with open('.env', 'w') as env_file:
            env_file.write(env_content)
        
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
        pid = os.getpid()
        print(prefix + f" On PID: {pid}")
        print('─' * 70)
        print(prefix + f' Operating on Python {pythonVersion}')
        print(prefix + f' Running: discord v{dpyVersion}')
        print('─' * 70)
        print(prefix + f' Username: {bot.user}')
        print(prefix + f' ID: {bot.user.id}')
        print('─' * 70)
        


if __name__ == "__main__":
    try:
        bot = Main()
        set_boot_time()
        bot.run(dpyToken)
    except Exception as error:
        print(f"An error has occured: {error}")