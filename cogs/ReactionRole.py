import discord

from discord.ext import commands
from views.ReactionRoles import *

class ReactionRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.has_role(1145345878777925763)
    async def rr(self, ctx):
        try:
            if ctx.invoked_subcommand is None:
                pass
        except commands.errors.MissingRole:
            embedError = discord.Embed(description="Only the server technician can use reaction role commands!", color=0xb50000)

            await ctx.message.delete()
            await ctx.send(embed=embedError, delete_after=5)

    @rr.command()
    async def setup(self, ctx):
        header = discord.File('img\headers\ProfileBuilder.png')
        await ctx.send(file=header)

        pbEmbed = discord.Embed(description="Click one of any buttons below to start building your profile?", color=0xb50000)
        await ctx.send(embed=pbEmbed, view=ProfileBuilder())
    
async def setup(bot):
    await bot.add_cog(ReactionRole(bot))