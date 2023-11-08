from datetime import datetime
import discord
import json
import asyncio

from discord.ext import commands

# Get's the logging channel info
with open("config.json", "r") as f:
    config = json.load(f)

modlogsID = config["channels"]["modlogs"]
announcement = config["channels"]["announcement"]
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class ModerationTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.limit = config["Limits"]["Purge"]

    @commands.has_any_role(1145295540549062696, 1134472355935178752)
    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def purge(self, ctx, amount):
        try:
            amount = int(amount)
        except ValueError:
            errorEmbed = discord.Embed(
                description="Please provide a valid integer for the amount argument.\nTry ``ftg.purge <amount (in numerical form)>``",
                color=0xB50000,
            )
            await ctx.send(embed=errorEmbed, delete_after=5)
            return

        if ctx.invoked_subcommand is None:
            try:
                await ctx.message.delete()
                if amount > self.limit:
                    embedError = discord.Embed(
                        description="The amount exceeds the limit. Do not exceed the limit to keep the bot running smoothly."
                    )
                    await ctx.send(embed=embedError)
                else:
                    # Load the JSON file containing the cases
                    with open("./extras/cases.json", "r") as f:
                        cases = json.load(f)

                    # Increment the case number
                    case_number = cases["total_count"] + 1

                    # Create a new case object
                    new_case = {
                        "ID": case_number,
                        "Responsible Staff": ctx.author.name,
                        "Activity": "Purge",
                        "Channel": ctx.channel.name,
                    }

                    # Append the new case to the cases list
                    cases["cases"].append(new_case)

                    # Update the case number in the JSON file
                    cases["total_count"] = case_number

                    # Save the JSON file
                    with open("./extras/cases.json", "w") as f:
                        json.dump(cases, f, indent=4)

                    try:
                        # Attempt to use bulk deletion
                        deletedAmount = await ctx.channel.purge(limit=amount)
                    except discord.errors.HTTPException:
                        # If bulk deletion fails (messages older than 14 days), resort to manual deletion
                        older_than_14_days = []
                        async for message in ctx.channel.history(limit=amount):
                            if (datetime.now() - message.created_at).days > 14:
                                older_than_14_days.append(message)
                            if len(older_than_14_days) >= amount:
                                break

                        # Delete messages older than 14 days manually
                        for message in older_than_14_days:
                            try:
                                asyncio.sleep(1.5)
                                await message.delete()
                            except discord.errors.RateLimited:
                                errorEmbed = discord.Embed(
                                    description="We are being rate limited.",
                                    color=0xB50000,
                                )
                                await ctx.send(embed=errorEmbed)

                        deletedAmount = older_than_14_days

                    embedAction = discord.Embed(
                        description=f"Deleted {len(deletedAmount)} messages in this channel",
                        color=0xF50000,
                    )
                    await ctx.send(embed=embedAction, delete_after=5)

                    # Log the moderation activity
                    modlogs = self.bot.get_channel(int(modlogsID))
                    embedLog = discord.Embed(color=0xB50000, timestamp=datetime.now())
                    embedLog.add_field(
                        name="<:Empty:1134737303324065873>",
                        value=f"<:Empty:1134737303324065873><:SBM:1134737397746257940> Activity: Deleted {len(deletedAmount)} in  {ctx.channel.mention}\n<:Empty:1134737303324065873><:SBM:1134737397746257940> Staff Responsible: {ctx.author.mention}",
                    )
                    embedLog.set_author(name="Automatic Logging System")
                    embedLog.set_footer(text=f"Case ID: {case_number}")
                    await modlogs.send(embed=embedLog)

            except discord.errors.RateLimited:
                errorEmbed = discord.Embed(
                    description="We are being rate limited.", color=0xB50000
                )
                await ctx.send(embed=errorEmbed)
            except discord.errors.NotFound:
                errorEmbed = discord.Embed(
                    description="Some messages could not be found and were not deleted.",
                    color=0xB50000,
                )
                await ctx.send(embed=errorEmbed)
        else:
            pass

    @purge.command()
    async def member(self, ctx, member: discord.Member, amount: int):
        await ctx.message.delete()

        member_messages = []
        async for message in ctx.channel.history(limit=None):
            if message.author == member:
                member_messages.append(message)

        if member_messages:
            # Load the JSON file containing the cases
            with open("./extras/cases.json", "r") as f:
                cases = json.load(f)

            # Increment the case number
            case_number = cases["total_count"] + 1

            # Create a new case object
            new_case = {
                "ID": case_number,
                "Responsible Staff": ctx.author.name,
                "Activity": "Purge Member Message",
                "Channel": ctx.channel.name,
                "Member": member.name,
                "Time": current_time,
            }

            # Append the new case to the cases list
            cases["cases"].append(new_case)

            # Update the case number in the JSON file
            cases["total_count"] = case_number

            # Save the JSON file
            with open("./extras/cases.json", "w") as f:
                json.dump(cases, f, indent=4)

            try:
                # Collect the messages that need to be deleted
                deletedAmount = [message for message in member_messages[:amount]]
                await ctx.channel.delete_messages(deletedAmount)

                embedAction = discord.Embed(
                    description=f"Deleted {len(deletedAmount)} messages of {member.display_name} in this channel",
                    color=0xB50000,
                )
                await ctx.send(embed=embedAction, delete_after=5)
            except discord.errors.HTTPException as e:
                if "can only bulk delete messages that are under 14 days old" in str(e):
                    # Handle the error when messages are over 14 days old
                    errorEmbed = discord.Embed(
                        description="You can only bulk delete messages that are under 14 days old.",
                        color=0xB50000,
                    )
                    await ctx.send(embed=errorEmbed, delete_after=5)

            # Log the moderation activity
            channel = self.bot.get_channel(modlogsID)
            embedLog = discord.Embed(color=0xB50000, timestamp=datetime.now())
            embedLog.add_field(
                name="<:Empty:1134737303324065873>",
                value=f"<:Empty:1134737303324065873><:SBM:1134737397746257940> Activity: Deleted {len(deletedAmount)} of {member.name} in {ctx.channel.mention}\n<:Empty:1134737303324065873><:SBM:1134737397746257940> Staff Responsible: {ctx.author.name}",
            )
            embedLog.set_author(name="Automatic Logging System")
            embedLog.set_footer(text=f"Case ID: {case_number}")
            await channel.send(embed=embedLog)
        else:
            embedAction = discord.Embed(
                description=f"{member.display_name} has not sent any messages in this channel",
                color=0xB50000,
            )
            await ctx.send(embed=embedAction, delete_after=5)

    @purge.command()
    async def bot(self, ctx, amount: int):
        def is_bot_message(message):
            return message.author == self.bot.user

        # Load the JSON file containing the cases
        with open("./extras/cases.json", "r") as f:
            cases = json.load(f)

            # Increment the case number
            case_number = cases["total_count"] + 1

            # Create a new case object
            new_case = {
                "ID": case_number,
                "Responsible Staff": ctx.author.name,
                "Activity": "Purge Bot Message",
                "Channel": ctx.channel.name,
                "Time": current_time,  # Ensure current_time is defined
            }

            # Append the new case to the cases list
            cases["cases"].append(new_case)

            # Update the case number in the JSON file
            cases["total_count"] = case_number

            # Save the JSON file
            with open("./extras/cases.json", "w") as f:
                json.dump(cases, f, indent=4)

        deletedAmount = []
        bot_messages = []

        async for message in ctx.channel.history(limit=None):
            if is_bot_message(message):
                bot_messages.append(message)
                if len(bot_messages) >= amount:
                    break

        if bot_messages:
            try:
                await ctx.channel.delete_messages(bot_messages)
                deletedAmount.extend(bot_messages)
            except discord.errors.RateLimited:
                errorEmbed = discord.Embed(
                    description="We are being rate limited. Retrying...",
                    color=0xB50000,
                )
                await ctx.send(embed=errorEmbed)
                await asyncio.sleep(5)

        embedAction = discord.Embed(
            description=f"Deleted {len(deletedAmount)} messages of the bot in this channel",
            color=0xB50000,
        )
        await ctx.send(embed=embedAction, delete_after=5)

    ### Punishment System ###
    @commands.command()
    @commands.has_any_role(1145295540549062696, 1134472355935178752)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason was provided"):
        if member == ctx.author:
            embedError = discord.Embed(
                description="Error! You cannot kick yourself!", color=0xFF0000
            )

            await ctx.send(embed=embedError, delete_after=3)
        else:
            await ctx.message.delete()
            # Load the JSON file containing the cases
            with open("./extras/cases.json", "r") as f:
                cases = json.load(f)

            # Increment the case number
            case_number = cases["total_count"] + 1

            # Create a new case object
            new_case = {
                "ID": case_number,
                "Responsible Staff": ctx.author.name,
                "User": member.name,
                "Activity": "Kicked",
                "Reason": reason,
                "Time": current_time,
            }

            # Append the new case to the cases list
            cases["cases"].append(new_case)

            # Update the case number in the JSON file
            cases["total_count"] = case_number

            # Save the JSON file
            with open("./extras/cases.json", "w") as f:
                json.dump(cases, f, indent=4)

            # Load the JSON file containing the warnings
            with open("./extras/warnings.json", "r") as f:
                warnings = json.load(f)

            # Send a kick notice to the member
            embedNotice = discord.Embed(
                description=f"Hey there {member.name}!\n\nThis message is sent to make you aware of the action we've made.\nYou have been removed from the server for violating our community guidelines.\n\nWe take the safety and well-being of our community seriously. Please respect our rules and guidelines to ensure a positive and enjoyable experience for all members.\n\nIf you were removed from the server and believe it was unjust, you can file an appeal ticket on our server for reinstatement. Provide a clear explanation and any supporting evidence. We take moderation actions seriously and will not entertain frivolous appeals. Our team will review and make a decision as soon as possible.\n\nHere's the reason why you were kicked:\n<:Empty:1134737303324065873><:SBM:1134737397746257940> {reason}",
                color=0xB50000,
                timestamp=datetime.now(),
            )
            embedNotice.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)
            embedNotice.set_footer(
                text=f"Case ID: {case_number} • Responsible Staff : {ctx.author.name}"
            )

            await member.send(embed=embedNotice)

            # Sends a message on the channel and kicks the member
            embedAction = discord.Embed(
                description=f"{member.name} has been removed from the server for violating our community guidelines.",
                color=0xF50000,
            )
            await ctx.send(embed=embedAction, delete_after=5)
            await member.kick(reason=reason)

            # Log the moderation activity
            modlogs = self.bot.get_channel(int(modlogsID))
            sbt = "<:Empty:1134737303324065873><:SBM:1134737397746257940>"
            sbm = "<:Empty:1134737303324065873><:SBM:1134737397746257940>"
            sbb = "<:Empty:1134737303324065873><:SBB:1134737393921036348>"

            if member.id in warnings:
                totalWarnings = (
                    f"{warnings[str(member.id)]['WarningCount']}" + " Infractions"
                )
            else:
                totalWarnings = "No Active Infractions"

            embedLog = discord.Embed(color=0xB50000, timestamp=datetime.now())
            embedLog.set_author(name=f"Automatic Logging System")
            embedLog.add_field(
                name="<:Empty:1134737303324065873>",
                value=f"{sbt} Activity: User Kicked\n{sbm} Username: {member.display_name}\n{sbm} User ID: {member.id}\n{sbm}Total Warnings of User: {totalWarnings}\n{sbm}Staff Responsible: {ctx.author.name}\n{sbb}Reason: {reason}",
            )
            embedLog.set_footer(text=f"Case ID: {case_number}")
            await modlogs.send(embed=embedLog)

    @commands.command()
    @commands.has_any_role(1145295540549062696, 1145345878777925763, 1145295915159138334, 1145296297058910269)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason was provided"):
        await ctx.message.delete()
        if member == ctx.author:
            embedError = discord.Embed(
                description="Error! You cannot ban yourself!", color=0xFF0000
            )

            await ctx.send(embed=embedError, delete_after=3)
        else:

            # Load the JSON file containing the cases
            with open("./extras/cases.json", "r") as f:
                cases = json.load(f)

            with open("./extras/warnings.json", "r") as f:
                warnings = json.load(f)

            # Increment the case number
            case_number = cases["total_count"] + 1

            # Create a new case object
            new_case = {
                "ID": case_number,
                "Responsible Staff": ctx.author.name,
                "User": member.name,
                "Activity": "Banned",
                "Reason": reason,
                "Time": current_time,
            }

            # Append the new case to the cases list
            cases["cases"].append(new_case)

            # Update the case number in the JSON file
            cases["total_count"] = case_number

            # Save the JSON file
            with open("./extras/cases.json", "w") as f:
                json.dump(cases, f, indent=4)

            # Send a ban notice to the member
            embedNotice = discord.Embed(
                description=f"Hey there {member.name}!\n\nThis message is sent to make you aware of the action we've made.\nYou have been banned from the server for violating our community guidelines.\n\nWe take the safety and well-being of our community seriously. Please respect our rules and guidelines to ensure a positive and enjoyable experience for all members.\n\nIf you were removed from the server and believe it was unjust, you can [submit an appeal](https://forms.gle/M6yTr78DkMycVpSY7) for reinstatement. Provide a clear explanation and any supporting evidence. We take moderation actions seriously and will not entertain frivolous appeals. Our team will review and make a decision as soon as possible.\n\nHere's the reason why you were banned:\n<:Empty:1134737303324065873><:SBM:1134737397746257940> {reason}",
                color=0xF50000,
                timestamp=datetime.now(),
            )
            embedNotice.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)
            embedNotice.set_footer(
                text=f"Case ID: {case_number} • Responsible Staff : {ctx.author.name}"
            )

            await member.send(embed=embedNotice)

            # Sends a message on the channel and bans the member
            embedAction = discord.Embed(
                description=f"{member.name} has been banned from the server for violating our community guidelines.",
                color=0xF50000,
            )
            await ctx.send(embed=embedAction, delete_after=3)
            await member.ban(reason=reason)

            # Log the moderation activity
            modlogs = self.bot.get_channel(int(modlogsID))
            sbt = "<:Empty:1134737303324065873><:SBM:1134737397746257940>"
            sbm = "<:Empty:1134737303324065873><:SBM:1134737397746257940>"
            sbb = "<:Empty:1134737303324065873><:SBB:1134737393921036348>"

            if member.id in warnings:
                totalWarnings = (
                    f"{warnings[str(member.id)]['WarningCount']}" + " Infractions"
                )
            else:
                totalWarnings = "No Active Infractions"

            embedLog = discord.Embed(color=0xB50000, timestamp=datetime.now())
            embedLog.set_author(name=f"Automatic Logging System")
            embedLog.add_field(
                name="<:Empty:1134737303324065873>",
                value=f"{sbt} Activity: User Banned\n{sbm} Username: {member.display_name}\n{sbm} User ID: {member.id}\n{sbm}Total Warnings of User: {totalWarnings}\n{sbm}Staff Responsible: {ctx.author.name}\n{sbb}Reason: {reason}",
            )
            embedLog.set_footer(text=f"Case ID: {case_number}")
            await modlogs.send(embed=embedLog)

    @commands.command()
    @commands.has_any_role(1145295915159138334, 1145295540549062696, 1145345878777925763)
    async def unban(self, ctx, userID: int, *, reason: str = "No reason was provided."):
        await ctx.message.delete()
        # Attempt to get the banned user using the userID
        try:
            banned_user = await ctx.guild.fetch_ban(discord.Object(userID))
        except discord.NotFound:
            banned_user = None

        if banned_user is None:
            await ctx.send("User with that ID is not banned.")
            return

        # Load the JSON file containing the cases
        with open("./extras/cases.json", "r") as f:
            cases = json.load(f)

        # Increment the case number
        case_number = cases["total_count"] + 1

        # Create a new case object
        new_case = {
            "ID": case_number,
            "Responsible Staff": ctx.author.name,
            "User": banned_user.user.name,
            "Activity": "Unbanned",
            "Reason": reason,
            "Time": str(datetime.now()),
        }

        # Append the new case to the cases list
        cases["cases"].append(new_case)

        # Update the case number in the JSON file
        cases["total_count"] = case_number

        # Save the JSON file
        with open("./extras/cases.json", "w") as f:
            json.dump(cases, f, indent=4)

        # Sends a message on the channel and unbans the member
        await ctx.guild.unban(banned_user.user)

        # Log the unban activity
        modlogs = self.bot.get_channel(int(modlogsID))
        sbm = "<:Empty:1134737303324065873><:SBM:1134737397746257940>"
        sbb = "<:Empty:1134737303324065873><:SBB:1134737393921036348>"
        embedLog = discord.Embed(color=0xb50000, timestamp=datetime.now())
        embedLog.set_author(name=f"Automatic Logging System")
        embedLog.add_field(
            name="<:Empty:1134737303324065873>",
            value=f"{sbm} Activity: User Unbanned\n{sbm} Username: {banned_user.user.name}\n{sbm} User ID: {banned_user.user.id}\n{sbm} Staff Responsible: {ctx.author.mention}\n{sbb} Reason: {reason}",
        )
        embedLog.set_footer(text=f"Case ID: {case_number}")
        await modlogs.send(embed=embedLog)

    ### Warning System ###
    @commands.command()
    @commands.has_any_role(1145295540549062696, 1134472355935178752)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def warn(self, ctx, member: discord.Member, *, reason="No reason was provided"):
        if member == ctx.author:
            embedError = discord.Embed(
                description="Error! You cannot warn yourself!", color=0xFF0000
            )
            await ctx.send(embed=embedError, delete_after=3)
            return

        # Load the JSON file containing the cases
        with open("./extras/cases.json", "r") as f:
            cases = json.load(f)

        # Increment the case number
        case_number = cases["total_count"] + 1

        # Load the JSON file containing the warnings
        with open("./extras/warnings.json", "r") as f:
            warnings = json.load(f)

        # Checks if the member has existing warning
        if str(member.id) not in warnings:
            warnings[str(member.id)] = {"WarningCount": "0"}
            warnings[str(member.id)][
                "WarningCount"
            ] = "1"  # Set initial warning count to 1
            warning_number = warnings[str(member.id)]["WarningCount"]

            warnings[str(member.id)][warning_number] = {
                "Reason": reason,
                "Staff Responsible": ctx.author.name,
                "Time": str(datetime.now()),
            }
        elif str(member.id) in warnings:
            warning_number = warnings[str(member.id)]["WarningCount"]
            if int(warning_number) < 3:
                warnings[str(member.id)]["WarningCount"] = str(int(warning_number) + 1)

                # Increment the warning count and add the warning details
                warning_number = warnings[str(member.id)]["WarningCount"]

                warnings[str(member.id)][warning_number] = {
                    "Reason": reason,
                    "Staff Responsible": ctx.author.name,
                    "Time": str(datetime.now()),
                }
            else:
                modlogs = self.bot.get_channel(int(modlogsID))
                sbt = "<:Empty:1134737303324065873><:SBM:1134737397746257940>"
                sbm = "<:Empty:1134737303324065873><:SBM:1134737397746257940>"
                sbb = "<:Empty:1134737303324065873><:SBB:1134737393921036348>"

                if str(member.id) in warnings:
                    totalWarnings = (
                        f"{warnings[str(member.id)]['WarningCount']}" + " Infractions"
                    )
                else:
                    totalWarnings = "No Active Infractions"

                embed = discord.Embed(
                    description=f"{member.name} has been automatically kicked for reaching the amount of maximum infractions.",
                    color=0xB50000,
                )
                await ctx.send(embed=embed, delete_after=5)

                embedLog = discord.Embed(color=0xB50000, timestamp=datetime.now())
                embedLog.set_author(name=f"Automatic Logging System")
                embedLog.add_field(
                    name="<:Empty:1134737303324065873>",
                    value=f"{sbt} Activity: User Kicked\n{sbm} Username: {member.display_name}\n{sbm} User ID: {member.id}\n{sbm}Total Warnings of User: {totalWarnings}\n{sbm}Staff Responsible: {ctx.author.name}\n{sbb}Reason: Reached the maximum amount of Infractions.",
                )
                embedLog.set_footer(text=f"Case ID: {case_number}")
                await modlogs.send(embed=embedLog)

                embedNotice = discord.Embed(
                    description=f"Hey there {member.name}!\n\nThis message is sent to make you aware of the action we've made.\nYou have been automatically kicked from the server for reaching the maximum amount of violations in our community guidelines.\n\nWe take the safety and well-being of our community seriously. Please respect our rules and guidelines to ensure a positive and enjoyable experience for all members.\n\nIf you were removed from the server and believe it was unjust, you can file an appeal ticket on our server for reinstatement. Provide a clear explanation and any supporting evidence. We take moderation actions seriously and will not entertain frivolous appeals. Our team will review and make a decision as soon as possible.\n\nHere's the reason why you were automatically been kicked:\n<:Empty:1134737303324065873><:SBM:1134737397746257940> {reason}",
                    color=0xB50000,
                    timestamp=datetime.now(),
                )
                embedNotice.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)
                embedNotice.set_footer(
                    text=f"Case ID: {case_number} • Responsible Staff : {ctx.author.name}"
                )

                await member.send(embed=embedNotice)

                await member.kick(reason=reason)

        # Save the JSON file
        with open("./extras/warnings.json", "w") as f:
            json.dump(warnings, f, indent=4)

            # Sends a message on the channel
            embedAction = discord.Embed(
                description=f"{member.mention} have been warned for the reason stated below\n\n**Reason**: {reason}",
                color=0xF50000,
            )
            await ctx.send(embed=embedAction, delete_after=5)

            # Log the moderation activity
            modlogs = self.bot.get_channel(int(modlogsID))
            sbt = "<:Empty:1134737303324065873><:SBM:1134737397746257940>"
            sbm = "<:Empty:1134737303324065873><:SBM:1134737397746257940>"
            sbb = "<:Empty:1134737303324065873><:SBB:1134737393921036348>"

            if str(member.id) in warnings:
                totalWarnings = (
                    f"{warnings[str(member.id)]['WarningCount']}" + " Infractions"
                )
            else:
                totalWarnings = "No Active Infractions"

            embedLog = discord.Embed(color=0xB50000, timestamp=datetime.now())
            embedLog.set_author(name=f"Automatic Logging System")
            embedLog.add_field(
                name="<:Empty:1134737303324065873>",
                value=f"{sbt} Activity: User Warned\n{sbm} Username: {member.display_name}\n{sbm} User ID: {member.id}\n{sbm}Total Warnings of User: {totalWarnings}\n{sbm}Staff Responsible: {ctx.author.name}\n{sbb}Reason: {reason}",
            )
            embedLog.set_footer(text=f"Case ID: {case_number}")
            await modlogs.send(embed=embedLog)

    @commands.command()
    @commands.has_any_role(1145295540549062696, 1145345878777925763, 1145295915159138334)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def clearwarnings(self, ctx, member: discord.Member):
        if member == ctx.author:
            embedError = discord.Embed(
                description="Error! You cannot clear your warnings!", color=0xFF0000
            )

            await ctx.send(embed=embedError, delete_after=3)
        else:
            await ctx.message.delete()
            # Load the JSON file containing the cases
            with open("./extras/cases.json", "r") as f:
                cases = json.load(f)

            # Increment the case number
            case_number = cases["total_count"] + 1

            # Create a new case object
            new_case = {
                "ID": case_number,
                "Responsible Staff": ctx.author.name,
                "User": member.name,
                "Activity": "Clear Warnings",
                "Time": current_time,
            }

            # Append the new case to the cases list
            cases["cases"].append(new_case)

            # Update the case number in the JSON file
            cases["total_count"] = case_number

            # Save the JSON file
            with open("./extras/cases.json", "w") as f:
                json.dump(cases, f, indent=4)

            # Load the JSON file containing the warnings
            with open("./extras/warnings.json", "r") as f:
                warnings = json.load(f)

            # Sends a message on the channel and clear all the warnings of the member
            if str(member.id) not in warnings:
                await ctx.send("This user has no warnings.")
                return

            del warnings[str(member.id)]
            with open("./extras/warnings.json", "w") as f:
                json.dump(warnings, f)

            embedAction = discord.Embed(
                description=f"All warnings of {member.mention} have been cleared.",
                timestamp=datetime.now(),
            )
            await ctx.send(embed=embedAction, delete_after=5)

            # Log the moderation activity
            modlogs = self.bot.get_channel(int(modlogsID))
            sbt = "<:Empty:1134737303324065873><:SBM:1134737397746257940>"
            sbm = "<:Empty:1134737303324065873><:SBM:1134737397746257940>"
            sbb = "<:Empty:1134737303324065873><:SBB:1134737393921036348>"

            if member.id in warnings:
                totalWarnings = (
                    f"{warnings[str(member.id)]['WarningCount']}" + " Infractions"
                )
            else:
                totalWarnings = "No Active Infractions"

            embedLog = discord.Embed(color=0xB50000, timestamp=datetime.now())
            embedLog.set_author(name=f"Automatic Logging System")
            embedLog.add_field(
                name="<:Empty:1134737303324065873>",
                value=f"{sbm} Activity: Cleared Warnings for {member.name}\n{sbb}Staff Responsible: {ctx.author.name}",
            )
            embedLog.set_footer(text=f"Case ID: {case_number}")

            await modlogs.send(embed=embedLog)

    @commands.command(aliases=["warnings", "checkwarns", "warns"])
    @commands.has_any_role(1145295540549062696, 1134472355935178752)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def checkwarnings(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        # Load warnings data
        with open("./extras/warnings.json", "r") as f:
            warnings = json.load(f)

        # Check if member is not mentioned or is the author
        if member is None or member == ctx.author:
            author_id = str(ctx.author.id)
            if author_id not in warnings:
                embedCount = discord.Embed(
                    description=f"You currently have no warnings.", color=0xB50000
                )
            else:
                count = warnings[author_id]["WarningCount"]
                embedCount = discord.Embed(
                    description=f"You currently have a total of {count} warning(s).",
                    color=0xB50000,
                )

            await ctx.send(embed=embedCount, delete_after=5)
        else:
            member_id = str(member.id)
            if member_id not in warnings:
                embedCount = discord.Embed(
                    description=f"{member.name} currently has no warnings.",
                    color=0xB50000,
                )
            else:
                count = warnings[member_id]["WarningCount"]
                embedCount = discord.Embed(
                    description=f"{member.name} has a total of {count} warning(s).",
                    color=0xB50000,
                )

            await ctx.send(embed=embedCount, delete_after=5)

    ### Lockdown System ###
    @commands.command(aliases=["lockserver"])
    @commands.has_any_role(1145295540549062696, 1145345878777925763)
    async def lockdown(self, ctx):
        # Load the JSON file containing the cases
        with open("./extras/cases.json", "r") as f:
            cases = json.load(f)

        # Increment the case number
        case_number = cases["total_count"] + 1

        # Create a new case object
        new_case = {
            "ID": case_number,
            "Responsible Staff": ctx.author.name,
            "Status": "Server Lockdown",
            "Time": current_time,
        }

        # Append the new case to the cases list
        cases["cases"].append(new_case)

        # Update the case number in the JSON file
        cases["total_count"] = case_number

        # Save the JSON file
        with open("./extras/cases.json", "w") as f:
            json.dump(cases, f, indent=4)

        # Load the config file and gets all the channel in ChannelsToLock key in a lockdown mode
        with open("config.json") as f:
            config = json.load(f)
        channels_to_lock = config["ChannelsToLock"]

        # For general channels
        for channel_id in channels_to_lock:
            channel = ctx.guild.get_channel(int(channel_id))
            if channel is None:
                continue

            verifiedID = discord.utils.get(ctx.guild.roles, id=1145298592173662269)
            overwrite = channel.overwrites_for(verifiedID)
            overwrite.send_messages = False
            overwrite.view_channel = False
            await channel.set_permissions(verifiedID, overwrite=overwrite)

        # For community specific channels
        valoChannel = ctx.guild.get_channel(1160034512785387540)
        valoScrims = ctx.guild.get_channel(1160519497711628370)

        codmChannel = ctx.guild.get_channel(1160034543286366338)
        codmScrims = ctx.guild.get_channel(1160519716201300029)

        mlChannel = ctx.guild.get_channel(1160034580531785889)
        mlScrims = ctx.guild.get_channel(1160519812313792574)

        await channel.set_permissions(overwrite=overwrite)

        # Sends a message on the announcement channel
        channel = self.bot.get_channel(announcement)
        embedAction = discord.Embed(
            description="**Attention** @everyone,\n\nOur server is currently in lockdown mode.\nAccess to certain channels and features may be restricted.\nThis is for the safety and security of the community.\n\nPlease follow any instructions from the server administrators and stay updated on the situation. \n\nThank you for your understanding and cooperation.\n\n- Management",
            color=0xFF0000,
        )
        await channel.send(embed=embedAction)

        # Log the moderation activity
        modlogs = self.bot.get_channel(int(modlogsID))
        embedLog = discord.Embed(color=0x000000, timestamp=datetime.now())
        embedLog.set_author(
            name="Lockdown mode has been enabled.", icon_url=ctx.guild.icon
        )
        embedLog.set_footer(text=f"Case ID: {case_number}")

        await modlogs.send(embed=embedLog)

    @commands.command(aliases=["unlockdown", "liftlock"])
    @commands.has_any_role(1145295540549062696, 1145345878777925763)
    async def unlock(self, ctx):
        # Load the JSON file containing the cases
        with open("./extras/cases.json", "r") as f:
            cases = json.load(f)

        # Increment the case number
        case_number = cases["total_count"] + 1

        # Create a new case object
        new_case = {
            "ID": case_number,
            "Responsible Staff": ctx.author.name,
            "Status": "Lockdown Lifted",
            "Time": current_time,
        }

        # Append the new case to the cases list
        cases["cases"].append(new_case)

        # Update the case number in the JSON file
        cases["total_count"] = case_number

        # Save the JSON file
        with open("./extras/cases.json", "w") as f:
            json.dump(cases, f, indent=4)

        # Load the config file and gets all the channel in ChannelsToLock key in a lockdown mode
        with open("config.json") as f:
            config = json.load(f)
        channels_to_lock = config["ChannelsToLock"]

        for channel_id in channels_to_lock:
            channel = ctx.guild.get_channel(int(channel_id))
            if channel is None:
                continue

            verifiedID = discord.utils.get(ctx.guild.roles, id=1145298592173662269)
            overwrite = channel.overwrites_for(verifiedID)
            overwrite.send_messages = True
            overwrite.view_channel = True
            await channel.set_permissions(verifiedID, overwrite=overwrite)

        # Sends a message on the announcement channel
        channel = self.bot.get_channel(announcement)
        embedAction = discord.Embed(
            description="**Attention** @everyone,\n\nGreat news! The server's lockdown status has been lifted.\nAccess to certain channels and features has now been given back.\n\nWe promise to get back to you as soon as possible.\n\nnWe thank you for your understanding and cooperation.\n\n- Management",
            color=0xFFFFFF,
        )
        await channel.send(embed=embedAction)

        # Log the moderation activity
        modlogs = self.bot.get_channel(int(modlogsID))
        embedLog = discord.Embed(color=0xFFFFFFF, timestamp=datetime.now())
        embedLog.set_author(
            name="Lockdown mode has been lifted.", icon_url=ctx.guild.icon
        )
        embedLog.set_footer(text=f"Case ID: {case_number}")

        await modlogs.send(embed=embedLog)

    @commands.command()
    @commands.has_any_role(1145295540549062696, 1134472355935178752)
    async def announce(self, ctx, channel: discord.TextChannel, *, message):
        embed = discord.Embed(description=f"{message}", color=0xB50000)

        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ModerationTools(bot))
