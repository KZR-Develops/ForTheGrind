import json
import random
import discord
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        try:
            with open('./extras/afks.json', 'r') as f:
                self.afk_data = json.load(f)
        except FileNotFoundError:
            self.afk_data = {}

    @commands.command(aliases=["roll"])
    async def dice(self, ctx):
        dice = random.randint(1, 6)

        embed = discord.Embed(
            description=f"You rolled a dice, and got {dice}.",
            color=0xb50000
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def coinflip(self, ctx):
        coin = random.randint(1, 2)

        def flip(coin):
            if coin == 1:
                face = "Heads"
                return face
            elif coin == 2:
                face = "Tails"
                return face
        
        embed = discord.Embed(
            description=f"You flipped a coin, and got {flip(coin=coin)}.",
            color=0xb50000
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=['8ball', 'magicball'])
    async def eightball(self, ctx, *, question):
        responses = ["Yes, definitely.",
                     "No, never.",
                     "It's possible.",
                     "Not in a million years.",
                     "Yes, but don't count on it.",
                     "I would not bet on it.",
                     "Outlook not so good.",
                     "Absolutely!",
                     "I don't think so.",
                     "Ask again later."]

        # Choose a random response
        response = random.choice(responses)

        embed = discord.Embed(
            description=f"{response}",
            color=0xb50000
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def rps(self, ctx, choice):
        choices = ['rock', 'paper', 'scissors']
        
        # Check if the user's choice is valid
        choice = choice.lower()
        if choice not in choices:
            await ctx.send("Invalid choice! Choose either rock, paper, or scissors.")
            return
        
        # Bot's choice
        bot_choice = random.choice(choices)
        
        # Determine the winner
        if choice == bot_choice:
            result = "It's a tie!"
        elif (choice == 'rock' and bot_choice == 'scissors') or \
             (choice == 'paper' and bot_choice == 'rock') or \
             (choice == 'scissors' and bot_choice == 'paper'):
            result = "You win!"
        else:
            result = "You lose!"
        
        embed = discord.Embed(title="Rock, Paper, Scissors", color=discord.Color.blue())
        embed.add_field(name="Your choice", value=choice, inline=False)
        embed.add_field(name="Bot's choice", value=bot_choice, inline=False)
        embed.add_field(name="Result", value=result, inline=False)

        await ctx.send(embed=embed)

    def save_afk_data(self):
        # Save AFK data to a JSON file
        with open('./extras/afks.json', 'w') as f:
            json.dump(self.afk_data, f)

    @commands.command()
    async def afk(self, ctx, *, reason="No reason provided."):
        """Set yourself as AFK"""
        self.afk_data[str(ctx.author.id)] = reason
        self.save_afk_data()
        await ctx.send(f"{ctx.author.mention} is now AFK. Reason: {reason}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.author.id) in self.afk_data:
            # Remove user from AFK if they send a message
            del self.afk_data[str(message.author.id)]
            self.save_afk_data()
            await message.channel.send(f"{message.author.mention} is no longer AFK.")
    

async def setup(bot):
    await bot.add_cog(Fun(bot))