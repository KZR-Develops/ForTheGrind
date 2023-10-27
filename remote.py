import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
import socket
import subprocess
import os
import sys
import time
from cogs.DeveloperTools import DeveloperTools
from bot import Main

from dotenv import load_dotenv

# Store the PID of the running bot process

def start_bot():
    try:
        process = subprocess.Popen(['start', 'cmd', '/c', 'start_bot.bat'], shell=True)
        # Wait for the process to start
        time.sleep(10)  # Adjust this delay as needed')
        load_dotenv(override=True)
        botPID = os.getenv('PID')
        print(f"Successfuly started the bot with Process ID: {botPID}")

    except Exception as e:
        print(f'Failed to start the bot. Error: {str(e)}')


def stop_bot():
    load_dotenv(override=True)

    try:
        botPID = os.getenv('PID')
        # Terminate the process using its PID
        os.system(f"taskkill /F /PID {botPID}")
        print(f'Bot with PID {botPID} stopped successfully.')
        

    except Exception as e:
        print(f'An error occurred while stopping the bot: {str(e)}')

def restart():
    stop_bot()

    with open('./config.json', 'r') as f:
        config = json.load(f)

    config['Restarted'] = "True"

    with open('./config.json', 'w') as f:
        json.dump(config, f)

    start_bot()

def main_loop():
    while True:
        load_dotenv(override=True)
        botPID = os.getenv('PID') 
        try:
            option = None 
            print("FTG BOT RAT MENU")
            print("[1] Start The Bot")
            print("[2] Restart The Bot")
            print("[3] Stop The Bot")

            option = input("Enter your choice: ")  

            try:
                option = int(option)
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if option == 1:
                print("Initiating bot startup...")
                if botPID is not None:
                    os.system('cls')
                    print(f"Error while starting bot. The bot is already running on PID: {botPID}")
                else:
                    start_bot()
                    continue

            if option == 2:
                try:
                    print("Initiating bot restart...")
                    restart()
                    continue
                except Exception as error:
                    os.system('cls')
                    print(f"Error while restarting the bot: {error}")

            if option == 3:
                try:
                    print("Shutting the bot down. This may take a while...")
                    stop_bot()
                    continue
                except Exception as error:
                    os.system('cls')
                    print(f"An error has occured: {error}")


        except Exception as error:
            os.system('cls')
            print(f"An error has occured: {error}")
            

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("Server was interrupted by the user.")