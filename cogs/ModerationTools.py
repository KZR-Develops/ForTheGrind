from datetime import datetime
import discord
import json
import asyncio

from discord.ext import commands

# Get's the logging channel info
with open("config.json", "r") as f:
    config = json.load(f)

<<<<<<< HEAD
modlogsID = config["channels"]["modlogs"]
announcement = config["channels"]["announcement"]
=======
modlogsID = config['channels']['modlogs']
announcement = config['channels']['announcement']
>>>>>>> e200e1035f2a61a8df79874c40551ca6c26cbd3d
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class ModerationTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.limit = config["Limits"]["Purge"]

    @commands.command(aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
<<<<<<< HEAD
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def purge(self, ctx, amount: int, member: discord.Member = None):
        try:
            await ctx.message.delete()
            if amount > int(self.limit):
                embedError = discord.Embed(
                    description="The amount exceeds the limit. Do not exceed the limit to keep the bot running smoothly."
                )

                await ctx.send(embed=embedError)
            else:
                if member is not None:
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

                        # Deletes x amount of messages and sends a message on the channel
                        deletedAmount = await ctx.channel.purge(
                            limit=amount, check=lambda m: m.author == member
                        )
                        embedAction = discord.Embed(
                            description=f"Deleted {len(deletedAmount)} messages of {member.display_name} in this channel",
                            color=0xB50000,
                        )
                        await ctx.send(embed=embedAction, delete_after=5)

                        # Log the moderation activity
                        channel = self.bot.get_channel(modlogsID)
                        embedLog = discord.Embed(
                            color=0xB50000, timestamp=datetime.now()
                        )
                        embedLog.add_field(
                            name="<:Empty:1134737303324065873>",
                            value=f"<:Empty:1134737303324065873><:SBM:1134737397746257940> Activity: Deleted {len(deletedAmount)} of {member.name} in  {ctx.channel.mention}\n<:Empty:1134737303324065873><:SBM:1134737397746257940> Staff Responsible: {ctx.author.name}",
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
                        "Time": current_time,
                    }

                    # Append the new case to the cases list
                    cases["cases"].append(new_case)

                    # Update the case number in the JSON file
                    cases["total_count"] = case_number

                    # Save the JSON file
                    with open("./extras/cases.json", "w") as f:
                        json.dump(cases, f, indent=4)

                    # Deletes x amount of messages and sends a message on the channel
                    try:
                        deletedAmount = await ctx.channel.purge(limit=amount)
                    except discord.errors.RateLimited:
                        errorEmbed = discord.Embed(
                            description="We are being rate limited.", color=0xB50000
                        )
                        await ctx.send(embed=errorEmbed)
                        await asyncio.sleep(5)
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

=======
    async def purge(self, ctx, amount: int, member: discord.Member=None):
        
        if amount > int(self.limit):
            embedError = discord.Embed(description="The amount exceeds the limit. Do not exceed the limit to keep the bot running smoothly.")
            
            await ctx.send(embed=embedError)
        else:
            if member is not None:
                
                # Load the JSON file containing the cases
                with open('./extras/cases.json', 'r') as f:
                    cases = json.load(f)
                
                # Increment the case number
                case_number = cases['total_count'] + 1
                
                # Create a new case object
                new_case = {
                    'ID': case_number,
                    'Responsible Staff': ctx.author.name,
                    'Activity': 'Purge Member Message',
                    'Channel': ctx.channel.name,
                    'Member': member.name,
                    'Time': current_time
                }
                
                # Append the new case to the cases list
                cases['cases'].append(new_case)
                
                # Update the case number in the JSON file
                cases['total_count'] = case_number
                
                # Save the JSON file
                with open('./extras/cases.json', 'w') as f:
                    json.dump(cases, f, indent=4)
                
                # Deletes x amount of messages and sends a message on the channel
                await ctx.channel.purge(limit=amount + 1, check=lambda m: m.author == member)
                embedAction = discord.Embed(description=f"Deleted {amount} messages of {member.display_name} in this channel", color=0xf50000)
                await ctx.send(embed=embedAction, delete_after=5)
                
                # Log the moderation activity
                channel = self.bot.get_channel(modlogsID)
                embedLog = discord.Embed(description=f"Deleted {amount} messages of {member.display_name} in {ctx.channel.mention}", color=0x9acd32, timestamp=datetime.now())
                embedLog.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                embedLog.set_footer(text=f"Case ID: {case_number}")
                await channel.send(embed=embedLog)
            else:
                
                # Load the JSON file containing the cases
                with open('./extras/cases.json', 'r') as f:
                    cases = json.load(f)
                
                # Increment the case number
                case_number = cases['total_count'] + 1
                
                # Create a new case object
                new_case = {
                    'ID': case_number,
                    'Responsible Staff': ctx.author.name,
                    'Activity': 'Purge',
                    'Channel': ctx.channel.name,
                    'Time': current_time
                }
                
                # Append the new case to the cases list
                cases['cases'].append(new_case)
                
                # Update the case number in the JSON file
                cases['total_count'] = case_number
                
                # Save the JSON file
                with open('./extras/cases.json', 'w') as f:
                    json.dump(cases, f, indent=4)
                
                # Deletes x amount of messages and sends a message on the channel
                await ctx.channel.purge(limit=amount + 1)
                embedAction = discord.Embed(description=f"Deleted {amount} messages in this channel", color=0xf50000)
                await ctx.send(embed=embedAction, delete_after=5)
                
                # Log the moderation activity
                modlogs = self.bot.get_channel(int(modlogsID))
                embedLog = discord.Embed(description=f"Deleted {amount} messages in {ctx.channel.mention}", color=0x9acd32, timestamp=datetime.now())
                embedLog.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                embedLog.set_footer(text=f"Case ID: {case_number}")
                await modlogs.send(embed=embedLog)       
        
>>>>>>> e200e1035f2a61a8df79874c40551ca6c26cbd3d
    ### Punishment System ###
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if member == ctx.author:
            embedError = discord.Embed(
                description="Error! You cannot kick yourself!", color=0xFF0000
            )

            await ctx.send(embed=embedError, delete_after=3)
        else:
<<<<<<< HEAD
            await ctx.message.delete()
=======
            
>>>>>>> e200e1035f2a61a8df79874c40551ca6c26cbd3d
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
<<<<<<< HEAD

=======
                
            # Sends a message on the channel and kicks the member
            embedAction = discord.Embed(description=f"{member.name} has been removed from the server for violating our community guidelines.", color=0xf50000)
            await ctx.send(embed=embedAction, delete_after=5)
            await member.kick(reason=reason)
            
            # Send a kick notice to the member
            embedNotice = discord.Embed(description=f"Hey there {member.name}!\n\nThis message is sent to make you aware of the action we've made.\nYou have been removed from the server for violating our community guidelines.\n\nWe take the safety and well-being of our community seriously. Please respect our rules and guidelines to ensure a positive and enjoyable experience for all members.\n\nIf you were removed from the server and believe it was unjust, you can file an appeal ticket on our server for reinstatement. Provide a clear explanation and any supporting evidence. We take moderation actions seriously and will not entertain frivolous appeals. Our team will review and make a decision as soon as possible.", color=0xb50000, timestamp=datetime.now())
            embedNotice.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)
            embedNotice.add_field(name="Reason For The Action:", value=reason)
            embedNotice.set_footer(text=f"Case ID: {case_number} • Responsible Staff : {ctx.author.name}")
            
            await member.send(embed=embedNotice)
            
            # Log the moderation activity
            modlogs = self.bot.get_channel(int(modlogsID))
            embedLog = discord.Embed(color=0xf50000, timestamp=datetime.now())
            embedLog.set_author(name=f"{member.name}#{member.discriminator} has been kicked", icon_url=member.avatar)
            embedLog.add_field(name="Responsible Staff", value=ctx.author, inline=True)
            embedLog.add_field(name="Reason", value=reason, inline=False)
            await modlogs.send(embed=embedLog)
        
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if member == ctx.author:
            embedError = discord.Embed(description="Error! You cannot ban yourself!", color=0xff0000)
            
            await ctx.send(embed=embedError, delete_after=3)
        else:
            
            # Load the JSON file containing the cases
            with open('./extras/cases.json', 'r') as f:
                cases = json.load(f)
            
            # Increment the case number
            case_number = cases['total_count'] + 1
            
            # Create a new case object
            new_case = {
                'ID': case_number,
                'Responsible Staff': ctx.author.name,
                'User': member.name,
                'Activity': 'Banned',
                'Reason': reason,
                'Time': current_time
            }
            
            # Append the new case to the cases list
            cases['cases'].append(new_case)
            
            # Update the case number in the JSON file
            cases['total_count'] = case_number
            
            # Save the JSON file
            with open('./extras/cases.json', 'w') as f:
                json.dump(cases, f, indent=4)
                
            # Sends a message on the channel and bans the member
            embedAction = discord.Embed(description=f"{member.name} has been banned from the server for violating our community guidelines.", color=0xf50000)
            await ctx.send(embed=embedAction)
            await member.ban(reason=reason)
            
            # Send a ban notice to the member
            embedNotice = discord.Embed(description=f"Hey there {member.name}!\n\nThis message is sent to make you aware of the action we've made.\nYou have been banned from the server for violating our community guidelines.\n\nWe take the safety and well-being of our community seriously. Please respect our rules and guidelines to ensure a positive and enjoyable experience for all members.\n\nIf you were removed from the server and believe it was unjust, you can [submit an appeal](https://forms.gle/M6yTr78DkMycVpSY7) for reinstatement. Provide a clear explanation and any supporting evidence. We take moderation actions seriously and will not entertain frivolous appeals. Our team will review and make a decision as soon as possible.", color=0xf50000, timestamp=datetime.now())
            embedNotice.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)
            embedNotice.add_field(name="Reason For The Action:", value=reason)
            embedNotice.set_footer(text=f"Case ID: {case_number} • Responsible Staff : {ctx.author.name}")
            
            await member.send(embed=embedNotice)
            
            # Log the moderation activity
            modlogs = self.bot.get_channel(int(modlogsID))
            embedLog = discord.Embed(color=0xf50000, timestamp=datetime.now())
            embedLog.set_author(name=f"{member.name}#{member.discriminator} has been banned", icon_url=member.avatar)
            embedLog.add_field(name="Responsible Staff", value=ctx.author, inline=True)
            embedLog.add_field(name="Reason", value=reason, inline=False)
            await modlogs.send(embed=embedLog)
        
    ### Warning System ###
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        if member == ctx.author:
            embedError = discord.Embed(description="Error! You cannot warn yourself!", color=0xff0000)
            
            await ctx.send(embed=embedError, delete_after=3)
        else:
            
            # Load the JSON file containing the cases
            with open('./extras/cases.json', 'r') as f:
                cases = json.load(f)
            
            # Increment the case number
            case_number = cases['total_count'] + 1
            
            # Create a new case object
            new_case = {
                'ID': case_number,
                'Responsible Staff': ctx.author.name,
                'User': member.name,
                'Status': 'Warning',
                'Reason': reason,
                'Time': current_time
            }
            
            # Append the new case to the cases list
            cases['cases'].append(new_case)
            
            # Update the case number in the JSON file
            cases['total_count'] = case_number
            
            # Save the JSON file
            with open('./extras/cases.json', 'w') as f:
                json.dump(cases, f, indent=4)
            
>>>>>>> e200e1035f2a61a8df79874c40551ca6c26cbd3d
            # Load the JSON file containing the warnings
            with open("./extras/warnings.json", "r") as f:
                warnings = json.load(f)

<<<<<<< HEAD
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
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if member == ctx.author:
            embedError = discord.Embed(
                description="Error! You cannot ban yourself!", color=0xFF0000
            )

            await ctx.send(embed=embedError, delete_after=3)
        else:
            await ctx.message.delete()

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
            await ctx.send(embed=embedAction)
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

    ### Warning System ###
    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
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

=======
                warnings[str(member.id)]["WarningCount"] = str(int(warnings[str(member.id)]["WarningCount"]) + 1)
                warning_number = warnings[str(member.id)]["WarningCount"]
                warnings[str(member.id)][warning_number] = {
                    "Reason": reason,
                    "Staff Responsible": ctx.author.name,
                    "Time": str(datetime.now())
                    }
            elif warnings[str(member.id)]["WarningCount"] == 3:

                modlogs = self.bot.get_channel(int(modlogsID))
                embedLog = discord.Embed(color=0xf50000, timestamp=datetime.now())
                embedLog.set_author(name=f"{member.name}#{member.discriminator} has been kicked for surpassing the maximum amount of warnings.", icon_url=member.avatar)
                embedLog.add_field(name="Responsible Staff", value=ctx.author, inline=True)
                embedLog.add_field(name="Reason", value=reason, inline=False)
                await modlogs.send(embed=embedLog)

                await member.kick(reason=reason)
        
            
            # Save the JSON file
            with open("./extras/warnings.json", "w") as f:
                json.dump(warnings, f, indent=4)
                
>>>>>>> e200e1035f2a61a8df79874c40551ca6c26cbd3d
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
    @commands.has_permissions(manage_guild=True)
<<<<<<< HEAD
    @commands.cooldown(1, 3, commands.BucketType.user)
=======
>>>>>>> e200e1035f2a61a8df79874c40551ca6c26cbd3d
    async def clearwarnings(self, ctx, member: discord.Member):
        if member == ctx.author:
            embedError = discord.Embed(
                description="Error! You cannot clear your warnings!", color=0xFF0000
            )

            await ctx.send(embed=embedError, delete_after=3)
        else:
<<<<<<< HEAD
            await ctx.message.delete()
=======
            
>>>>>>> e200e1035f2a61a8df79874c40551ca6c26cbd3d
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
<<<<<<< HEAD
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def checkwarnings(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        # Load warnings data
        with open("./extras/warnings.json", "r") as f:
=======
    @commands.has_permissions(kick_members=True)
    async def checkwarnings(self, ctx, member: discord.Member):
        with open('./extras/warnings.json', 'r') as f:
>>>>>>> e200e1035f2a61a8df79874c40551ca6c26cbd3d
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
    @commands.has_permissions(administrator=True)
    async def lockdown(self, ctx):
<<<<<<< HEAD
=======
        
>>>>>>> e200e1035f2a61a8df79874c40551ca6c26cbd3d
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
    @commands.has_permissions(administrator=True)
    async def unlock(self, ctx):
<<<<<<< HEAD
=======
        
>>>>>>> e200e1035f2a61a8df79874c40551ca6c26cbd3d
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
    @commands.has_any_role(
        1134743832345448498,
        1145297118735642715,
        1145283225875390504,
        1145295915159138334,
    )
    async def announce(self, ctx, channel: discord.TextChannel, *, message):
        embed = discord.Embed(description=f"{message}", color=0xB50000)

        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ModerationTools(bot))
