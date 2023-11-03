import sys
import aiohttp
import discord
import logging
import logging.handlers
import os
import json
import time
import platform
import wavelink

from dotenv import load_dotenv, set_key

from views.Ticket import *
from views.ReactionRoles import *
from cogs.ServerHub import *

from discord.ext import commands
from cogs.utils.utility import set_boot_time

startTime = time.time()

# Set the encoding to UTF-8
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)
sys.stderr = open(sys.stderr.fileno(), mode='w', encoding='utf8', buffering=1)

with open("config.json", "r") as f:
    config = json.load(f)

load_dotenv(override=True)
dpyToken = os.getenv("dpyToken")

with open("prodInfo.json", "r") as f:
    prodInfo = json.load(f)

log_directory = "C:/Life/Programming/ForTheGrindBot/logs"
log_file = os.path.join(log_directory, "discord.log")
log_retention_period = 7
dt_fmt = "%m/%d/%y @ %I:%M %p"

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)

handler = logging.handlers.TimedRotatingFileHandler(
    log_file, when="D", interval=1, backupCount=log_retention_period
)

formatter = logging.Formatter("[{asctime}] [{levelname}]: {message}", dt_fmt, style="{")
handler.setFormatter(formatter)
logger.addHandler(handler)


class Main(commands.AutoShardedBot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or(config["prefix"]),
            intents=discord.Intents.all(),
            case_insensitive=True,
        )
        self.added = False
        self.remove_command("help")
        self.nodes = []

    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print("─" * 70)
        print(f" Node URI: {node.uri}")
        print(f" Node ID: {node.id}")
        print(f" Node Ping: {node.heartbeat}ms")
        print(f" Node Status: {node.status.name}")
        print("─" * 70)

    async def setup_hook(self):
        try:
            try:
                node1 = wavelink.Node(
                    uri="lava1.horizxon.tech:443", password="horizxon.tech", secure=True
                )
                await wavelink.NodePool.connect(client=self, nodes=[node1])
            except Exception as e:
                print("Error while connecting to node 1")

            try:
                node2 = wavelink.Node(
                    uri="lava3.horizxon.tech:443", password="horizxon.tech", secure=True
                )
                await wavelink.NodePool.connect(client=self, nodes=[node2])
            except Exception as e:
                print("Error while connecting to node 3")

            print("─" * 70)
            print("[WAVELINK] Successfully connected to Lavalink nodes!")
            print("─" * 70)
        except:
            print("─" * 70)
            print("[WAVELINK] Error while initiating a connection between the nodes")
            print("─" * 70)

        await asyncio.sleep(3)

        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    await bot.load_extension(f"cogs.{filename[:-3]}")
                    print("─" * 70)
                    print(
                        f"[EXTENSIONS] {filename[:-3]} has been loaded with no errors."
                    )
                    print("─" * 70)
                except Exception as e:
                    print(
                        "[STARTUP ERROR] Failed to load extension {}\n{}: {}".format(
                            filename, type(e).__name__, e
                        )
                    )

    async def on_ready(self):
        pid = os.getpid()

        set_key(".env", "PID", f"{pid}")

        if not self.added:
            self.add_view(StartupSettings())
            self.add_view(startHub())
            self.add_view(ticketSetup())
            self.add_view(ProfileBuilder())
            self.added = True

        endTime = time.time()
        bootTime = endTime - startTime

        dpyVersion = discord.__version__
        pythonVersion = platform.python_version()

        activity = discord.Activity(
            type=discord.ActivityType.listening, name=f"{config['prefix']}help | FTG"
        )
        await self.change_presence(activity=activity)

        art = r"""
__/\\\\\\\\\\\\\\\_        __/\\\\\\\\\\\\\\\_        _____/\\\\\\\\\\\\_        
 _\/\\\///////////__        _\///////\\\/////__        ___/\\\//////////__       
  _\/\\\_____________        _______\/\\\_______        __/\\\_____________      
   _\/\\\\\\\\\\\_____        _______\/\\\_______        _\/\\\____/\\\\\\\_     
    _\/\\\///////______        _______\/\\\_______        _\/\\\___\/////\\\_    
     _\/\\\_____________        _______\/\\\_______        _\/\\\_______\/\\\_   
      _\/\\\_____________        _______\/\\\_______        _\/\\\_______\/\\\_  
       _\/\\\_____________        _______\/\\\_______        _\//\\\\\\\\\\\\/__ 
        _\///______________        _______\///________        __\////////////____
"""
        print("─" * 70)
        print(art)
        print("─" * 70)
        print(" Boot Time: {:.2f}s to launch the program".format(bootTime))
        pid = os.getpid()
        print(f" Running On PID: {pid}")
        print("─" * 70)
        print(f" Operating on Python {pythonVersion}")
        print(f" Running: discord v{dpyVersion}")
        print("─" * 70)
        print(f" Username: {bot.user}")
        print(f" UserID: {bot.user.id}")
        print("─" * 70)

        if config["Restarted"] == "True":
            devChannel = self.get_channel(1134737529443196988)
            restartEmbed = discord.Embed(
                description="Restart was successful. It took me {:.2f} seconds to relaunch the program.".format(
                    bootTime
                ),
                color=0xB50000,
            )

            await devChannel.send(embed=restartEmbed)

            config["Restarted"] = "False"

            with open("./config.json", "w") as f:
                json.dump(config, f, indent=4)


if __name__ == "__main__":
    try:
        bot = Main()
        set_boot_time()
        bot.run(dpyToken)
    except Exception as error:
        print(f"An error has occured: {error}")
