import json
import discord
from discord.ext import commands
import random

class Economy(commands.Cog):
    def __init__(self, bot):
        self.client = bot
        self.level_experience_requirements = {
            1: 100,
            5: 500,
            10: 1000,
            25: 25000,
            50: 50000,
            75: 75000,
            100: 100000
        }
        self.level_up_channel_id = 1134737529443196988  # Replace with your actual channel ID

    # Event listener for when a message is sent
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  # Ignore messages from bots

        await self.add_experience(message)  # Call add_experience using self

        # ... rest of your message handling code
        # Example: You can check message content, apply rewards, etc.

        # Save the data after every message
        data = self.load_data()
        self.save_data(data)

    # Create a new user entry for when a user joins
    async def create_new_user_entry(self, member):
        user_id = str(member.id)
        data = self.load_data()

        # Check if the user already exists in the data
        if user_id not in data["users"]:
            data["users"][user_id] = {"Level": 1, "Experience": 0, "Experience_Gained": 0}

        self.save_data(data)

    # Function to add experience points to a user
    async def add_experience(self, message):
        user_id = str(message.author.id)
        data = self.load_data()
        user = data["users"].get(user_id, {"Level": 1, "Experience": 0, "Experience_Gained": 0})

        if user["Level"] >= 100:
            return  # Do not gain experience beyond level 100
        
        # Check if the message is a command
        if message.content.startswith('ftg.'):  # Adjust this condition based on your command prefix
            return  # Do not gain experience for commands
        
        # Generate a random number between 0 and 1
        random_chance = random.random()

        # Define a lower chance of gaining experience (e.g., 50%)
        chance_of_experience = 0.5

        if random_chance < chance_of_experience:
            # Generate a random amount of experience points between 1 and 5
            experience_points = random.randint(1, 5)

            user["Experience"] += experience_points
            user["Experience_Gained"] += experience_points

            while user["Experience"] >= self.calculate_experience_required(user["Level"] + 1):
                user["Level"] += 1
                user["Experience"] -= self.calculate_experience_required(user["Level"])

                if user["Level"] >= 100:
                    user["Level"] = 100
                    user["Experience"] = 0
                    break

                # Send a level-up message to the designated channel
                level_up_channel = self.client.get_channel(self.level_up_channel_id)
                if level_up_channel:
                    await level_up_channel.send(f"🎉 {user_id} has reached Level {user['Level']}!")

            data["users"][user_id] = user
            self.save_data(data)  # Save the data after updating
    
    def calculate_experience_required(self, level):
        # Calculate experience required based on provided requirements
        for req_level, req_experience in self.level_experience_requirements.items():
            if level <= req_level:
                return req_experience
        return self.level_experience_requirements[100]  # Default to level 100 experience

    # Function to load data
    def load_data(self):
        # Implement your data loading logic here
        # Example: Load data from a JSON file
        with open('./extras/bank.json', 'r') as f:
            return json.load(f)

    # Function to save data
    def save_data(self, data):
        # Implement your data saving logic here
        # Example: Save data to a JSON file
        with open('./extras/bank.json', 'w') as f:
            json.dump(data, f, indent=4)

# Function to set up the cog
async def setup(bot):
    await bot.add_cog(Economy(bot))