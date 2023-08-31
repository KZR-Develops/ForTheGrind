import discord

from discord.ext import commands

class ErrorHandler(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.MissingPermissions):
            embedError = discord.Embed(description="You are missing the required permission to run this command.", color=0xb50000)
            await ctx.send(embed=embedError, delete_after=5)
        else:
            embedError = discord.Embed(description="Oops! Something went wrong.", color=0xb50000)
            print(f"[COMMAND ERROR]{error}")
            await ctx.send(embed=embedError, delete_after=5)


async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))