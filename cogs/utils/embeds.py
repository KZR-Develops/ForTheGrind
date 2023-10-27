import discord

async def MissingPermissions(ctx):
    embed = discord.Embed(
        description="You don't have enough permissions to run this command.",
        color=0xb50000
    )

    await ctx.send(embed=embed, delete_after=5)

async def MissingArguments(ctx):
    embed = discord.Embed(
        description="Cannot complete the request, command is missing a required argument.",
        color=0xb50000
    )

    await ctx.send(embed=embed, delete_after=5)

async def MissingRole(ctx):
    embed = discord.Embed(
        description="Cannot complete the request, command is missing a required argument.",
        color=0xb50000
    )

    await ctx.send(embed=embed, delete_after=5)