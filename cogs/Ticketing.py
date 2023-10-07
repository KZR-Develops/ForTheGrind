import asyncio
import discord
import json

from discord.ext import commands
from datetime import datetime
from views.Ticket import ticketSetup, Settings

with open('./config.json', "r") as f:
    config = json.load(f)

class TicketingSetup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name="ticket")
    @commands.has_permissions(manage_guild=True)
    async def ticket(self, ctx):
        try:
            if ctx.invoked_subcommand is None:
                pass
        except commands.errors.MissingPermissions:
            embedError = discord.Embed(description="You don't have enough permissions to run this command!", color=0xb50000)
            
            await ctx.message.delete()
            await ctx.send(embed=embedError, delete_after=5)

    @ticket.command()
    async def setup(self, ctx):
        embedSetup = discord.Embed(title="Do you need help?", description="To get help from our staffs, click the button below.\n\nIt will automatically generate a channel to discuss your problem with our support team.", color=0xb50000)
        await ctx.send(embed=embedSetup, view=ticketSetup())
        await ctx.message.delete()
            
    @ticket.command()
    async def settings(self, ctx):
        embedSettings = discord.Embed(description="What do you want to do to this ticket?")
        await ctx.send(embed=embedSettings, view=Settings())
        await ctx.message.delete()

    @ticket.command()
    async def setdashboard(self, ctx, channel: discord.TextChannel=None):
        olddashboard = config['channels']['ticket_dashboard']
        if channel is None:
            config['channels']['ticket_dashboard'] = ctx.channel.id 

            with open('./config.json', 'w') as file:
                json.dump(config, file, indent=8)

            embedSuccess = discord.Embed(description=f"``{ctx.channel.mention}`` is now set as the ticket dashboard.", color=0xb50000)    
            await ctx.send(embed=embedSuccess)
        else:
            if channel.id is olddashboard:
                embedError = discord.Embed(description=f"Error! {channel.mention} is already set as the ticket dashboard", color=0xb50000)
                await ctx.send(embed=embedError)

            else:
                config['channels']['ticket_dashboard'] = channel.id 

                with open('./config.json', 'w') as file:
                    json.dump(config, file, indent=8)

                embedSuccess = discord.Embed(description=f"``{channel.mention}`` is now set as the ticket dashboard.", color=0xb50000)    
                await ctx.send(embed=embedSuccess)


    
        
async def setup(bot):
    await bot.add_cog(TicketingSetup(bot))