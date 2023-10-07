from typing import Optional
import discord

from discord.ext import commands
class ProfileBuilder(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Gender", style=discord.ButtonStyle.red, custom_id="pbGender:red",)
    async def gender(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user.get_role(1159728857264439297):
            genderDone = discord.Embed(description="You already picked your pronouns. Contact an admin if you want to repick your option.")
            await interaction.response.send_message(embed=genderDone, ephemeral=True, delete_after=3)
        elif interaction.user.get_role(1159728910737604680):
            genderDone = discord.Embed(description="You already picked your pronouns. Contact an admin if you want to repick your option.")
            await interaction.response.send_message(embed=genderDone, ephemeral=True, delete_after=3)
        elif interaction.user.get_role(1159732888414199870):
            genderDone = discord.Embed(description="You already picked your pronouns. Contact an admin if you want to repick your option.")
            await interaction.response.send_message(embed=genderDone, ephemeral=True, delete_after=3)
        else:
            genderEmbed = discord.Embed(description="How would you like to be addressed?", color=0xb50000)
            await interaction.response.send_message(embed=genderEmbed, view=Gender(), ephemeral=True, delete_after=3)

    @discord.ui.button(label="Age", style=discord.ButtonStyle.red, custom_id="pbAge:red")
    async def age(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user.get_role(1159726521632698449):
            ageDone = discord.Embed(description="You've already set your age. Contact an admin if you want to repick your option.", color=0xb50000)
            await interaction.response.send_message(embed=ageDone, ephemeral=True, delete_after=3)
        elif interaction.user.get_role(1159726592570957904):
            ageDone = discord.Embed(description="You've already set your age. Contact an admin if you want to repick your option.", color=0xb50000)
            await interaction.response.send_message(embed=ageDone, ephemeral=True, delete_after=3)
        elif interaction.user.get_role(1159726630042877982):
            ageDone = discord.Embed(description="You've already set your age. Contact an admin if you want to repick your option.", color=0xb50000)
            await interaction.response.send_message(embed=ageDone, ephemeral=True, delete_after=3)
        else:
            ageEmbed = discord.Embed(description="How old are you?")
            await interaction.response.send_message(embed=ageEmbed, view=Age(), ephemeral=True)

    @discord.ui.button(label="Game", style=discord.ButtonStyle.red, custom_id="pbGame:red")
    async def game(self, interaction: discord.Interaction, button: discord.Button):
        
        genderEmbed = discord.Embed(description="What games do you play?", color=0xb50000)
        await interaction.response.send_message(embed=genderEmbed, view=Games(), ephemeral=True)

class Gender(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=20)

    options = [
        discord.SelectOption(label="He/Him", value="h"),
        discord.SelectOption(label="She/Her", value="s"),
        discord.SelectOption(label="They/Them", value="t")
    ]

    @discord.ui.select(placeholder="Pick an option", options=options)
    async def menu_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        selfRole = discord.utils.get(interaction.user.guild.roles, id=1134472118252343426)
        he = discord.utils.get(interaction.user.guild.roles, id=1159728857264439297)
        she = discord.utils.get(interaction.user.guild.roles, id=1159728910737604680)
        nonBinary = discord.utils.get(interaction.user.guild.roles, id=1159732888414199870)

        if select.values[0] == "h":
            if interaction.user.get_role(1159728857264439297):
                genderDone = discord.Embed(description="You already picked your pronouns. Contact an admin if you want to repick your option.")
                await interaction.response.send_message(embed=genderDone, ephemeral=True, delete_after=3)
            else:
                await interaction.user.add_roles(he)
                embedRole = discord.Embed(description="Added <@&1159728857264439297> to your roles", color=0xb50000)
                await interaction.response.send_message(embed=embedRole, ephemeral=True, delete_after=3)
        if select.values[0] == "s":
            if interaction.user.get_role(1159728910737604680):
                genderDone = discord.Embed(description="You already picked your pronouns. Contact an admin if you want to repick your option.")
                await interaction.response.send_message(embed=genderDone, ephemeral=True, delete_after=3)
            else:
                await interaction.user.add_roles(she)
                embedRole = discord.Embed(description="Added <@&1159728910737604680> to your roles", color=0xb50000)
                await interaction.response.send_message(embed=embedRole, ephemeral=True, delete_after=3)
        if select.values[0] == "t":
            if interaction.user.get_role(1159728857264439297):
                genderDone = discord.Embed(description="You already picked your pronouns. Contact an admin if you want to repick your option.")
                await interaction.response.send_message(embed=genderDone, ephemeral=True, delete_after=3)
            else:
                await interaction.user.add_roles(nonBinary)
                embedRole = discord.Embed(description="Added <@&1159728857264439297> to your roles", color=0xb50000)
                await interaction.response.send_message(embed=embedRole, ephemeral=True, delete_after=3)

        await interaction.user.add_roles(selfRole)
        
class Age(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=20)

    options = [
        discord.SelectOption(label="13 to 15", value="1"),
        discord.SelectOption(label="16 to 18", value="2"),
        discord.SelectOption(label="19 and above", value="3")
    ]

    @discord.ui.select(placeholder="Pick an option", options=options)
    async def menu_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        selfRole = discord.utils.get(interaction.user.guild.roles, id=1134472118252343426)
        ttf = discord.utils.get(interaction.user.guild.roles, id=1159726521632698449)
        ste = discord.utils.get(interaction.user.guild.roles, id=1159726592570957904)
        nau = discord.utils.get(interaction.user.guild.roles, id=1159726630042877982)

        if select.values[0] == "1":
            if interaction.user.get_role(1159726521632698449):
                ageDone = discord.Embed(description="You've already set your age. Contact an admin if you want to repick your option.", color=0xb50000)
                await interaction.response.send_message(embed=ageDone, ephemeral=True, delete_after=3)
            else:
                await interaction.user.add_roles(ttf)
                embedRole = discord.Embed(description="Added <@&1159726521632698449> to your roles")
                await interaction.response.send_message(embed=embedRole, ephemeral=True, delete_after=3)
        if select.values[0] == "2":
            if interaction.user.get_role(1159726592570957904):
                ageDone = discord.Embed(description="You've already set your age. Contact an admin if you want to repick your option.", color=0xb50000)
                await interaction.response.send_message(embed=ageDone, ephemeral=True, delete_after=3)
            else:
                await interaction.user.add_roles(ste)
                embedRole = discord.Embed(description="Added <@&1159726592570957904> to your roles")
                await interaction.response.send_message(embed=embedRole, ephemeral=True, delete_after=3)
        if select.values[0] == "3":
            if interaction.user.get_role(1159726630042877982):
                ageDone = discord.Embed(description="You've already set your age. Contact an admin if you want to repick your option.", color=0xb50000)
                await interaction.response.send_message(embed=ageDone, ephemeral=True, delete_after=3)
            else:
                await interaction.user.add_roles(nau)
                embedRole = discord.Embed(description="Added <@&1159726630042877982> to your roles")
                await interaction.response.send_message(embed=embedRole, ephemeral=True, delete_after=3)

        await interaction.user.add_roles(selfRole)
        
class Games(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=20)

    options = [
        discord.SelectOption(label="Mobile Legends: Bang Bang", value="1"),
        discord.SelectOption(label="Valorant", value="2"),
        discord.SelectOption(label="Call of Duty: Mobile", value="3")
    ]

    @discord.ui.select(placeholder="Pick an option", options=options)
    async def menu_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        selfRole = discord.utils.get(interaction.user.guild.roles, id=1134472118252343426)
        ml = discord.utils.get(interaction.user.guild.roles, id=1159723941858922587)
        val = discord.utils.get(interaction.user.guild.roles, id=1159724038055272531)
        codm = discord.utils.get(interaction.user.guild.roles, id=1159723897323798538)

        if select.values[0] == "1":
            if interaction.user.get_role(1159723941858922587):
                gameDone = discord.Embed(description="You already have this role.")
                await interaction.response.send_message(embed=gameDone, ephemeral=True, delete_after=3)
            else:
                await interaction.user.add_roles(ml)
                embedRole = discord.Embed(description="Added <@&1159723941858922587> to your roles")
                await interaction.response.send_message(embed=embedRole, ephemeral=True, delete_after=3)
        if select.values[0] == "2":
            if interaction.user.get_role(1159724038055272531):
                gameDone = discord.Embed(description="You already have this role.")
                await interaction.response.send_message(embed=gameDone, ephemeral=True, delete_after=3)
            else:
                await interaction.user.add_roles(val)
                embedRole = discord.Embed(description="Added <@&1159724038055272531> to your roles")
                await interaction.response.send_message(embed=embedRole, ephemeral=True, delete_after=3)
        if select.values[0] == "3":
            if interaction.user.get_role(1159723897323798538):
                gameDone = discord.Embed(description="You already have this role.")
                await interaction.response.send_message(embed=gameDone, ephemeral=True, delete_after=3)
            else:
                await interaction.user.add_roles(codm)
                embedRole = discord.Embed(description="Added <@&1159723897323798538> to your roles")
                await interaction.response.send_message(embed=embedRole, ephemeral=True, delete_after=3)

        await interaction.user.add_roles(selfRole)