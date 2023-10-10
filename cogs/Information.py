import datetime
import json
import discord

from datetime import datetime
from cogs.utils.utility import get_boot_time, format_boot_time
from discord.ext import commands

with open('config.json') as f:
    config = json.load(f)
    
class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="info")
    async def info(self, ctx):
        sbt = "<:SBT:1134737401089114203>"
        sbb = "<:SBB:1134737393921036348>"

        if ctx.invoked_subcommand is None:
            with open('config.json', 'r') as f:
                config = json.load(f)
            
            with open('prodInfo.json', 'r') as f:
                prodInfo = json.load(f)
            
        
            lastBoot = get_boot_time()

            
            version = prodInfo['Version']
            phase = prodInfo['Phase']
            formattedLastBoot = format_boot_time("%A, %d %B %Y at %I:%M %p")
            dpyVersion = discord.__version__
            currentTime = datetime.now()
            uptime = currentTime - lastBoot
            uptime_days = uptime.days
            uptime_hours = uptime.seconds // 3600
            uptime_minutes = (uptime.seconds // 60) % 60

            createdTime = self.bot.user.created_at.strftime("%B %d, %Y @ %I:%M %p")
            
            embedInfo = discord.Embed(title="Official Bot's Information", color=0xb50000, description="<:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198><:Divider:1134737299515654198>")
            embedInfo.add_field(name=f"{sbt}Software Version", value=f'{sbb}{phase} {version}', inline=True)
            embedInfo.add_field(name=f"{sbt}Library Version", value=f"{sbb}Discord.py {dpyVersion}", inline=True)

            if uptime_days == 0:
                days_text = ""
            elif uptime_days == 1:
                days_text = f"{uptime.days} day,"
            else:
                days_text = f"{uptime.days} days,"

            if uptime_hours == 0:
                hours_text = ""
            elif uptime_hours == 1:
                hours_text = f"{uptime_hours} hour,"
            else:
                hours_text = f"{uptime_hours} hours,"

            if uptime_minutes == 0:
                minutes_text = ""
            elif uptime_minutes == 1:
                minutes_text = f"{uptime_minutes} minute, and"
            else:
                minutes_text = f"{uptime_minutes} minutes, and"

            seconds_text = f"{uptime.seconds % 60} seconds"

            uptime_text = f"{days_text} {hours_text} {minutes_text} {seconds_text}"

            embedInfo.add_field(name=f"{sbt}Total Running Time", value=f"{sbb}{uptime_text}", inline=False)
            embedInfo.add_field(name=f"{sbt}Last System Startup Date", value=f'{sbb}{formattedLastBoot}', inline=False)
            
            await ctx.send(embed=embedInfo)
    
    @info.command()
    async def server(self, ctx):
        guild = ctx.guild
        embedInfo = discord.Embed(description=guild.description, color=discord.Color.blue())

        embedInfo.set_author(name=guild.name, icon_url=guild.icon)
        embedInfo.set_thumbnail(url=guild.icon)
        embedInfo.add_field(name="Server ID", value=guild.id, inline=False)
        embedInfo.add_field(name="Members", value=guild.member_count, inline=False)
        embedInfo.add_field(name="Channels", value=f"Text Channels: {len([channel for channel in guild.channels if isinstance(channel, discord.TextChannel)])}\nVoice Channels: {len([channel for channel in guild.channels if isinstance(channel, discord.VoiceChannel)])}", inline=False)
        embedInfo.add_field(name="Boost Status", value=f"Boost Level: {guild.premium_tier}\nBoost Count: {guild.premium_subscription_count}", inline=False)
        embedInfo.add_field(name="Creation Date", value=guild.created_at.__format__("%B %d, %Y @ %I:%M %p"), inline=False)
        
        if guild.verification_level == discord.VerificationLevel.none:
            embedInfo.add_field(name="Verification Level", value="[None] This server is unrestricted.")
        elif guild.verification_level == discord.VerificationLevel.low:
            embedInfo.add_field(name="Verification Level", value="[Low] Must have a verified email on their account.")
        elif guild.verification_level == discord.VerificationLevel.medium:
            embedInfo.add_field(name="Verification Level", value="[Medium] Must be registered for longer than 5 minutes.")
        elif guild.verification_level == discord.VerificationLevel.high:
            embedInfo.add_field(name="Verification Level", value="[High] Must be a member for longer than 10 minutes.")
        elif guild.verification_level == discord.VerificationLevel.highest:
            embedInfo.add_field(name="Verification Level", value="[Highest] Must have a verified phone on their account.")
                

        await ctx.send(embed=embedInfo)
    
    @info.command()
    async def user(self, ctx, *, member: discord.Member=None):
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
        embedInfo.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar)
        embedInfo.add_field(name="Member ID", value=member.id, inline=True)
        embedInfo.add_field(name="Nickname", value=member.nick, inline=True)
        embedInfo.add_field(name="Top Role", value=highest_role, inline=False)
        embedInfo.add_field(name="Account Creation Date", value=member.created_at.__format__("%B %d, %Y @ %I:%M %p"), inline=False)
        embedInfo.add_field(name="Member Since", value=member.joined_at.__format__("%B %d, %Y @ %I:%M %p"), inline=False)
            
        await ctx.send(embed=embedInfo)
        
    @commands.command()
    async def ping(self, ctx):
        embedLatency = discord.Embed(title=f"<:SBT:1134737401089114203> Latency Checker", description=f"<:SBB:1134737393921036348> It took me approximately {round(self.bot.latency * 100)}ms to respond back.",color=0xb50000)
        
        await ctx.send(embed=embedLatency)
    
    
    @commands.command()
    async def uptime(self, ctx):
        last_boot = get_boot_time()
        current_time = datetime.now()
        uptime = current_time - last_boot

        # Calculate days, hours, minutes, and seconds
        uptime_days = uptime.days
        uptime_hours = uptime.seconds // 3600
        uptime_minutes = (uptime.seconds // 60) % 60
        uptime_seconds = uptime.seconds % 60

        # Adjust for days and hours
        if uptime_days > 0:
            uptime_hours += uptime_days * 24

        # Create the uptime text
        uptime_text = ""
        if uptime_days > 0:
            uptime_text += f"{uptime_days} day{'s' if uptime_days > 1 else ''}, "
        if uptime_hours > 0:
            uptime_text += f"{uptime_hours} hour{'s' if uptime_hours > 1 else ''}, "
        if uptime_minutes > 0:
            uptime_text += f"{uptime_minutes} minute{'s' if uptime_minutes > 1 else ''}, "
        uptime_text += f"{uptime_seconds} second{'s' if uptime_seconds > 1 else ''}"

        embed_uptime = discord.Embed(title="<:SBT:1134737401089114203> Total Running Time", description=f"<:SBB:1134737393921036348> {uptime_text}", color=0xb50000)

        await ctx.send(embed=embed_uptime)

async def setup(bot):
    await bot.add_cog(Information(bot))