import asyncio
from typing import Optional
import discord

from discord.ext import commands
from views.ReactionRoles import *

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
        startEmbed.add_field(name="<:redbook:1160100642891759686> Quick Information", value="<:Empty:1134737303324065873><:SBB:1134737393921036348> Co-Owners: <@713953519597518939> & <@239004733027778561>\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Created at: July 28, 2023 @ 10:46 AM", inline=True)

        mainEmbed = discord.Embed(
            description="Before you can access the server's exclusive contents, you need to get verified first. To get started, make sure you __read the rules carefully and complete the verification process__.\n\nOnce you're done with the verification, you can now start personalizing your profile by clicking the Profile Builder button. This will show a list of categories of self-roles you can have to personalize your server profile.\n\nOnce you're done, feel free to explore and engage with the community.\n\nHappy Navigating!",
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

async def setup(bot):
    await bot.add_cog(Setup(bot))