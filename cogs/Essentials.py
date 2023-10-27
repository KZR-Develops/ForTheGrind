import json
import discord

from discord.ext import commands

def format_time(self, seconds):
                # Extract hours, minutes, and seconds
                hours, remainder = divmod(seconds, 3600)
                minutes, seconds = divmod(remainder, 60)

                # Build a readable time format
                if hours:
                    return f"{hours} hours, {minutes} minutes, and {seconds} seconds"
                elif minutes:
                    return f"{minutes} minutes and {seconds} seconds"
                else:
                    return f"{seconds} seconds"
                
class Essentials(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 86400)
    async def nick(self, ctx, member: discord.Member, *, nickname):
        # Get the remaining cooldown time for the user
        remaining_cooldown = round(commands.cooldowns.Cooldown(1, 86400, commands.BucketType.user).get_bucket(ctx.message).get_retry_after())
        await ctx.message.delete()

        if remaining_cooldown == 0:
            await member.edit(nick=nickname)
        else:
            # Create an embed
            embed = discord.Embed(
                description=f"You can change your nickname again after {format_time(remaining_cooldown)}.",
                color=0xb50000 # You can choose a different color
            )

            await ctx.send(embed=embed)

    @commands.group()
    async def role(self, ctx):
         if ctx.invoked_subcommand is None:
              pass
            
    @role.command()
    async def give(self, ctx, member: discord.Member, role: discord.Role):
        if role is not None or member is not None:
            if role not in member.roles:
                await ctx.message.delete()
                await member.add_roles(role)
                embed = discord.Embed(
                    description=f"{role.name} role was given to {member.name}.",
                    color=0xb50000
                )

                await ctx.send(embed=embed, delete_after=5)
            else:
                embed = discord.Embed(
                    description=f"{member.name} already has {role.name} role.",
                    color=0xb50000
                )

                await ctx.send(embed=embed, delete_after=5)

    @role.command()
    async def remove(self, ctx, member: discord.Member, role: discord.Role):
        if role is not None or member is not None:
            if role not in member.roles:
                await ctx.send(f"{member.name} don't have {role.name}.")
            await member.remove_roles(role)
            await ctx.send(f"{member.mention} has been removed from the role '{role.name}'.")
              

              
         
async def setup(bot):
    await bot.add_cog(Essentials(bot))