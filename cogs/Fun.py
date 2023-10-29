import discord
import json
import random
import aiohttp
import requests

from discord.ext import commands


def format_time(self, seconds):
    # Extract hours, minutes, and seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Build a readable time format
    if hours:
        return f"{hours} hours, {minutes} minutes, and {seconds} seconds"
    elif minutes:
        return f"{minutes} minutes and {seconds} seconds"
    else:
        return f"{seconds} seconds"


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        try:
            with open("./extras/afks.json", "r") as f:
                self.afk_data = json.load(f)
        except FileNotFoundError:
            self.afk_data = {}

    @commands.command(aliases=["roll"])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def dice(self, ctx):
        dice = random.randint(1, 6)

        embed = discord.Embed(
            description=f"You rolled a dice, and got {dice}.", color=0xB50000
        )

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.member)
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
            color=0xB50000,
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=["8ball", "magicball"])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def eightball(self, ctx, *, question):
        responses = [
            "Yes, definitely.",
            "No, never.",
            "It's possible.",
            "Not in a million years.",
            "Yes, but don't count on it.",
            "I would not bet on it.",
            "Outlook not so good.",
            "Absolutely!",
            "I don't think so.",
            "Ask again later.",
        ]

        # Choose a random response
        response = random.choice(responses)

        embed = discord.Embed(description=f"{response}", color=0xB50000)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def rps(self, ctx, choice):
        choices = ["rock", "paper", "scissors"]

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
        elif (
            (choice == "rock" and bot_choice == "scissors")
            or (choice == "paper" and bot_choice == "rock")
            or (choice == "scissors" and bot_choice == "paper")
        ):
            result = "You win!"
        else:
            result = "You lose!"

        embed = discord.Embed(title="Rock, Paper, Scissors", color=discord.Color.blue())
        embed.add_field(name="Your choice", value=choice, inline=False)
        embed.add_field(name="Bot's choice", value=bot_choice, inline=False)
        embed.add_field(name="Result", value=result, inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dog(self, ctx):
        # Your API URL
        api_url = "https://dog.ceo/api/breeds/image/random"

        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success":
                image_url = data["message"]

                # Send the image in the Discord channel
                await ctx.send(image_url)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cat(self, ctx):
        api_url = "https://api.thecatapi.com/v1/images/search"

        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()

            if data and isinstance(data, list) and "url" in data[0]:
                image_url = data[0]["url"]
                await ctx.send(image_url)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dadjoke(self, ctx):
        # API URL for dad jokes
        api_url = "https://icanhazdadjoke.com/"

        # Set headers to specify we want a plain text response
        headers = {"Accept": "text/plain"}

        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            joke = response.text
            await ctx.send(joke)


async def setup(bot):
    await bot.add_cog(Fun(bot))
