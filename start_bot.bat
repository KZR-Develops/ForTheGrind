@echo off
chcp 65001
call c:/Life/Programming/ForTheGrindBot/.venv/Scripts/activate
python "C:/Life/Programming/ForTheGrindBot/bot.py" > "C:\Life\Programming\ForTheGrindBot\logs\output.log" 2>&1
