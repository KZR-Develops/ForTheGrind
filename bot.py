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
    
    
# Define log file path and log file retention period
log_file = 'discord.log'
log_retention_period = 7  # 7 days

# Create a custom date format
dt_fmt = '%m/%d/%y @ %I:%M %p'

# Create a logger with INFO level
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

# Create a RotatingFileHandler for logging
handler = logging.handlers.TimedRotatingFileHandler(
    log_file,
    when='D',  # Daily rotation
    interval=1,  # Rotate every day
    backupCount=log_retention_period  # Keep logs for 7 days
)

# Create a custom formatter
formatter = logging.Formatter('[{asctime}] [{levelname}]: {message}', dt_fmt, style='{')

# Set the formatter for the handler
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)


class Main(commands.AutoShardedBot):
    def __init__(self) -> None:
        super().__init__(command_prefix=commands.when_mentioned_or(config['prefix']), intents=discord.Intents.all(), case_insensitive=True)
        self.added = False
        self.remove_command("help")

    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print('─' * 70)
        print(f"Node URI: {node.uri}")
        print(f"Node ID: {node.id}")
        print(f"Node Ping: {node.heartbeat}ms")
        print(f"Node Status: {node.status.name}")
        print('─' * 70)

    async def setup_hook(self):
        # Wavelink 2.0 has made connecting Nodes easier... Simply create each Node
        # and pass it to NodePool.connect with the client/bot.
        print('─' * 70)
        print("[WAVELINK] Initiating connection to lavalink nodes...")
        print('─' * 70)
        try:
            node1: wavelink.Node = wavelink.Node(uri='lava1.horizxon.tech:443', password='horizxon.tech', secure=True)
            node2: wavelink.Node = wavelink.Node(uri='lava2.horizxon.tech:443', password='horizxon.tech', secure=True)
            node3: wavelink.Node = wavelink.Node(uri='lava3.horizxon.tech:443', password='horizxon.tech', secure=True)
            await wavelink.NodePool.connect(client=bot, nodes=[node1, node2, node3])
            print('─' * 70)
            print("[WAVELINK] Successfuly connected to lavalink nodes!")
            print('─' * 70)
        except ConnectionError:
            print('─' * 70)
            print("[WAVELINK] Error while initiating a connection between the nodes.")
            print('─' * 70)

        await asyncio.sleep(3)
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await asyncio.sleep(2)
                try:
                    await bot.load_extension(f'cogs.{filename[:-3]}')
                    print('─' * 70)
                    print(f'[EXTENSIONS] {filename[:-3]} has been loaded with no errors.')
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
        
        activity = discord.Activity(type=discord.ActivityType.listening, name=f"{config['prefix']}help | FTG")
        await self.change_presence(activity=activity)

        art = r'''
__/\\\\\\\\\\\\\\\_        __/\\\\\\\\\\\\\\\_        _____/\\\\\\\\\\\\_        
 _\/\\\///////////__        _\///////\\\/////__        ___/\\\//////////__       
  _\/\\\_____________        _______\/\\\_______        __/\\\_____________      
   _\/\\\\\\\\\\\_____        _______\/\\\_______        _\/\\\____/\\\\\\\_     
    _\/\\\///////______        _______\/\\\_______        _\/\\\___\/////\\\_    
     _\/\\\_____________        _______\/\\\_______        _\/\\\_______\/\\\_   
      _\/\\\_____________        _______\/\\\_______        _\/\\\_______\/\\\_  
       _\/\\\_____________        _______\/\\\_______        _\//\\\\\\\\\\\\/__ 
        _\///______________        _______\///________        __\////////////____
'''
        print('─' * 70)
        print(art)
        print('─' * 70)
        print(' Boot Time: {:.2f}s to launch the program'.format(bootTime))
        pid = os.getpid()
        print(f" Running On PID: {pid}")
        print('─' * 70)
        print(f' Operating on Python {pythonVersion}')
        print(f' Running: discord v{dpyVersion}')
        print('─' * 70)
        print(f' Username: {bot.user}')
        print(f' UserID: {bot.user.id}')
        print('─' * 70)
        


if __name__ == "__main__":
    try:
        bot = Main()
        set_boot_time()
        bot.run(dpyToken)
    except Exception as error:
        print(f"An error has occured: {error}")