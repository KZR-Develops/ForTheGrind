from typing import Optional
import discord
from discord.ext import commands

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setupHub(self, ctx):
        mainEmbed = discord.Embed(
            description="To get started, make sure you read the rules carefully and complete the verification process. Once you're done, feel free to explore and engage with the community. Happy navigating!",
            color=0xb50000
        )
        header = discord.File('img\headers\StartHere.png')
        await ctx.send(file=header)
        await ctx.send(embed=mainEmbed, view=rulesP1(), ephemeral=True)
        await ctx.message.delete()

class rulesP1(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.div = '<:Divider:1134737299515654198>' * 27

    @discord.ui.button(label="Start Reading the Rules", style=discord.ButtonStyle.red, custom_id="sH:start:red")
    async def start(self, interaction: discord.Interaction, button: discord.Button):
        rulesP1 = discord.Embed(
            title="Section 1: Discord's Rules",
            description=f"{self.div}\nThis server abides the Discord's Community Guidelines and Terms of Service.\nBe sure to be familiar with it to avoid any issues.\n\n**Discord's Community Guidelines**: https://discord.com/guidelines\n**Discord's Terms of Service**: https://discord.com/tos",
            color=0xb50000
        )

        await interaction.response.send_message(embed=rulesP1, view=rulesP2(), ephemeral=True, delete_after=240)

class rulesP2(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.div = '<:Divider:1134737299515654198>' * 27

    @discord.ui.button(label="Next Page", style=discord.ButtonStyle.gray, custom_id="sh:nextPage:gray")
    async def nextPage(self, interaction: discord.Interaction, button: discord.Button):
        rulesP2 = discord.Embed(
            title="Section 2: General Rules",
            description=f"{self.div}\n\n<:B1:1134737275318706278>Be Respectful: \n<:Empty:1134737303324065873><:SBB:1134737393921036348>Treat everyone with respect and courtesy. No harassment, hate speech, or personal attacks will be tolerated.\n\n<:B1:1134737275318706278> No NSFW Content:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Keep the server family-friendly. Do not share explicit, pornographic, or offensive material.\n\n<:B1:1134737275318706278> Stay On-Topic:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Keep discussions relevant to their channels. Avoid derailing conversations with unrelated topics.\n\n<:B1:1134737275318706278> No Spamming:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Do not flood the chat with repetitive messages, emojis, or unsolicited advertisements.\n\n<:B1:1134737275318706278> Real or Recognizable Nicknames\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Use nicknames that are either your real name or easily recognizable and associated with your online identity. This helps other members address you properly.\n\n<:B1:1134737275318706278> Respect Privacy:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Do not share personal information about yourself or others that could compromise privacy or security.",
            color=0xb50000
        )

        await interaction.response.send_message(embed=rulesP2, view=rulesP3(), ephemeral=True, delete_after=240)
    
class rulesP3(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.div = '<:Divider:1134737299515654198>' * 27

    @discord.ui.button(label="Next Page", style=discord.ButtonStyle.gray, custom_id="sh:nextPage:gray")
    async def nextPage(self, interaction: discord.Interaction, button: discord.Button):
        rulesP3 = discord.Embed(
            title="Section 3: Text Channel Rules",
            description=f"{self.div}\n\n<:B1:1134737275318706278> No Excessive @mentions:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Refrain from constantly tagging or mentioning other members, especially without a valid reason.\n\n<:B1:1134737275318706278> No Advertising:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Do not promote external servers, products, or services without permission from the server administrators.\n\n<:B1:1134737275318706278> No Drama or Gossip:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Do not use the text channels to fuel drama or spread rumors about other members or outside entities.\n\n<:B1:1134737275318706278> No Excessive Caps or Emoji:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Avoid using excessive capital letters or overusing emojis, as it can be disruptive and difficult to read.\n\n<:B1:1134737275318706278> No Backseat Moderating:\n<:Empty:1134737303324065873><:SBB:1134737393921036348> Let the server staff handle rule violations. If you notice a rule breach, report it instead of trying to enforce the rules yourself.",
            color=0xb50000
        )

        await interaction.response.send_message(embed=rulesP3, view=rulesP4(), ephemeral=True, delete_after=240)

class rulesP4(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.div = '<:Divider:1134737299515654198>' * 27

    @discord.ui.button(label="Next Page", style=discord.ButtonStyle.gray, custom_id="sh:nextPage:gray")
    async def nextPage(self, interaction: discord.Interaction, button: discord.Button):
        rulesP4 = discord.Embed(
            title="Important Notice",
            description=f"{self.div}\n\nThese rules may change without any prior notice, these ensure a healthy community.",
            color=0xb50000
        )
        
        if interaction.user.get_role(1145298592173662269):
            await interaction.response.send_message(embed=rulesP4, ephemeral=True, delete_after=240)
        else:
            await interaction.response.send_message(embed=rulesP4, view=Verification(), ephemeral=True, delete_after=240)

class Verification(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
            self.div = '<:Divider:1134737299515654198>' * 27

        @discord.ui.button(label="Next Page", style=discord.ButtonStyle.gray, custom_id="sh:nextPage:gray")
        async def nextPage(self, interaction: discord.Interaction, button: discord.Button):
            embedVerification = discord.Embed(
                title="First time here?",
                description=f"{self.div}\nTo complete the verification process, click the verify button below.",
                color=0xb50000
                )
            
            await interaction.response.send_message(embed=embedVerification, ephemeral=True, view=Verify(), delete_after=240)

class Verify(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Verify", style=discord.ButtonStyle.danger, custom_id="verify:red")
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