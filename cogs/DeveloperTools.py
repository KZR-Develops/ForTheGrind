import asyncio
import time
import discord
import os
import sys
import json

from discord.ext import commands


# Fetch configuration datas
with open('config.json', 'r') as f:
    config = json.load(f)

class DeveloperTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.group()
    @commands.is_owner()
    async def cog(self, ctx):
        if ctx.invoked_subcommand is None:
            pass
    
    @commands.command()
    async def plugins(self, ctx):
        prefix = "<:Empty:1134737303324065873><:SBM:1134737397746257940> "

        all_cogs = set(self.bot.cogs.keys())  # All cogs
        loaded_cogs = set(cog.__class__.__name__ for cog in self.bot.cogs.values())  # Loaded cogs
        # unloaded_cogs = all_cogs - loaded_cogs

        loaded_cogs_text = "\n".join(f"{prefix}{cog}" for cog in loaded_cogs)
        # unloaded_cogs_text = "\n".join(f"{prefix}{cog}" for cog in unloaded_cogs)

        if not loaded_cogs:
            loaded_cogs_text = f"{prefix}No loaded cogs."

        embedCogs = discord.Embed(title="All Available Plugins", color=0xb50000)
        embedCogs.add_field(name="<:B6:1134737298030874634> Loaded Plugins", value=loaded_cogs_text)
        # embedCogs.add_field(name="<:B6:1134737298030874634> Unloaded Plugins", value=unloaded_cogs_text)
        await ctx.send(embed=embedCogs)

    @cog.command()
    async def unload(self, ctx, extension):
        try:
            await self.bot.unload_extension(f'cogs.{extension}')

            embedAction = discord.Embed(description=f"{extension} has been unloaded with no errors.", color=0x00ff00)
            await ctx.send(embed=embedAction, delete_after=5)
        except Exception as e:
            embedError = discord.Embed(description=f"An error occured while unloading module named {extension}.\n {e}.", color=0xb50000)
            await ctx.send(embed=embedError, delete_after=5)
    
    @cog.command()
    async def load(self, ctx, extension):
        try:
            await self.bot.reload_extension(f'cogs.{extension}')

            embedAction = discord.Embed(description=f"{extension} has been loaded with no errors.", color=0x00ff00)
            await ctx.send(embed=embedAction, delete_after=5)
        except Exception as e:
            embedError = discord.Embed(description=f"An error occured while loading module named {extension}.\n {e}.", color=0xb50000)
            await ctx.send(embed=embedError, delete_after=5)

    @cog.command()
    async def reload(self, ctx, extension):
        try:
            await self.bot.reload_extension(f'cogs.{extension}')

            embedAction = discord.Embed(description=f"{extension} has been reloaded with no errors.", color=0x00ff00)
            await ctx.send(embed=embedAction, delete_after=5)
        except Exception as e:
            embedError = discord.Embed(description=f"An error occured while unloading module named {extension}.\n {e}.", color=0xb50000)
            await ctx.send(embed=embedError, delete_after=5)

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await self.bot.close()
        print("Closed the connection between the bot and the gateway.")
        self.bot.clear()
        os._exit(0)

async def setup(bot):
    await bot.add_cog(DeveloperTools(bot))
