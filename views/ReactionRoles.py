from typing import Optional
import discord

from discord.ext import commands
class ProfileBuilder(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Gender", style=discord.ButtonStyle.gray, custom_id="pbGender:gray",)
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
            await interaction.response.send_message(embed=genderEmbed, view=Gender(), ephemeral=True, delete_after=15)

    @discord.ui.button(label="Age", style=discord.ButtonStyle.gray, custom_id="pb:Age:gray")
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
            await interaction.response.send_message(embed=ageEmbed, view=Age(), ephemeral=True, delete_after=15)

    @discord.ui.button(label="Game", style=discord.ButtonStyle.gray, custom_id="pb:Game:gray")
    async def game(self, interaction: discord.Interaction, button: discord.Button):
        
        genderEmbed = discord.Embed(description="What games do you play?", color=0xb50000)
        await interaction.response.send_message(embed=genderEmbed, view=Games(), ephemeral=True, delete_after=15)

    @discord.ui.button(label="Ping Roles", style=discord.ButtonStyle.gray, custom_id="pB:pR:gray")
    async def pingRole(self, interaction: discord.Interaction, button: discord.Button):

        pingRoles = discord.Embed(
            description="Select roles to receive targeted notifications that matters to you.",
            color=0xb50000
        )

        await interaction.response.send_message(embed=pingRoles, view=pingRole(), ephemeral=True, delete_after=120)

class pingRole(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label="Updates", value="updates", description="Stay informed with the latest community news and changes.", emoji="<:community:1160393239996678204>"),
        discord.SelectOption(label="Giveaways", value="giveaway", description="Get notified when a giveaway starts.", emoji="<:giftss:1160393434041958410>"),
        discord.SelectOption(label="Events", value="events", description="Engage in exciting community gatherings and friendly competitions.", emoji="<:updates:1160393621812547705>")
    ]

    @discord.ui.select(placeholder="Pick an option", options=options)
    async def menu_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        pingRoles = discord.utils.get(interaction.user.guild.roles, id=1145350859140632616)
        updates = discord.utils.get(interaction.user.guild.roles, id=1145351148648284180)
        giveaways = discord.utils.get(interaction.user.guild.roles, id=1145351002552270889)
        events = discord.utils.get(interaction.user.guild.roles, id=1145351092650127381)

        if select.values[0] == "updates":
            if interaction.user.get_role(1145351148648284180):
                pingDone = discord.Embed(description="You already have this role. I'll be removing this instead.")
                await interaction.user.remove_roles(updates)
                await interaction.response.send_message(embed=pingDone, ephemeral=True, delete_after=3)
            else:
                await interaction.user.add_roles(updates)
                embedRole = discord.Embed(description="Added <:community:1160393239996678204> <@&1145351148648284180> to your roles", color=0xb50000)
                await interaction.response.send_message(embed=embedRole, ephemeral=True, delete_after=3)
        if select.values[0] == "giveaway":
            if interaction.user.get_role(1145351002552270889):
                giveawaysDone = discord.Embed(description="You already have this role. I'll be removing this instead.")
                await interaction.user.remove_roles(giveaways)
                await interaction.response.send_message(embed=giveawaysDone, ephemeral=True, delete_after=3)
            else:
                await interaction.user.add_roles(giveaways)
                embedRole = discord.Embed(description="Added <:giftss:1160393434041958410> <@&1145351002552270889> to your roles", color=0xb50000)
                await interaction.response.send_message(embed=embedRole, ephemeral=True, delete_after=3)
        if select.values[0] == "events":
            if interaction.user.get_role(1145351092650127381):
                eventsDone = discord.Embed(description="You already have this role. I'll be removing this instead.")
                await interaction.user.remove_roles(events)
                await interaction.response.send_message(embed=eventsDone, ephemeral=True, delete_after=3)
            else:
                await interaction.user.add_roles(events)
                embedRole = discord.Embed(description="Added <:updates:1160393621812547705> <@&1145351092650127381> to your roles", color=0xb50000)
                await interaction.response.send_message(embed=embedRole, ephemeral=True, delete_after=3)

        await interaction.user.add_roles(pingRoles)

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
        discord.SelectOption(label="Mobile Legends: Bang Bang", value="1", emoji="<:ml:1160491413847429261>"),
        discord.SelectOption(label="Valorant", value="2", emoji="<:valo:1160491417332895836>"),
        discord.SelectOption(label="Call of Duty: Mobile", value="3", emoji="<:codm:1160491412027093092>")
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
                embedRole = discord.Embed(description="Added <:ml:1160491413847429261> <@&1159723941858922587> to your roles")
                await interaction.response.send_message(embed=embedRole, ephemeral=True, delete_after=3)
        if select.values[0] == "2":
            if interaction.user.get_role(1159724038055272531):
                gameDone = discord.Embed(description="You already have this role.")
                await interaction.response.send_message(embed=gameDone, ephemeral=True, delete_after=3)
            else:
                await interaction.user.add_roles(val)
                embedRole = discord.Embed(description="Added <:valo:1160491417332895836> <@&1159724038055272531> to your roles")
                await interaction.response.send_message(embed=embedRole, ephemeral=True, delete_after=3)
        if select.values[0] == "3":
            if interaction.user.get_role(1159723897323798538):
                gameDone = discord.Embed(description="You already have this role.")
                await interaction.response.send_message(embed=gameDone, ephemeral=True, delete_after=3)
            else:
                await interaction.user.add_roles(codm)
                embedRole = discord.Embed(description="Added <:codm:1160491412027093092> <@&1159723897323798538> to your roles")
                await interaction.response.send_message(embed=embedRole, ephemeral=True, delete_after=3)

        await interaction.user.add_roles(selfRole)