import json
import os
import subprocess
import time
from dotenv import load_dotenv, set_key

# Store the PID of the running bot process


def start_bot():
    try:
        os.system("cls")
        print("Starting the bot this might take a while...")
        subprocess.Popen([
            "start", "cmd", "/k",
            "C:\Life\Programming\ForTheGrindBot\start_bot.bat"
        ],
                         shell=True)
        # Wait for the process to start (you can adjust this delay as needed)
        time.sleep(10)
        load_dotenv(override=True)
        botPID = os.getenv("PID")
        print(f"Successfully started the bot with Process ID: {botPID}")

    except Exception as e:
        print(f"Failed to start the bot. Error: {str(e)}")


def stop_bot():
    load_dotenv(override=True)

    try:
        botPID = os.getenv("PID")
        if botPID != "None":
            os.system("cls")
            print("Shutting the bot down. This may take a while...")
            time.sleep(3)

            # Terminate the process using its PID
            os.system(f"taskkill /F /PID {botPID}")
            try:
                os.system(f"taskkill /F /IM cmd.exe")
            except Exception as e:
                print(e)
            print(f"Bot with PID {botPID} stopped successfully.")
            # Set the PID to None in the .env file
            set_key(".env", "PID", "None")
        else:
            print("Bot is not running on any process.")

    except Exception as e:
        print(f"An error occurred while stopping the bot: {str(e)}")


def restart():
    botPID = os.getenv("PID")
    if botPID != "None":
        stop_bot()
        start_bot()
        with open("./config.json", "r") as f:
            config = json.load(f)

        config["Restarted"] = "True"

        with open("./config.json", "w") as f:
            json.dump(config, f)
    else:
        print("Bot is not running on any process...")


def main_loop():
    while True:
        load_dotenv(override=True)
        botPID = os.getenv("PID")
        try:
            os.system("cls")
            option = None
            art = r"""┏┓┏┳┓┏┓  ┳┓┏┓┳┳┓┏┓┏┳┓┏┓
┣  ┃ ┃┓  ┣┫┣ ┃┃┃┃┃ ┃ ┣ 
┻  ┻ ┗┛  ┛┗┗┛┛ ┗┗┛ ┻ ┗┛
                       """
            print("─" * 50)
            print(art)
            print("─" * 50)
            if botPID != "None":
                print(f"Bot is currently running on PID: {botPID}")
                print("─" * 50)
            print("Remote Access Tool Options")
            print("─" * 50)
            print("[0] Quit the RAT")
            print("[1] Start The Bot")
            print("[2] Restart The Bot")
            print("[3] Stop The Bot")

            option = input("Enter your choice: ")

            try:
                option = int(option)
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if option == 0:
                print("Closing the Remote Access Tool for FTG")
                os.system("cls")
                break

            if option == 1:
                print("Initiating bot startup...")
                if botPID != "None":
                    os.system("cls")
                    print(
                        f"Error while starting bot. The bot is already running on PID: {botPID}"
                    )
                    continue
                elif botPID == "None":
                    start_bot()
                    continue

            if option == 2:
                try:
                    restart()
                    continue
                except Exception as error:
                    os.system("cls")
                    print(f"Error while restarting the bot: {error}")

            if option == 3:
                try:
                    stop_bot()
                    continue
                except Exception as error:
                    os.system("cls")
                    print(f"An error has occurred: {error}")

        except Exception as error:
            os.system("cls")
            print(f"An error has occurred:")
            print(f"\n\n{error}")

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("Server was interrupted by the user.")
