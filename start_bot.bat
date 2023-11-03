@echo off
chcp 65001
call c:/Life/Programming/ForTheGrindBot/.venv/Scripts/activate

REM Create a timestamp for the log file name (format: YYYYMMDD_HHMMSS)
for /f "tokens=2 delims==." %%I in ('wmic os get LocalDateTime /value') do set "timestamp=%%I"

REM Set the log folder and the number of log files to keep
set "logFolder=C:\Life\Programming\ForTheGrindBot\logs"
set "logsToKeep=5"

REM Delete old log files, keeping the newest 'logsToKeep' logs
for /f "tokens=1,* delims=_" %%F in ('dir /b /o-n "%logFolder%\output_*.log"') do (
    set /a "count+=1"
    if !count! gtr %logsToKeep% (
        del "%logFolder%\%%F_%%G"
    )
)

python "C:/Life/Programming/ForTheGrindBot/bot.py" > "%logFolder%\output_%timestamp%.log" 2>&1
