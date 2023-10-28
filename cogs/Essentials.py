import json
import re
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

try:
    with open('./extras/afks.json', 'r') as file:
        afk_users = json.load(file)
except FileNotFoundError:
    afk_users = {}

class Essentials(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def nick(self, ctx, member: discord.Member = None, *, nickname: str):
        if member is None:
            member = ctx.author

            try:
                await ctx.message.delete()
                await member.edit(nick=nickname)
            except commands.MissingPermissions as error:
                embedError = discord.Embed(description="Your role is higher than mine.")

                await ctx.send(embedError)
            except commands.CommandOnCooldown as error:
                embedError = discord.Embed(
                    description=f"You can change your nickname again in {format_time(error.retry_after)}."
                )

                await ctx.send(embedError)
        else:
            try:
                await ctx.message.delete()
                await member.edit(nick=nickname)
            except commands.MissingPermissions as error:
                embedError = discord.Embed(description="Your role is higher than mine.")

                await ctx.send(embedError)

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def afk(self, ctx, *, reason: str = None):
        try:
            await ctx.message.delete()

            if reason is None:
                reason = "No reason was provided"

            afk_users[ctx.author.id] = {
                "Reason": reason,
                "oldNickname": ctx.author.display_name,
            }

            
            with open('./extras/afks.json', 'w') as file:
                json.dump(afk_users, file, indent=4)


            await ctx.author.edit(nick=f"[AFK] {ctx.author.display_name}")
        except commands.MissingPermissions as error:
            embedError = discord.Embed(description="Your role is higher than mine.")

            await ctx.send(embedError)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in afk_users:
            old_nickname = afk_users[message.author.id]["oldNickname"]
            await message.author.edit(nick=old_nickname)
            del afk_users[message.author.id]

            with open('./extras/afks.json', 'w') as afks:
                json.dump(afk_users, afks, indent=4)

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
                    color=0xB50000,
                )

                await ctx.send(embed=embed, delete_after=5)
            else:
                embed = discord.Embed(
                    description=f"{member.name} already has {role.name} role.",
                    color=0xB50000,
                )

                await ctx.send(embed=embed, delete_after=5)

    @role.command()
    async def remove(self, ctx, member: discord.Member, role: discord.Role):
        if role is not None or member is not None:
            if role not in member.roles:
                await ctx.send(f"{member.name} don't have {role.name}.")
            await member.remove_roles(role)
            await ctx.send(
                f"{member.mention} has been removed from the role '{role.name}'."
            )


async def setup(bot):
    await bot.add_cog(Essentials(bot))
