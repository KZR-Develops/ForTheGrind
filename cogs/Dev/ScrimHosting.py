from typing import Optional
import discord

from utils.embeds import *
from discord.ext import commands

class ScrimHosting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.has_any_role(1145295915159138334, 1145296297058910269)
    async def scrim(self, ctx):
        if ctx.invoked_subcommand is None:
            MissingArguments(ctx=ctx)

    @scrim.commands()
    async def start(self, ctx):
        

    
async def setup(bot):
    await bot.add_cog(ScrimHosting(bot))