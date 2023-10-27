import json
import discord

from discord.ext import commands
from cogs.utils.embeds import *


class ErrorHandler(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        with open('./config.json', 'r') as f:
            config = json.load(f)
            botlogsID = config['channels']['botlogs']

        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.MissingPermissions):
            MissingPermissions(ctx=ctx)
        elif isinstance(error, commands.MissingRequiredArgument):
            MissingArguments(ctx=ctx)
        else:
            print(f"[COMMAND ERROR] {error}")
            embedError = discord.Embed(description="Oops! Something went wrong.", color=0xb50000)
            botLog = self.bot.get_channel(int(botlogsID))

            embedLog = discord.Embed(description=f"[ERROR COMMAND] {error}", color=0xb50000)
            await botLog.send(embed=embedLog)
            
            await ctx.send(embed=embedError, delete_after=5)


async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))