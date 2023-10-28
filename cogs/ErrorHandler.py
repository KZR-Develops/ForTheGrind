import json
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

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description="Cannot complete the request, command is missing a required argument.",
                color=0xB50000,
            )

            await ctx.send(embed=embed, delete_after=5)

        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                description=f"This command is on cooldown. Please wait for {error.retry_after:.0f} seconds before trying again.",
                color=0xB50000,
            )

            await ctx.send(embed=embed, delete_after=5)

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
