import asyncio
import subprocess
import time
import discord
import os
import json

from discord.ext import commands
from cogs.Music import Music

# Fetch configuration datas
with open("config.json", "r") as f:
    config = json.load(f)


class DeveloperTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.has_role(1145345878777925763)
    @commands.group(invoke_without_command=True)
    async def plugin(self, ctx):
        if ctx.invoked_subcommand is None:
            prefix = "<:Empty:1134737303324065873><:SBM:1134737397746257940> "

            all_cogs = set(self.bot.cogs.keys())  # All cogs
            loaded_cogs = set(
                cog.__class__.__name__ for cog in self.bot.cogs.values()
            )  # Loaded cogs
            # unloaded_cogs = all_cogs - loaded_cogs

            loaded_cogs_text = "\n".join(f"{prefix}{cog}" for cog in loaded_cogs)
            # unloaded_cogs_text = "\n".join(f"{prefix}{cog}" for cog in unloaded_cogs)

            if not loaded_cogs:
                loaded_cogs_text = f"{prefix}No loaded cogs."

            embedCogs = discord.Embed(title="All Available Plugins", color=0xB50000)
            embedCogs.add_field(
                name="<:B6:1134737298030874634> Loaded Plugins", value=loaded_cogs_text
            )
            # embedCogs.add_field(name="<:B6:1134737298030874634> Unloaded Plugins", value=unloaded_cogs_text)
            await ctx.send(embed=embedCogs)
        else:
            pass

    @plugin.command()
    async def unload(self, ctx, extension):
        await ctx.message.delete()
        try:
            print('─' * 70)
            print(f"Attempting to unload {extension}...")
            print('─' * 70)
            await self.bot.unload_extension(f"cogs.{extension}")
            embedAction = discord.Embed(
                description=f"{extension} has been unloaded with no errors.",
                color=0x00FF00,
            )

            print('─' * 70)
            print(f"{extension} has been unloaded successfuly.")
            print('─' * 70)
            await ctx.send(embed=embedAction, delete_after=3)
        except Exception as e:
            embedError = discord.Embed(
                description=f"An error occured while unloading module named {extension}.\n {e}.",
                color=0xB50000,
            )
            print(
                f"[EXTENSION ERROR] An error occured while unloading module named {extension}.\n {e}."
            )
            await ctx.message.delete()
            await ctx.send(embed=embedError, delete_after=3)

    @plugin.command()
    async def load(self, ctx, extension):
        await ctx.message.delete()

        try:
            print('─' * 70)
            print(f"Attempting to load {extension}...")
            print('─' * 70)
            await self.bot.reload_extension(f"cogs.{extension}")
            embedAction = discord.Embed(
                description=f"{extension} has been loaded with no errors.",
                color=0x00FF00,
            )
            await ctx.send(embed=embedAction, delete_after=5)

            print('─' * 70)
            print(f"{extension} has been loaded successfuly.")
            print('─' * 70)
        except Exception as e:
            embedError = discord.Embed(
                description=f"An error occured while loading module named {extension}.\n {e}.",
                color=0xB50000,
            )
            print(
                f"[EXTENSION ERROR] An error occured while loading module named {extension}.\n {e}."
            )
            await ctx.send(embed=embedError, delete_after=5)

    @plugin.command()
    async def reload(self, ctx, extension: str = None):
        await ctx.message.delete()
        if extension != None:
            try:
                print('─' * 70)
                print("Attempting to reload active bot extensions...")
                print('─' * 70)
                if extension == "Music":
                    cog = self.bot.get_cog("Music")
                    if cog:
                        leave_command = self.bot.get_command("leave")
                        if leave_command:
                            try:
                                await ctx.invoke(leave_command)
                            except Exception as e:
                                print(f"[EXTENSION ERROR] An error occurred while reloading module named Music: {e}")
                        else:
                            print("The 'leave' command was not found in the Music cog.")
                    else:
                        print("The Music cog was not found.")

                await self.bot.reload_extension(f"cogs.{extension}")
                embedAction = discord.Embed(
                    description=f"{extension} has been reloaded with no errors.",
                    color=0x00FF00,
                )
                await ctx.send(embed=embedAction, delete_after=5)
                print('─' * 70)
                print(f"{extension} has been reloaded successfuly.")
                print('─' * 70)
            except Exception as e:
                embedError = discord.Embed(
                    description=f"An error occured while reloading module named {extension}.\n {e}.",
                    color=0xB50000,
                )
                print(
                    f"[EXTENSION ERROR] An error occured while reloading module named {extension}.\n {e}."
                )
                await ctx.send(embed=embedError, delete_after=5)
        else:
            for filename in os.listdir("./cogs"):
                if filename.endswith(".py"):
                    if not filename.startswith("DeveloperTools"):
                        try:
                            await asyncio.sleep(3)
                            await self.bot.reload_extension(f"cogs.{filename[:-3]}")
                            embedAction = discord.Embed(
                                description=f"{filename[:-3]} has been reloaded with no errors.",
                                color=0x00FF00,
                            )
                            await ctx.send(embed=embedAction, delete_after=5)
                            print("─" * 70)
                            print(f"{filename[:-3]} has been reloaded with no errors.")
                            print("─" * 70)
                        except Exception as e:
                            embedError = discord.Embed(
                                description=f"An error occured while reloading module named {filename[:-3]}.\n {e}.",
                                color=0xB50000,
                            )
                            print(
                                f"[EXTENSION ERROR] An error occured while reloading module named {filename[:-3]}.\n {e}."
                            )
                            await ctx.send(embed=embedError, delete_after=5)

            embedAction = discord.Embed(
                description=f"All plugins has been reloaded successfuly with no errors.",
                color=0x00FF00,
            )
            await ctx.send(embed=embedAction, delete_after=10)

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Shutting down...")
        config["Restarted"] == "False"

        with open("./config.json", "w") as f:
            json.dump(config, f, indent=4)

        await ctx.message.delete()
        await asyncio.sleep(5)
        await self.bot.close()
        print("Closed the connection between the bot and the gateway.")

        self.bot.clear()
        os._exit(0)

    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
        os.system("cls")
        print("Initiating a restart.")
        await asyncio.sleep(5)
        await ctx.send("Initiating a restart...")

        config["Restarted"] = "True"

        with open("./config.json", "w") as f:
            json.dump(config, f)

        await ctx.message.delete()
        await self.bot.close()
        print("Closed the connection between the bot and the gateway.")
        pid = os.getpid()
        time.sleep(10)  # Await for other tasks to finish
        subprocess.Popen(["start", "cmd", "/c", "start_bot.bat"], shell=True)
        print("Bot started on another process...")
        time.sleep(10)
        os.system(f"taskkill /F /PID {pid}")
        os._exit(0)


async def setup(bot):
    await bot.add_cog(DeveloperTools(bot))
