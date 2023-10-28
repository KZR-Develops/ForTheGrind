import discord
import json

from .DeveloperTools import DeveloperTools
from discord.ext import commands

with open(file="./config.json", mode="r+") as configFile:
    config = json.load(configFile)


class ConfigLoader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.has_permissions(manage_guild=True)
    async def config(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @config.command()
    async def modlogs(self, ctx, channel: discord.TextChannel):
        oldmodlogs = config["channels"]["modlogs"]
        if channel is None:
            embedError = discord.Embed(
                description="Error! No channel was selected.", color=0xB50000
            )
            await ctx.send(embed=embedError, delete_after=5)
        else:
            if channel.id != oldmodlogs:
                config["channels"]["modlogs"] = channel.id

                with open(file="./config.json", mode="w") as configFile:
                    json.dump(config, configFile, indent=4)

                await self.bot.reload_extension("cogs.ModerationTools")
                embedSuccess = discord.Embed(
                    description="This channel have been configured to be a log for moderation actions.",
                    color=0xB50000,
                )
                await channel.send(embed=embedSuccess)
            else:
                embedError = discord.Embed(
                    description=f"{channel.mention} is already set as the moderation logs channel.",
                    color=0xB50000,
                )
                await ctx.send(embed=embedError)

    @config.command()
    async def prefix(self, ctx, prefix: str):
        oldprefix = config["prefix"]
        if prefix is None:
            embedError = discord.Embed(
                description=f"The command prefix should not be empty.", color=0xB50000
            )
            await ctx.send(embed=embedError)
        else:
            if prefix == oldprefix:
                embedError = discord.Embed(
                    description=f"{prefix} is already set as the command prefix.",
                    color=0xB50000,
                )
                await ctx.send(embed=embedError)
            else:
                if len(prefix) <= 4:
                    config["prefix"] = prefix

                    with open("./config.json", "w") as configFile:
                        json.dump(config, configFile, indent=4)

                    embedSuccess = discord.Embed(
                        description=f"``{prefix}`` is now set as the new command prefix.\nYou may need to restart the bot to load the changes.",
                        color=0xB50000,
                    )

                    activity = discord.Activity(
                        type=discord.ActivityType.listening, name=f"{prefix}help | FTG"
                    )
                    await self.bot.change_presence(activity=activity)
                    await ctx.send(embed=embedSuccess)
                else:
                    embedError = discord.Embed(
                        description=f"The command prefix should be less than 4 characters.",
                        color=0xB50000,
                    )
                    await ctx.send(embed=embedError)


async def setup(bot):
    await bot.add_cog(ConfigLoader(bot))
