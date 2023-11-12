@echo off
chcp 65001
title ForTheGrind - Discord Server Bot
call c:/Life/Programming/ForTheGrindBot/.venv/Scripts/activate

REM Set the log folder and the number of log files to keep
set "logFolder=C:\Life\Programming\ForTheGrindBot\logs"

REM Run your Python script and redirect the output to a log file
python "C:/Life/Programming/ForTheGrindBot/bot.py"