import discord
from discord.ext import commands


class ScrimScheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def schedule(self, ctx, game, *, text):
        communityChannel = ctx.guild.get_channel(1134737529443196988)
        description = f"Game: {game}\n{text}"

        scheduleEmbed = discord.Embed(description=description, color=0xB50000)
        scheduleEmbed.set_author(name="Community Scrim Manager")
        scheduleEmbed.add_field(name="Joined",  value="No players", inline=True)
        scheduleEmbed.add_field(name="Tentative", value="No players", inline=True)
        # Create the message with the view and send it
        message = await communityChannel.send(embed=scheduleEmbed, view=ParticipantsControl(ctx=ctx, game=game, text=description))

class ParticipantsControl(discord.ui.View):
    joinedPlayers = []
    tentativePlayers = []

    def __init__(self, game, ctx, text):
        super().__init__(timeout=None)
        self.game = game
        self.ctx = ctx
        self.text = text

    @discord.ui.button(
        label="Join Party", style=discord.ButtonStyle.grey, custom_id="pc:JP:gray"
    )
    async def join(self, interaction: discord.Interaction, button: discord.Button):
        user_id = interaction.user.id  # Get the user's ID
        if len(self.joinedPlayers) < 5:
            if user_id in self.tentativePlayers:
                self.tentativePlayers.remove(user_id)
            if user_id not in self.joinedPlayers:  # Check if the user is not already in the list
                self.joinedPlayers.append(user_id)
                print(f"A participant has joined. Total Players Joined: {len(self.joinedPlayers)}/5")
                if self.game == "Valorant":
                    ScrimChannel = self.ctx.guild.get_channel(1160519497711628370)
                    role = discord.utils.get(interaction.user.guild.roles, id=1160522888554741772)
                    await interaction.user.add_roles(role)

                joinedEmbed = discord.Embed(description=f"You have successfully joined the scrim!\nYou can now access {ScrimChannel.mention}.")
                scheduleEmbed = discord.Embed(description=self.text, color=0xb50000)
                scheduleEmbed.set_author(name="Community Scrim Manager")
                scheduleEmbed.add_field(name="Joined", value="\n".join([f"<:B1:1134737275318706278><@{player}>" for player in self.joinedPlayers]))
                if self.tentativePlayers:
                    scheduleEmbed.add_field(name="Tentative", value="\n".join([f"<:B1:1134737275318706278><@{player}>" for player in self.tentativePlayers]))
                else:
                    scheduleEmbed.add_field(name="Tentative", value="No players yet")
                
                await interaction.message.edit(embed=scheduleEmbed)
                await interaction.response.send_message(embed=joinedEmbed, ephemeral=True)
            else:
                already = discord.Embed(
                    description="You are already joined the party!",
                    color=0xb50000
                )

                await interaction.response.send_message(embed=already, ephemeral=True)

    @discord.ui.button(
        label="Join Tentative", style=discord.ButtonStyle.grey, custom_id="pc:JT:gray"
    )
    async def tentative(self, interaction: discord.Interaction, button: discord.Button):
        user_id = interaction.user.id  # Get the user's ID
        if len(self.tentativePlayers) < 5:
            if user_id in self.joinedPlayers:
                joinedRole = discord.utils.get(interaction.guild.roles, id=1160522888554741772)
                if joinedRole is not None:
                    await interaction.user.remove_roles(joinedRole)  # Remove the role
                    print(f"Role {joinedRole.name} removed from {interaction.user.display_name}")
                else:
                    print("Role not found.")
                self.joinedPlayers.remove(user_id)
                    
            if user_id not in self.tentativePlayers:  # Check if the user is not already in the list
                self.tentativePlayers.append(user_id)
                print(f"A participant has joined tentatively. Total Players Joined: {len(self.tentativePlayers)}/5")

                tentativeEmbed = discord.Embed(description=f"You are now listed as a tentative player.")
                scheduleEmbed = discord.Embed(description=self.text, color=0xb50000)
                scheduleEmbed.set_author(name="Community Scrim Manager")
                if self.joinedPlayers:
                    scheduleEmbed.add_field(name="Joined", value="\n".join([f"<:B1:1134737275318706278><@{player}>" for player in self.joinedPlayers]))
                else: 
                    scheduleEmbed.add_field(name="Joined", value="No players yet")
                scheduleEmbed.add_field(name="Tentative", value="\n".join([f"<:B1:1134737275318706278><@{player}>" for player in self.tentativePlayers]))
                
                await interaction.message.edit(embed=scheduleEmbed)
                await interaction.response.send_message(embed=tentativeEmbed, ephemeral=True)
            else:
                already = discord.Embed(
                    description="You are already listed as a tentative player!",
                    color=0xb50000
                )

                await interaction.response.send_message(embed=already, ephemeral=True)


async def setup(bot):
    await bot.add_cog(ScrimScheduler(bot))
