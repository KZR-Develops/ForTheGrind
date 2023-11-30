import json
import random
import discord
import platform
import time

from discord.ext import commands


class EventsHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(self):
        print("─" * 70)
        print(f" [DISCORD] The client has successfully connected to Discord.")
        print("─" * 70)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        role_id = 1146684980563558440  # Replace with the actual role ID

        role = discord.utils.get(guild.roles, id=role_id)
        await member.add_roles(role)

        memberEmbed = discord.Embed(
            color=0xb50000,
            description="Welcome to the official Discord server of For The Grind Esports!\n\n<:Info:1134737385058476123> **To get access to our channels, please complete the verification process**:\n<:B2:1134737280297353246> Head over to our server's hub.\n<:B2:1134737280297353246> Click on the \"Server Rules\" and start reading them carefully.\n<:B2:1134737280297353246> Once you've read and understood all the rules, you'll receive a special role.\n<:B2:1134737280297353246> With your new role, you'll be able to connect with fellow gamers!\n\nIf you encounter any issues or have suggestions, don't hesitate to create a ticket. Our dedicated staff will be there to assist you.\n\nWe're excited to have you as part of our growing community!\n\nBest Regards,\nFor The Grind"
        )

        memberEmbed.set_author(name="For The Grind Esports - Welcome Message")

        await member.send(embed=memberEmbed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        with open("./config.json", 'r') as file:
            config = json.load(file)

        excRoles = config['GroupRoles']['Executives']
        supportRoles = config['GroupRoles']['SupportingStaff']
        specialRoles = config['GroupRoles']['Specials']
        orgRoles = config['GroupRoles']['Organization']

        if not before.premium_since and after.premium_since:
            # The user has just boosted the server
            special_role = discord.utils.get(after.guild.roles, id=1134472266890092607)
            if special_role:
                await after.add_roles(special_role)

        added_roles = set(after.roles) - set(before.roles)

        for role in added_roles:
            # Executives Group Role
            if role.id in excRoles and not discord.utils.get(after.roles, id=1145295540549062696):
                GroupRole = discord.utils.get(after.guild.roles, id=1145295540549062696)
                if GroupRole:
                    await after.add_roles(GroupRole)

            # Supporting Staff Group Role
            if role.id in supportRoles and not discord.utils.get(after.roles, id=1134472355935178752):
                GroupRole = discord.utils.get(after.guild.roles, id=1134472355935178752)
                if GroupRole:
                    await after.add_roles(GroupRole)
            
            # Specials Group Role
            if role.id in specialRoles and not discord.utils.get(after.roles, id=1134472266890092607):
                GroupRole = discord.utils.get(after.guild.roles, id=1134472266890092607)
                if GroupRole:
                    await after.add_roles(GroupRole)

            # Organization Members
            if role.id in orgRoles and not discord.utils.get(after.roles, id=1145298592173662269):
                GroupRole = discord.utils.get(after.guild.roles, id=1145298592173662269)
                if GroupRole:
                    await after.add_roles(GroupRole)

        removed_roles = set(before.roles) - set(after.roles)

        for role in removed_roles:
            removed_role_id = role.id

            if removed_role_id in excRoles:
                excRoles.remove(removed_role_id)
                GroupRole = discord.utils.get(after.guild.roles, id=1145295540549062696)
                if GroupRole:
                    await after.remove_roles(GroupRole)

            elif removed_role_id in supportRoles:
                supportRoles.remove(removed_role_id)
                GroupRole = discord.utils.get(after.guild.roles, id=1134472355935178752)
                if GroupRole:
                    await after.remove_roles(GroupRole)

            elif removed_role_id in specialRoles:
                specialRoles.remove(removed_role_id)
                GroupRole = discord.utils.get(after.guild.roles, id=1134472266890092607)
                if GroupRole:
                    await after.remove_roles(GroupRole)

            elif removed_role_id in orgRoles:
                orgRoles.remove(removed_role_id)
                GroupRole = discord.utils.get(after.guild.roles, id=1145298592173662269)
                if GroupRole:
                    await after.remove_roles(GroupRole)


async def setup(bot: commands.Bot):
    await bot.add_cog(EventsHandler(bot))
