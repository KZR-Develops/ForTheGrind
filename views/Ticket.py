import asyncio
import math
import os
from typing import Optional
import discord
import datetime
import json

from discord.ext import commands
from datetime import datetime

from discord.interactions import Interaction
from discord.utils import MISSING

with open("./config.json", "r") as f:
    config = json.load(f)

<<<<<<< HEAD

async def ticketDashboard(type, claimStatus, interaction: discord.Interaction):
    b6 = "<:B6:1134737298030874634>"
    userName = interaction.user.name
    userID = interaction.user.id
    dashboard = discord.utils.get(
        interaction.guild.channels, id=config["channels"]["ticket_dashboard"]
    )

    if type == None:
        desc = f""
    else:
        desc = f"Type: {type}\nStatus: {claimStatus}"

    embed = discord.Embed(
        title="Ticket Manager",
        description=desc,
        timestamp=datetime.now(),
        color=0xB50000,
    )

    embed.add_field(
        name="Author Information", value=f"{b6}Name: {userName}\n{b6}User ID: {userID}"
    )

    await dashboard.send(embed=embed, view=closedButtons(interaction))


async def generate(self, interaction: discord.Interaction, type):
    author = interaction.user
    guild = interaction.guild
    category = discord.utils.get(guild.categories, id=self.ticket_category_id)

    self.ticket_name = config["Total Tickets"] + 1
    config["Total Tickets"] = self.ticket_name
    with open("./config.json", "w") as file:
        json.dump(config, file)

    channel_name = f"ticket-{self.ticket_name}"
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        interaction.user: discord.PermissionOverwrite(
            view_channel=True, send_messages=True, attach_files=True, embed_links=True
        ),
    }
    channel = await guild.create_text_channel(
        channel_name, category=category, overwrites=overwrites
    )

    embedAssistance = discord.Embed(
        title=f"Ticket Manager",
        description=f"Hey there {author.mention}!\nA <@&{self.ticket_role}> will be here shortly, please wait.",
        timestamp=datetime.now(),
        color=0xB50000,
    )

    if type == "question":
        embedAssistance.set_footer(text=f"Type: Question")
        await channel.send(embed=embedAssistance, view=StarupSettings())
        await ticketDashboard(
            interaction=interaction, type="Question", claimStatus="Open"
        )

    if type == "report":
        embedAssistance.set_footer(text=f"Type: Report")
        await channel.send(embed=embedAssistance, view=ReportTypeSelector())
        await ticketDashboard(
            interaction=interaction, type="Question", claimStatus="Open"
        )

    if type == "appeal":
        embedAssistance.set_footer(text=f"Type: Appeal")
        await channel.send(embed=embedAssistance, view=AppealTypeSelector())
        await ticketDashboard(
            interaction=interaction, type="Question", claimStatus="Open"
        )

    embedCreated = discord.Embed(
        title="Ticket Manager",
        description=f"{author.mention}, Your ticket has been created in {channel.mention}.",
        timestamp=datetime.now(),
        color=0xB50000,
    )
    await interaction.response.send_message(embed=embedCreated, ephemeral=True)


class ticketSetup(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.cooldown = commands.CooldownMapping.from_cooldown(
            1, 600, commands.BucketType.member
        )

    @discord.ui.button(
        label="Create a Ticket",
        style=discord.ButtonStyle.red,
        custom_id="create:blurple",
    )
=======
async def generate(self, interaction: discord.Interaction, type):
    
        author = interaction.user
        guild = interaction.guild
        category = discord.utils.get(guild.categories, id=self.ticket_category_id)
        dashboard = discord.utils.get(guild.channels, id=self.ticket_dashboard_id)
        self.total_ticket = category.channels
        self.ticket_count = len(self.total_ticket) - 2
        self.ticket_name = self.ticket_count + 1
        channel_name = f'ticket-{self.ticket_name}'
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel = False),
            interaction.user: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files = True, embed_links = True)
        }
        channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)

        if type == "question":
            embedAssistance = discord.Embed(title=f"Ticket Manager", description=f"Hey there {author.mention}!\nA <@&{self.ticket_role}> will be here shortly, please wait.", timestamp=datetime.now(), color=0xb50000)
            embedAssistance.set_footer(text=f"Ticket ID: {self.ticket_name} • Type: Question")
            await channel.send(embed=embedAssistance)
            
            embedDashboard = discord.Embed(description=f"Type of Ticket: Question\nTicket Channel: {channel.mention}", color=0xb50000, timestamp=datetime.now())
            embedDashboard.set_author(name=f"A ticket was generated for {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar)
            embedDashboard.set_footer(text=f"Ticket ID: {self.ticket_name}")
            
            await dashboard.send(embed=embedDashboard)
        if type == "report":
            embedAssistance = discord.Embed(title=f"Ticket Manager", description=f"Hey there {author.mention}!\nA <@&{self.ticket_role}> will be here shortly, please wait.", timestamp=datetime.now(), color=0xb50000)
            embedAssistance.set_footer(text=f"Ticket ID: {self.ticket_name} • Type: Report")
            await channel.send(embed=embedAssistance, view=ReportTypeSelector())
            
            embedDashboard = discord.Embed(description=f"Type of Ticket: Report\nTicket Channel: {channel.mention}", color=0xb50000, timestamp=datetime.now())
            embedDashboard.set_author(name=f"A ticket was generated for {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar)
            embedDashboard.set_footer(text=f"Ticket ID: {self.ticket_name}")
            
            await dashboard.send(embed=embedDashboard)
        if type == "appeal":
            embedAssistance = discord.Embed(title=f"Ticket Manager", description=f"Hey there {author.mention}!\nA <@&{self.ticket_role}> will be here shortly, please wait.", timestamp=datetime.now(), color=0xb50000)
            embedAssistance.set_footer(text=f"Ticket ID: {self.ticket_name} • Type: Appeal")
            await channel.send(embed=embedAssistance, view=AppealTypeSelector()) 
            
            embedDashboard = discord.Embed(description=f"Type of Ticket: Appeal\nTicket Channel: {channel.mention}", color=0xb50000, timestamp=datetime.now())
            embedDashboard.set_author(name=f"A ticket was generated for {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar)
            embedDashboard.set_footer(text=f"Ticket ID: {self.ticket_name}")
            
            await dashboard.send(embed=embedDashboard) 

        
        embedCreated = discord.Embed(title="Ticket Manager", description=f"{author.mention}, Your ticket has been created in {channel.mention}.", timestamp=datetime.now(), color=0xb50000)    
        await interaction.response.send_message(embed=embedCreated, ephemeral=True)

class Setup(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 600, commands.BucketType.member)
    
    @discord.ui.button(label="Create a Ticket", style=discord.ButtonStyle.red, custom_id="create:blurple")
>>>>>>> e200e1035f2a61a8df79874c40551ca6c26cbd3d
    async def create(self, interaction: discord.Interaction, button: discord.ui.Button):
        interaction.message.author = interaction.user
        retry = self.cooldown.get_bucket(interaction.message).update_rate_limit()

        if retry:
<<<<<<< HEAD

=======
>>>>>>> e200e1035f2a61a8df79874c40551ca6c26cbd3d
            def convert_seconds(seconds):
                if seconds > 60:
                    minutes = seconds // 60
                    seconds = seconds % 60
                    rounded_seconds = math.floor(seconds)

                    return f"{str(minutes).rstrip('.0')} minutes and {rounded_seconds} seconds"
                else:
                    return f"{rounded_seconds} seconds"
<<<<<<< HEAD

            return await interaction.response.send_message(
                f"Slow down! You can create a ticket again in {convert_seconds(retry)}",
                ephemeral=True,
            )

        embedTypeSelector = discord.Embed(
            description="To assist you further, tell us why you are creating a ticket.",
            color=0xB50000,
        )
        await interaction.response.send_message(
            embed=embedTypeSelector, view=TicketTypeSelector(), ephemeral=True
        )


class TicketTypeSelector(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    ticket_category_id = config["categories"]["ticket"]
    ticket_role = config["roles"]["ticketer"]
    ticket_dashboard_id = config["channels"]["ticket_dashboard"]
=======
                
            return await interaction.response.send_message(f"Slow down! You can create a ticket again in {convert_seconds(retry)}", ephemeral=True)
        
        embedTypeSelector = discord.Embed(description="To assist you further, tell us why you are creating a ticket.", color=0xb50000)
        await interaction.response.send_message(embed=embedTypeSelector, view=TicketTypeSelector(), ephemeral=True)

class TicketTypeSelector(discord.ui.View):
    ticket_category_id = config['categories']['ticket']
    ticket_role = config['roles']['ticketer']
    ticket_dashboard_id = config['channels']['ticket_dashboard']
>>>>>>> e200e1035f2a61a8df79874c40551ca6c26cbd3d

    types = [
        discord.SelectOption(
            label="Questions",
            value="question",
            description="Want to clarify something?",
            emoji="❔",
        ),
        discord.SelectOption(
            label="Report",
            value="report",
            description="To report a misbehaving user or broken features.",
            emoji="❕",
        ),
        discord.SelectOption(
            label="Appeal",
            value="appeal",
            description="If you want to file an appeal for a moderation activity.",
            emoji="📄",
        ),
    ]

    @discord.ui.select(placeholder="What's the ticket for?", options=types)
    async def menu_callback(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):
        if select.values[0] == "question":
            await generate(self, interaction, type="question")
        if select.values[0] == "report":
            await generate(self, interaction, type="report")
        if select.values[0] == "appeal":
            await generate(self, interaction, type="appeal")


class ReportTypeSelector(discord.ui.View):
<<<<<<< HEAD
    def __init__(self):
        super().__init__(timeout=None)

=======
    
>>>>>>> e200e1035f2a61a8df79874c40551ca6c26cbd3d
    types = [
        discord.SelectOption(label="A member", value="member"),
        discord.SelectOption(label="A staff", value="staff"),
        discord.SelectOption(label="A broken feature", value="feature"),
    ]
<<<<<<< HEAD

    @discord.ui.select(
        placeholder="Select the category that matches your report", options=types
    )
    async def menu_callback(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):
=======
    
    @discord.ui.select(placeholder="Select the category that matches your report", options=types)
    async def menu_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        select.disabled = True
>>>>>>> e200e1035f2a61a8df79874c40551ca6c26cbd3d
        divider = "<:Divider:1134737299515654198>" * 12
        bullet = "<:B1:1134737275318706278>"

        if select.values[0] == "member":
<<<<<<< HEAD
            embedFollowUp = discord.Embed(
                description=f"In order for us to help you resolve an issue with our player, please answer this form:\n{divider}\n{bullet}1. What is the username of the player you're reporting?\n{bullet}2. Describe the behavior or actions of the player you're reporting.\n{bullet}3. Do you have any evidence (screenshots, videos) to support your report?",
                color=0xB50000,
            )
            await interaction.response.send_message(embed=embedFollowUp)
        if select.values[0] == "staff":
            embedFollowUp = discord.Embed(
                description=f"In order for us to help you resolve an issue with our staff, please answer this form:\n{divider}\n{bullet}1. What is the username of the staff member you're reporting?\n{bullet}2. Explain the situation and why you believe the staff member's actions were inappropriate.\n{bullet}3. Do you have any evidence (logs, screenshots, etc.) to back up your report?",
                color=0xB50000,
            )
            await interaction.response.send_message(embed=embedFollowUp)
        if select.values[0] == "feature":
            embedFollowUp = discord.Embed(
                description=f"We appreciate your help in making the server features better.\nIn order for us to assist your, please answer this form:\n{divider}\n{bullet}1. Describe the issue you're experiencing in detail.\n{bullet}2. Can you provide the steps to reproduce the issue?\n{bullet}3. Have you tried any steps to resolve the issue on your own? If yes, what were the results?",
                color=0xB50000,
            )
=======
            embedFollowUp = discord.Embed(description=f"In order for us to help you resolve an issue with our player, please answer this form:\n{divider}\n{bullet}1. What is the username of the player you're reporting?\n{bullet}2. Describe the behavior or actions of the player you're reporting.\n{bullet}3. Do you have any evidence (screenshots, videos) to support your report?", color=0xb50000)
            await interaction.response.send_message(embed=embedFollowUp)
        if select.values[0] == "staff":
            embedFollowUp = discord.Embed(description=f"In order for us to help you resolve an issue with our staff, please answer this form:\n{divider}\n{bullet}1. What is the username of the staff member you're reporting?\n{bullet}2. Explain the situation and why you believe the staff member's actions were inappropriate.\n{bullet}3. Do you have any evidence (logs, screenshots, etc.) to back up your report?", color=0xb50000)
            await interaction.response.send_message(embed=embedFollowUp)
        if select.values[0] == "feature":
            embedFollowUp = discord.Embed(description=f"We appreciate your help in making the server features better.\nIn order for us to assist your, please answer this form:\n{divider}\n{bullet}1. Describe the issue you're experiencing in detail.\n{bullet}2. Can you provide the steps to reproduce the issue?\n{bullet}3. Have you tried any steps to resolve the issue on your own? If yes, what were the results?", color=0xb50000)
>>>>>>> e200e1035f2a61a8df79874c40551ca6c26cbd3d
            await interaction.response.send_message(embed=embedFollowUp)


class AppealTypeSelector(discord.ui.View):
<<<<<<< HEAD
    def __init__(self):
        super().__init__(timeout=None)

=======
    
>>>>>>> e200e1035f2a61a8df79874c40551ca6c26cbd3d
    types = [
        discord.SelectOption(label="I have been kicked", value="kicked"),
        discord.SelectOption(label="I have been banned", value="banned"),
    ]

    @discord.ui.select(placeholder="What is this appeal for?", options=types)
    async def menu_callback(self, interaction: discord.Interaction, select):
        select.disabled = True
        divider = "<:Divider:1134737299515654198>" * 12
        bullet = "<:B1:1134737275318706278>"

        if select.values[0] == "kicked":
<<<<<<< HEAD
            embedFollowUp = discord.Embed(
                description=f"We're open to hearing your opinion on the said action.\nIf you think it was unjust, fill up this form:\n{divider}\n{bullet}1. Why were you kicked from the server?\n{bullet}2. Do you think this was an unlawful act by our staff?\n{bullet}3. Is there anything else you'd like to add to support your appeal?\n{bullet}4. Lastly, can you send us the Case ID for your issue and the name of the responsible staff. (Check the footer of the notice that was sent to your DMs)",
                color=0xB50000,
            )
            await interaction.response.send_message(embed=embedFollowUp)
        if select.values[0] == "banned":
            embedFollowUp = discord.Embed(
                description=f"We're open to hearing your opinion on the said action.\nIf you think it was unjust, fill up this form:\n{divider}\n{bullet}1. Why were you kicked from the server?\n{bullet}2. Do you think this was an unlawful act by our staff?\n{bullet}3. Is there anything else you'd like to add to support your appeal?\n{bullet}4. Lastly, can you send us the Case ID for your issue and the name of the responsible staff. (Check the footer of the notice that was sent to your DMs)",
                color=0xB50000,
            )
=======
            embedFollowUp = discord.Embed(description=f"We're open to hearing your opinion on the said action.\nIf you think it was unjust, fill up this form:\n{divider}\n{bullet}1. Why were you kicked from the server?\n{bullet}2. Do you think this was an unlawful act by our staff?\n{bullet}3. Is there anything else you'd like to add to support your appeal?\n{bullet}4. Lastly, can you send us the Case ID for your issue and the name of the responsible staff. (Check the footer of the notice that was sent to your DMs)", color=0xb50000)
            await interaction.response.send_message(embed=embedFollowUp)
        if select.values[0] == "banned":
            embedFollowUp = discord.Embed(description=f"We're open to hearing your opinion on the said action.\nIf you think it was unjust, fill up this form:\n{divider}\n{bullet}1. Why were you kicked from the server?\n{bullet}2. Do you think this was an unlawful act by our staff?\n{bullet}3. Is there anything else you'd like to add to support your appeal?\n{bullet}4. Lastly, can you send us the Case ID for your issue and the name of the responsible staff. (Check the footer of the notice that was sent to your DMs)", color=0xb50000)
>>>>>>> e200e1035f2a61a8df79874c40551ca6c26cbd3d
            await interaction.response.send_message(embed=embedFollowUp)


class StarupSettings(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Close Ticket",
        style=discord.ButtonStyle.red,
        custom_id="close:red",
        emoji="🗑️",
    )
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        embedConfirmation = discord.Embed(
            description="Are you sure you want to close this ticket?", color=0xFF0000
        )
        await interaction.response.send_message(
            embed=embedConfirmation, ephemeral=True, view=CloseConfirmation()
        )


class Settings(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Close Ticket",
        style=discord.ButtonStyle.red,
        custom_id="close:red",
        emoji="🗑️",
    )
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        embedConfirmation = discord.Embed(
            description="Are you sure you want to close this ticket?", color=0xFF0000
        )
        await interaction.response.send_message(
            embed=embedConfirmation, ephemeral=True, view=CloseConfirmation()
        )

    @discord.ui.button(
        label="Create Transcript",
        style=discord.ButtonStyle.blurple,
        custom_id="transcript:blurple",
        emoji="🖨️",
    )
    async def transcript(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        channel = interaction.channel
        dashboard = discord.utils.get(
            interaction.guild.channels, id=self.ticket_dashboard_id
        )

        await interaction.response.defer()

        if os.path.exists(f"./extras/transcripts/{interaction.channel.id}.md"):
            return await interaction.followup.send(
                f"A transcript has already been generated", ephemeral=True
            )
        with open(
            f"./extras/transcripts/{interaction.channel.id}.md", "a", encoding="utf-8"
        ) as f:
            f.write(f"# Transcript of {interaction.channel.name}:\n\n")
            async for message in channel.history(limit=None, oldest_first=True):
                created = datetime.strftime(message.created_at, "%m/%d/%Y at %H:%M")
                if message.edited_at:
                    edited = datetime.strftime(message.edited_at, "%m/%d/%Y at %H:%M")
                    f.write(
                        f"{message.author} on {created}: {message.clean_content} (Edited at {edited})\n"
                    )
                else:
                    f.write(f"{message.author} on {created}: {message.clean_content}\n")

            generated = datetime.now().strftime("%m/%d/%Y at %H:%M")
            f.write(
                f"\n*Generated at {generated}*, this transcript was requested by {interaction.user}*"
            )

        with open(f"./extras/transcripts/{interaction.channel.id}.md", "rb") as f:
            await interaction.followup.send(
                file=discord.File(
                    f, f"./extras/transcripts/{interaction.channel.id}.md"
                )
            )

        async def delete_transcript():
            await asyncio.sleep(120)
            os.remove(f"./extras/transcripts/{interaction.channel.id}.md")

        asyncio.ensure_future(delete_transcript())


class CloseConfirmation(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.ticket_dashboard_id = config["channels"]["ticket_dashboard"]

    @discord.ui.button(
        label="Cancel", style=discord.ButtonStyle.gray, custom_id="cancel:gray"
    )
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(
        label="Confirm",
        style=discord.ButtonStyle.danger,
        custom_id="confirmclose:danger",
    )
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        embedAction = discord.Embed(
            description="Ticket is being deleted.", color=0xFF0000
        )
        dashboard = discord.utils.get(
            interaction.guild.channels, id=self.ticket_dashboard_id
        )
        await interaction.response.send_message(embed=embedAction, ephemeral=True)

        if os.path.exists(f"./extras/transcripts/{interaction.channel.id}.md"):
            return await interaction.followup.send(
                f"A transcript has already been generated", ephemeral=True
            )
        with open(
            f"./extras/transcripts/{interaction.channel.id}.md", "a", encoding="utf-8"
        ) as f:
            f.write(f"# Transcript of {interaction.channel.name}:\n\n")
            async for message in interaction.channel.history(
                limit=None, oldest_first=True
            ):
                created = datetime.strftime(message.created_at, "%m/%d/%Y at %H:%M")
                if message.edited_at:
                    edited = datetime.strftime(message.edited_at, "%m/%d/%Y at %H:%M")
                    f.write(
                        f"{message.author} on {created}: {message.clean_content} (Edited at {edited})\n"
                    )
                else:
                    f.write(f"{message.author} on {created}: {message.clean_content}\n")

            generated = datetime.now().strftime("%m/%d/%Y at %H:%M")
            f.write(
                f"\n*Generated at {generated}*, this transcript was automatically generated.*"
            )

        await ticketDashboard(
            interaction=interaction, claimStatus="Closed", type="None"
        )
        with open(f"./extras/transcripts/{interaction.channel.id}.md", "rb") as f:
            await dashboard.send(
                file=discord.File(
                    f, f"./extras/transcripts/{interaction.channel.id}.md"
                )
            )
            os.remove(f"./extras/transcripts/{interaction.channel.id}.md")

        await asyncio.sleep(5)
        await interaction.channel.delete()
<<<<<<< HEAD
        guild = interaction.guild

        embedFeedback = discord.Embed(
            title="Ticket Closed",
            description=f"Hey there!\nYour ticket `{interaction.channel.name}` has been closed.\n\nTo further help us improve our ticketing system, we would love to hear your feedback. This would help us create a better support system. Thanks!",
        )

        await interaction.user.send(embed=embedFeedback, view=Feedback(guild=guild))


class closedButtons(discord.ui.View):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(timeout=None)
        self.interaction = interaction

        @discord.ui.button(
            label="Open Transcript",
            style=discord.ButtonStyle.link,
            custom_id="cB:trans:link",
        )
        async def transcript(self, interaction: discord.Interaction):
            ticketID = self.interaction.channel.id

            if os.path.exists(f"./extras/transcripts/{ticketID}.md"):
                with open(
                    f"./extras/transcripts/{interaction.channel.id}.md", "rb"
                ) as f:
                    file = discord.File(file=f)

                    embedSending = discord.Embed(
                        description="File is being generated, it will be directly sent to you in a moment.",
                        color=0xB50000,
                    )
                    await interaction.response.send_message(
                        embed=embedSending, ephemeral=True
                    )
                    await interaction.user.send(file=file)
            else:
                embedError = discord.Embed(
                    description="Transcript was not found, it may have been deleted.",
                    color=0xB50000,
                )
                await interaction.response.send_message(
                    embed=embedError, ephemeral=True
                )


class Feedback(discord.ui.View):
    def __init__(self, guild):
        super().__init__(timeout=None)
        self.guild = guild

    @discord.ui.button(
        label="Write a feedback",
        style=discord.ButtonStyle.blurple,
        custom_id="feedback:blurple",
    )
    async def write(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FeedbackModal(guild=self.guild))


async def feedbackDashboard(
    guild: discord.Interaction, feedback, interaction: discord.Interaction, rating
):
    channel = config["channels"]["feedback_dashboard"]
    userName = interaction.user.name
    dashboard = discord.utils.get(guild.channels, id=channel)

    rate = rating * "<:B5:1134737294453129317>"
    embed = discord.Embed(
        description=f"{feedback}\n\nRating:{rate}",
        color=0xB50000,
        timestamp=datetime.now(),
    )

    embed.set_author(name=userName, icon_url=interaction.user.avatar)

    await dashboard.send(embed=embed)


class FeedbackModal(discord.ui.Modal, title="Send us your feedback"):
    def __init__(
        self, title="Send us your feedback", guild: discord.Interaction = None
    ):
        super().__init__(title=title)
        self.guild = guild

    feedback = discord.ui.TextInput(
        label="Feedback",
        placeholder="Let us know how well we did",
        style=discord.TextStyle.long,
    )

    async def on_submit(self, interaction: Interaction):
        embedSuccess = discord.Embed(
            description="Your opinion matters to us, rest assured that this feedback will be used to improve our support system.\n\nRate your experience to complete your review.",
            color=0xB50000,
        )

        await interaction.response.send_message(
            embed=embedSuccess,
            view=feedbackRating(
                guild=self.guild, feedback=self.feedback.value, interaction=interaction
            ),
        )


class feedbackRating(discord.ui.View):
    def __init__(self, feedback, guild, interaction):
        super().__init__(timeout=None)
        self.feedback = feedback
        self.guild = guild

    options = [
        discord.SelectOption(
            label="Very Good",
            value=5,
            description="The issue was resolved exceptionally well, and the service provided exceeded expectations.",
        ),
        discord.SelectOption(
            label="Good",
            value=4,
            description="The issue was resolved satisfactorily, and the service provided was of a good standard.",
        ),
        discord.SelectOption(
            label="Ok",
            value=3,
            description="The resolution of the issue was average, meeting the basic requirements.",
        ),
        discord.SelectOption(
            label="Bad",
            value=2,
            description="The resolution of the issue was unsatisfactory, and improvements are needed in the service provided.",
        ),
        discord.SelectOption(
            label="Very Bad",
            value=1,
            description="The issue was not resolved effectively, and the service provided was extremely poor.",
        ),
    ]

    @discord.ui.select(placeholder="Rate our service", options=options)
    async def menu_callback(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):
        if select.values[0] == "5":
            await feedbackDashboard(
                guild=self.guild,
                feedback=self.feedback,
                rating=5,
                interaction=interaction,
            )
        if select.values[0] == "4":
            await feedbackDashboard(
                guild=self.guild,
                feedback=self.feedback,
                rating=4,
                interaction=interaction,
            )
        if select.values[0] == "3":
            await feedbackDashboard(
                guild=self.guild,
                feedback=self.feedback,
                rating=3,
                interaction=interaction,
            )
        if select.values[0] == "2":
            await feedbackDashboard(
                guild=self.guild,
                feedback=self.feedback,
                rating=2,
                interaction=interaction,
            )
        if select.values[0] == "1":
            await feedbackDashboard(
                guild=self.guild,
                feedback=self.feedback,
                rating=1,
                interaction=interaction,
            )

        embedSuccess = discord.Embed(
            description="Thank you for taking your time in helping us be better.",
            color=0xB50000,
        )

        await interaction.response.send_message(embed=embedSuccess)
=======
>>>>>>> e200e1035f2a61a8df79874c40551ca6c26cbd3d
