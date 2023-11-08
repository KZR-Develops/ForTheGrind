import json
import os
import subprocess
import time
import discord

from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        with open("./config.json", "r") as f:
            config = json.load(f)
            botlogsID = config["channels"]["botlogs"]

        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description="You don't have enough permissions to run this command.",
                color=0xB50000,
            )

            await ctx.send(embed=embed, delete_after=5)

        elif isinstance(error, commands.MissingAnyRole):
            embed = discord.Embed(
                description="You don't have the required role to run this command.",
                color=0xB50000,
            )

            await ctx.send(embed=embed, delete_after=5)
        
        elif isinstance(error, commands.MissingRole):
            embed = discord.Embed(
                description="You don't have the required role to run this command.",
                color=0xB50000,
            )

            await ctx.send(embed=embed, delete_after=5)

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description="Cannot complete the request, command is missing a required argument.",
                color=0xB50000,
            )

            await ctx.send(embed=embed, delete_after=5)

        elif isinstance(error, commands.CommandOnCooldown):
            # Convert seconds to hours, minutes, and seconds
            hours, remainder = divmod(error.retry_after, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Create a readable time string
            time_str = f"{int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds"

            embed = discord.Embed(
                description=f"This command is on cooldown. Please wait for {time_str} before trying again.",
                color=0xB50000,
            )

            await ctx.send(embed=embed, delete_after=5)

        elif isinstance(error, discord.ConnectionClosed):
            # If it's a connection error
            await self.bot.close()
            print("Connection error detected. Restarting Wi-Fi and the bot...")
            subprocess.Popen(["cmd", "/c", "netsh interface set interface \"Wi-Fi\" admin=disable"], shell=True)
            os.system("cls")
            print("Disabled the Wi-Fi Connection...")
            time.sleep(5)  # Waits for 5 seconds
            subprocess.Popen(["cmd", "/c", "netsh interface set interface \"Wi-Fi\" admin=enable"], shell=True)
            print("Renabled the Wi-Fi Connection...")
            time.sleep(5)  # Waits for 5 seconds
            os.system("cls")
            subprocess.Popen(["start", "cmd", "/c", "start_bot.bat"], shell=True)
            config["Restarted"] = "True"

            with open("./config.json", "w") as f:
                json.dump(config, f)
            print("Bot started on another process...")
            time.sleep(10)
            os._exit(0)

        else:
            print(f"[COMMAND ERROR] {error}")
            embedError = discord.Embed(
                description="Oops! Something went wrong.", color=0xB50000
            )
            botLog = self.bot.get_channel(int(botlogsID))

            embedLog = discord.Embed(
                description=f"[ERROR COMMAND] {error}", color=0xB50000
            )
            await botLog.send(embed=embedLog)

            await ctx.send(embed=embedError, delete_after=5)


async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
