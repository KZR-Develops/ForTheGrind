import discord
from views.Verify import Verify

from discord.ext import commands

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_join(self, member):

        unverified_id = 1146684980563558440

        if (member.bot):
            return
        
        unverified = discord.utils.get(member.guild.roles, id=unverified_id)
        await member.add_roles(unverified)
        
    @commands.command()
    async def vsetup(self, ctx):
        embedVerification = discord.Embed(title="New here?", description="Click the verify button below to get verified.", color=0x5865f2)
        await ctx.send(embed=embedVerification, view=Verify())
        await ctx.message.delete()
        
async def setup(bot):
    await bot.add_cog(Verification(bot))