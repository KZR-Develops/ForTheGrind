import asyncio
from typing import Optional
import discord

from discord.ext import commands

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setupHub(self, ctx):
        startEmbed = discord.Embed(
            description="**For the Grinds Esports** was built to be one of the top gaming organizations in the Philippines, with a focus on cultivating players in the country.\nFor the Grinds Esports was established in the year 2020.",
            color=0xb50000
        )

        startEmbed.add_field(name="<:website:1160096124527452250> Quick Links", value="<:Empty:1134737303324065873><:SBB:1134737393921036348> [Facebook Page](https://www.facebook.com/FTGEsportsGG)\n<:Empty:1134737303324065873><:SBB:1134737393921036348> [Discord Server](https://discord.gg/GyNf93SAVf)", inline=True)
        startEmbed.add_field(name="<:redbook:1160100642891759686> Quick Information", value="<:Empty:1134737303324065873><:SBB:1134737393921036348> Co-Owners: <713953519597518939> & <239004733027778561>\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Created at: July 28, 2023 @ 10:46 AM", inline=True)

        mainEmbed = discord.Embed(
            description="To get started, make sure you read the rules carefully and complete the verification process. Once you're done, feel free to explore and engage with the community. Happy navigating!\n\nYou can also start personalizing your profile by clicking the **Profile Builder** button.\nThis will show a list of categories of self-roles you can have to personalize your server profile.\n\nHappy Navigating!",
            color=0xb50000
        )

        header = discord.File('img\headers\StartHere.png')
        await ctx.send(file=header)
        await ctx.send(embed=startEmbed)
        await ctx.send(embed=mainEmbed, view=startHub(), ephemeral=True)
        await ctx.message.delete()

class startHub(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Server Rules", style=discord.ButtonStyle.gray, custom_id="sH:start:gray", emoji="<:redbook:1160100642891759686>")
    async def serverRules(self, interaction: discord.Interaction, button: discord.Button):

        rulesP1 = discord.Embed(
            title="Section 1: Discord's Rules",
            description=f"This server strictly abides the Discord's Community Guidelines and Terms of Service. Be sure to be familiar with it to avoid any issues.\n\n**Discord's Community Guidelines**: https://discord.com/guidelines\n**Discord's Terms of Service**: https://discord.com/tos",
            color=0xb50000
        )

        rulesP2 = discord.Embed(
            title="Section 2: General Rules",
            description=f"<:B1:1134737275318706278>Be Respectful: \n<:Empty:1134737303324065873><:SBB:1134737393921036348>Treat everyone with respect and courtesy. No harassment, hate speech, or personal attacks will be tolerated.\n\n<:B1:1134737275318706278> No NSFW Content:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Keep the server family-friendly. Do not share explicit, pornographic, or offensive material.\n\n<:B1:1134737275318706278> Stay On-Topic:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Keep discussions relevant to their channels. Avoid derailing conversations with unrelated topics.\n\n<:B1:1134737275318706278> No Spamming:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Do not flood the chat with repetitive messages, emojis, or unsolicited advertisements.\n\n<:B1:1134737275318706278> Real or Recognizable Nicknames\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Use nicknames that are either your real name or easily recognizable and associated with your online identity. This helps other members address you properly.\n\n<:B1:1134737275318706278> Respect Privacy:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Do not share personal information about yourself or others that could compromise privacy or security.",
            color=0xb50000
        )

        rulesP3 = discord.Embed(
            title="Section 3: Text Channel Rules",
            description=f"<:B1:1134737275318706278> No Excessive @mentions:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Refrain from constantly tagging or mentioning other members, especially without a valid reason.\n\n<:B1:1134737275318706278> No Advertising:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Do not promote external servers, products, or services without permission from the server administrators.\n\n<:B1:1134737275318706278> No Drama or Gossip:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Do not use the text channels to fuel drama or spread rumors about other members or outside entities.\n\n<:B1:1134737275318706278> No Excessive Caps or Emoji:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Avoid using excessive capital letters or overusing emojis, as it can be disruptive and difficult to read.\n\n<:B1:1134737275318706278> No Backseat Moderating:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Let the server staff handle rule violations. If you notice a rule breach, report it instead of trying to enforce the rules yourself.",
            color=0xb50000
        )

        rulesP4 = discord.Embed(
            title="Important Notice",
            description=f"These rules are subject to change without prior notice, serving to maintain a thriving and positive community environment. Please make it a habit to review the rules regularly to prevent any misunderstandings or issues.",
            color=0xb50000
        )

        if interaction.user.get_role(1145298592173662269):
            message1 = await interaction.response.send_message(embed=rulesP1, ephemeral=True)
            message2 = await interaction.followup.send(embed=rulesP2, ephemeral=True)
            message3 = await interaction.followup.send(embed=rulesP3, ephemeral=True)
            message4 = await interaction.followup.send(embed=rulesP4, ephemeral=True)
        else:
            await interaction.response.send_message(embed=rulesP1, view=rulesPg2(), ephemeral=True, delete_after=240)

    @discord.ui.button(label="Roles Info", style=discord.ButtonStyle.gray, custom_id="sH:rI:gray", emoji="<:user:1160095232331874358>")
    async def rolesInfo(self, interaction: discord.Interaction, button: discord.Button):
        rolesInfo = discord.Embed(
            title="<:ftg:1160084867745316935> Staff Roles",
            color=0xb50000
        )

        rolesInfo.add_field(name="<:Empty:1134737303324065873>", value="<@&1134743832345448498>\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Top decision-maker, responsible for organizational direction and strategies.\n\n<@&1145297118735642715>\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Oversees daily operations, ensuring efficiency and effective resource management.\n\n<@&1145354422696825003>\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Manages Discord bots, enhancing server functionality through automation and maintenance.\n\n<@&1145296976963969084>\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Provides expert guidance and advice to the leadership team based on experience.\n\n<@&1145283225875390504>\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Leads esports initiatives, coordinating tournaments, player development, and team management.\n\n<@&1150328448049487944>\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Assists executives with various tasks, ensuring smooth operational functions.")
        rolesInfo.add_field(name="<:Empty:1134737303324065873>", value="<@&1160106324403687544>\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Coordinates talent acquisition, interviews, and onboarding, ensuring a skilled and motivated team.\n\n<@&1145345878777925763>\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Manages server, optimizing features and ensuring reliability.\n\n<@&1145295915159138334>\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Fosters community growth, engages members, and organizes events for enhanced interaction.\n\n<@&1145296297058910269>\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Maintains a positive and respectful community environment through rule enforcement.\n\n<@&1149656589544984618>\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Entry-level role, undergoing training to become a community moderator.")

        await interaction.response.send_message(embed=rolesInfo, ephemeral=True, delete_after=240)

    @discord.ui.button(label="Profile Builder", style=discord.ButtonStyle.gray, custom_id="sH:pB:gray", emoji="<:diy:1160120016314839080>")
    async def profileBuilder(self, interaction: discord.Interaction, button: discord.Button):
        profileBuilder = discord.Embed(
            description="This tool allows you to customize and personalize your profile by selecting various options that align with your interests and preferences. Based on your selections, the Profile Builder will automatically assign corresponding self-roles, enhancing your server experience and ensuring you're part of the communities that matter most to you.",
            color=0xb50000
        )

        await interaction.response.send_message(embed=profileBuilder, view=ProfileBuilder(), ephemeral=True, delete_after=120)

class rulesPg2(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Next Page", style=discord.ButtonStyle.gray, custom_id="sh:nextPage:gray", emoji="<:B6:1134737298030874634>")
    async def nextPage(self, interaction: discord.Interaction, button: discord.Button):
        rulesP2 = discord.Embed(
            title="Section 2: General Rules",
            description=f"<:B1:1134737275318706278>Be Respectful: \n<:Empty:1134737303324065873><:SBB:1134737393921036348>Treat everyone with respect and courtesy. No harassment, hate speech, or personal attacks will be tolerated.\n\n<:B1:1134737275318706278> No NSFW Content:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Keep the server family-friendly. Do not share explicit, pornographic, or offensive material.\n\n<:B1:1134737275318706278> Stay On-Topic:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Keep discussions relevant to their channels. Avoid derailing conversations with unrelated topics.\n\n<:B1:1134737275318706278> No Spamming:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Do not flood the chat with repetitive messages, emojis, or unsolicited advertisements.\n\n<:B1:1134737275318706278> Real or Recognizable Nicknames\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Use nicknames that are either your real name or easily recognizable and associated with your online identity. This helps other members address you properly.\n\n<:B1:1134737275318706278> Respect Privacy:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Do not share personal information about yourself or others that could compromise privacy or security.",
            color=0xb50000
        )

        await interaction.response.send_message(embed=rulesP2, view=rulesP3(), ephemeral=True, delete_after=240)
    
class rulesP3(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Next Page", style=discord.ButtonStyle.gray, custom_id="sh:nextPage:gray", emoji="<:B6:1134737298030874634>")
    async def nextPage(self, interaction: discord.Interaction, button: discord.Button):
        rulesP3 = discord.Embed(
            title="Section 3: Text Channel Rules",
            description=f"<:B1:1134737275318706278> No Excessive @mentions:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Refrain from constantly tagging or mentioning other members, especially without a valid reason.\n\n<:B1:1134737275318706278> No Advertising:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Do not promote external servers, products, or services without permission from the server administrators.\n\n<:B1:1134737275318706278> No Drama or Gossip:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Do not use the text channels to fuel drama or spread rumors about other members or outside entities.\n\n<:B1:1134737275318706278> No Excessive Caps or Emoji:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Avoid using excessive capital letters or overusing emojis, as it can be disruptive and difficult to read.\n\n<:B1:1134737275318706278> No Backseat Moderating:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Let the server staff handle rule violations. If you notice a rule breach, report it instead of trying to enforce the rules yourself.",
            color=0xb50000
        )

        await interaction.response.send_message(embed=rulesP3, view=rulesP4(), ephemeral=True, delete_after=240)

class rulesP4(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Next Page", style=discord.ButtonStyle.gray, custom_id="sh:nextPage:gray", emoji="<:B6:1134737298030874634>")
    async def nextPage(self, interaction: discord.Interaction, button: discord.Button):
        rulesP4 = discord.Embed(
            title="Important Notice",
            description=f"These rules are subject to change without prior notice, serving to maintain a thriving and positive community environment. Please make it a habit to review the rules regularly to prevent any misunderstandings or issues.",
            color=0xb50000
        )
        
        if interaction.user.get_role(1145298592173662269):
            await interaction.response.send_message(embed=rulesP4, ephemeral=True, delete_after=240)
        else:
            await interaction.response.send_message(embed=rulesP4, view=Verification(), ephemeral=True, delete_after=240)

class Verification(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label="Next Page", style=discord.ButtonStyle.gray, custom_id="sh:nextPage:gray", emoji="<:B6:1134737298030874634>")
        async def nextPage(self, interaction: discord.Interaction, button: discord.Button):
            embedVerification = discord.Embed(
                title="First time here?",
                description=f"To complete the verification process, click the verify button below.",
                color=0xb50000
                )
            
            await interaction.response.send_message(embed=embedVerification, ephemeral=True, view=Verify(), delete_after=240)

class Verify(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Verify", style=discord.ButtonStyle.danger, custom_id="verify:danger")
    async def verify(self, interaction: discord.Interaction, button: discord.Button):
        unverified_id = 1146684980563558440
        verified_id = 1145298592173662269
        defaults_id = 1145298529183604778

        embedVerified = discord.Embed(description="Great! You have successfully completed the verification process.  Feel free to start conversing and connecting with fellow members.\n\nHappy navigating!", color=0x00ff00)
        channel = interaction.channel
        user = interaction.user
        verified = discord.utils.get(user.guild.roles, id=verified_id)
        defaults = discord.utils.get(user.guild.roles, id=defaults_id)
        unverified = discord.utils.get(user.guild.roles, id=unverified_id)

        await user.remove_roles(unverified)
        await user.add_roles(verified)
        await user.add_roles(defaults)
        await interaction.response.send_message(embed=embedVerified, ephemeral=True, delete_after=10)

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
            description="Select roles to receive targeted notifications about updates, giveaways, and events you care about. Stay informed and engaged with what matters to you.",
            color=0xb50000
        )

        await interaction.response.send_message(embed=pingRoles, view=pingRole(), ephemeral=True, delete_after=120)

class pingRole(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label="Updates", value="updates", description="Stay informed with the latest community news and changes."),
        discord.SelectOption(label="Giveaways", value="giveaway", description="Get notified when a giveaway starts."),
        discord.SelectOption(label="Events", value="events", description="Engage in exciting community gatherings and friendly competitions.")
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
                embedRole = discord.Embed(description="Added <@&1145351148648284180> to your roles", color=0xb50000)
                await interaction.response.send_message(embed=embedRole, ephemeral=True, delete_after=3)
        if select.values[0] == "giveaway":
            if interaction.user.get_role(1145351002552270889):
                giveawaysDone = discord.Embed(description="You already have this role. I'll be removing this instead.")
                await interaction.user.remove_roles(giveaways)
                await interaction.response.send_message(embed=giveawaysDone, ephemeral=True, delete_after=3)
            else:
                await interaction.user.add_roles(giveaways)
                embedRole = discord.Embed(description="Added <@&1145351002552270889> to your roles", color=0xb50000)
                await interaction.response.send_message(embed=embedRole, ephemeral=True, delete_after=3)
        if select.values[0] == "events":
            if interaction.user.get_role(1145351092650127381):
                eventsDone = discord.Embed(description="You already have this role. I'll be removing this instead.")
                await interaction.user.remove_roles(events)
                await interaction.response.send_message(embed=eventsDone, ephemeral=True, delete_after=3)
            else:
                await interaction.user.add_roles(events)
                embedRole = discord.Embed(description="Added <@&1145351092650127381> to your roles", color=0xb50000)
                await interaction.response.send_message(embed=embedRole, ephemeral=True, delete_after=3)

        await interaction.user.add_roles(pingRoles)

class Gender(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=20)

    options = [
        discord.SelectOption(label="He/Him", value="h", emoji=":male_sign:"),
        discord.SelectOption(label="She/Her", value="s", emoji=":female_sign:"),
        discord.SelectOption(label="They/Them", value="t", emoji=":star:")
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

async def setup(bot):
    await bot.add_cog(Setup(bot))