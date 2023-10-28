import datetime
import json
import discord

from datetime import datetime
from cogs.utils.utility import get_boot_time, format_boot_time
from discord.ext import commands

with open("config.json") as f:
    config = json.load(f)


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="info")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def info(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @info.command()
    async def server(self, ctx):
        guild = ctx.guild
        embedInfo = discord.Embed(
            description=guild.description, color=0xb50000
        )

        embedInfo.set_author(name=guild.name, icon_url=guild.icon)
        embedInfo.set_thumbnail(url=guild.icon)
        embedInfo.add_field(name="Server ID", value=guild.id, inline=False)
        embedInfo.add_field(
            name="Members Count",
            value=f"<:Empty:1134737303324065873><:SBB:1134737393921036348> {len(guild.members) - 1}", 
            inline=False)
        embedInfo.add_field(
            name="Channels Count",
            value=f"<:Empty:1134737303324065873><:SBB:1134737393921036348>Text Channels: {len([channel for channel in guild.channels if isinstance(channel, discord.TextChannel)])}\n<:Empty:1134737303324065873><:SBB:1134737393921036348>Voice Channels: {len([channel for channel in guild.channels if isinstance(channel, discord.VoiceChannel)])}",
            inline=False,
        )
        embedInfo.add_field(
            name="Boost Status",
            value=f"<:Empty:1134737303324065873><:SBB:1134737393921036348>Boost Level: {guild.premium_tier}\n<:Empty:1134737303324065873><:SBB:1134737393921036348>Boost Count: {guild.premium_subscription_count}",
            inline=False,
        )
        embedInfo.add_field(
            name="Creation Date",
            value=f'<:Empty:1134737303324065873><:SBB:1134737393921036348>{guild.created_at.__format__("%B %d, %Y @ %I:%M %p")}',
            inline=False,
        )

        if guild.verification_level == discord.VerificationLevel.none:
            embedInfo.add_field(
                name="Verification Level", 
                value="<:Empty:1134737303324065873><:SBB:1134737393921036348>[None] This server is unrestricted."
            )
        elif guild.verification_level == discord.VerificationLevel.low:
            embedInfo.add_field(
                name="Verification Level",
                value="<:Empty:1134737303324065873><:SBB:1134737393921036348>[Low] Must have a verified email on their account.",
            )
        elif guild.verification_level == discord.VerificationLevel.medium:
            embedInfo.add_field(
                name="Verification Level",
                value="<:Empty:1134737303324065873><:SBB:1134737393921036348>[Medium] Must be registered for longer than 5 minutes.",
            )
        elif guild.verification_level == discord.VerificationLevel.high:
            embedInfo.add_field(
                name="Verification Level",
                value="<:Empty:1134737303324065873><:SBB:1134737393921036348>[High] Must be a member for longer than 10 minutes.",
            )
        elif guild.verification_level == discord.VerificationLevel.highest:
            embedInfo.add_field(
                name="Verification Level",
                value="<:Empty:1134737303324065873><:SBB:1134737393921036348>[Highest] Must have a verified phone on their account.",
            )

        await ctx.send(embed=embedInfo)

    @info.command()
    async def member(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author
        elif member is not None:
            member = member

        roles = sorted(member.roles, key=lambda x: x.position, reverse=True)
        for role in roles:
            if role.hoist:
                highest_role = role
                break
            else:
                highest_role = member.top_role

        embedInfo = discord.Embed(color=member.color)

        embedInfo.set_thumbnail(url=member.avatar)
        embedInfo.set_author(
            name=f"{member.name}#{member.discriminator}", icon_url=member.avatar
        )
        embedInfo.add_field(name="Member ID", value=member.id, inline=True)
        embedInfo.add_field(name="Nickname", value=member.nick, inline=True)
        embedInfo.add_field(name="Top Role", value=highest_role, inline=False)
        embedInfo.add_field(
            name="Account Creation Date",
            value=member.created_at.__format__("%B %d, %Y @ %I:%M %p"),
            inline=False,
        )
        embedInfo.add_field(
            name="Member Since",
            value=member.joined_at.__format__("%B %d, %Y @ %I:%M %p"),
            inline=False,
        )

        await ctx.send(embed=embedInfo)

    @commands.command()
    async def ping(self, ctx):
        embedLatency = discord.Embed(
            title=f"<:SBT:1134737401089114203> Latency Checker",
            description=f"<:SBB:1134737393921036348> It took me approximately {round(self.bot.latency * 100)}ms to respond back.",
            color=0xB50000,
        )

        await ctx.send(embed=embedLatency)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def uptime(self, ctx):
        last_boot = get_boot_time()
        current_time = datetime.now()
        uptime = current_time - last_boot

        # Calculate days, hours, minutes, and seconds
        uptime_days = uptime.days
        uptime_hours = uptime.seconds // 3600
        uptime_minutes = (uptime.seconds // 60) % 60
        uptime_seconds = uptime.seconds % 60

        # Reset hours when another day has passed
        if uptime_days > 0:
            uptime_hours = uptime_hours % 24  # Reset the hours count

        # Create the uptime text
        uptime_text = ""
        if uptime_days > 0:
            uptime_text += f"{uptime_days} day{'s' if uptime_days > 1 else ''}, "
        if uptime_hours > 0:
            uptime_text += f"{uptime_hours} hour{'s' if uptime_hours > 1 else ''}, "
        if uptime_minutes > 0:
            uptime_text += (
                f"{uptime_minutes} minute{'s' if uptime_minutes > 1 else ''}, "
            )
        uptime_text += f"and {uptime_seconds} second{'s' if uptime_seconds > 1 else ''}"

        embed_uptime = discord.Embed(
            title="<:SBT:1134737401089114203> Total Running Time",
            description=f"<:SBB:1134737393921036348> {uptime_text}",
            color=0xB50000,
        )

        await ctx.send(embed=embed_uptime)

    @commands.command()
    async def help(self, ctx, page: int = None):
        if page is None:
            helpEmbed = discord.Embed(color=0xB50000)

            helpEmbed.add_field(
                name="All Available Category of Command List",
                value="<:Empty:1134737303324065873>\n<:Empty:1134737303324065873><:SBB:1134737393921036348> **Page 1**: Fun\n<:Empty:1134737303324065873><:SBB:1134737393921036348> **Page 2**: Utility\n<:Empty:1134737303324065873><:SBB:1134737393921036348> **Page 3**: Information\n<:Empty:1134737303324065873><:SBB:1134737393921036348> **Page 4**: Music\n<:Empty:1134737303324065873><:SBB:1134737393921036348> **Page 5**: Moderator Tools\n<:Empty:1134737303324065873><:SBB:1134737393921036348> **Page 6**: Developer Tools",
            )
        else:
            if page == 1:
                helpEmbed = discord.Embed(color=0xB50000)

                helpEmbed.add_field(
                    name="Page 1: Fun Commands",
                    value="<:Empty:1134737303324065873>\n<:B1:1134737275318706278> ftg.dice - Roll a dice.\n<:B1:1134737275318706278> ftg.coinflip - Flip a coin.\n<:B1:1134737275318706278> ftg.8ball - Ask the magic 8-ball a question.\n<:B1:1134737275318706278> ftg.rps - Play rock-paper-scissors.\n<:B1:1134737275318706278> ftg.dog - Get a random dog image.\n<:B1:1134737275318706278> ftg.cat - Get a random cat image.\n<:B1:1134737275318706278> ftg.dadjoke - Receive a dad joke.",
                )
            elif page == 2:
                helpEmbed = discord.Embed(color=0xB50000)

                helpEmbed.add_field(
                    name="Page 2: Utility Commands",
                    value="<:Empty:1134737303324065873>\n<:B1:1134737275318706278> ftg.afk - Sets your \"away\" status.\n<:B1:1134737275318706278> ftg.nick - Changes your nickname.",
                )
            elif page == 3:
                helpEmbed = discord.Embed(color=0xB50000)

                helpEmbed.add_field(
                    name="Page 3: Information Commands",
                    value="<:Empty:1134737303324065873>\n<:B1:1134737275318706278> ftg.help <page> - Displays brief information regarding commands usage.\n<:B1:1134737275318706278> ftg.info <subcommand>- Provides general information.\n<:Empty:1134737303324065873><:B1:1134737275318706278> ftg.info bot - Gives details about the bot.\n<:Empty:1134737303324065873><:B1:1134737275318706278> ftg.info server - Gives details about the server.\n<:Empty:1134737303324065873><:B1:1134737275318706278> ftg.info member <member> - Fetches information about a specific member.\n<:B1:1134737275318706278> ftg.ping - Checks the response time of the bot.\n<:B1:1134737275318706278> ftg.uptime - Shows how long the bot has been running since its last restart.",
                )

        await ctx.send(embed=helpEmbed)


async def setup(bot):
    await bot.add_cog(Information(bot))
