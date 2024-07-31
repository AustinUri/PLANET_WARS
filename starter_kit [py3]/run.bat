@echo off

where python > nul 2> nul
if ERRORLEVEL 1 goto nopython

where java > nul 2> nul
if ERRORLEVEL 1 goto nojava

if [%1]==[] goto usage
if [%2]==[] goto usage

if not exist %1 goto notexist1
if not exist %2 goto notexist2

python tools/test_bot.py %1
if ERRORLEVEL 1 goto crashed1
python tools/test_bot.py %2
if ERRORLEVEL 1 goto crashed2

set map=%3
if [%3]==[]  set map=maps/default_map.txt

java -jar tools/PlayGame.jar %map% 1000 1000 log.txt "python tools/run_bot.py %1" "python tools/run_bot.py %2" | java -jar tools/ShowGame.jar 10
goto :eof

:usage
@echo Usage: %0 ^<Player One Bot^> ^<Player Two Bot^> [Map]
exit /B 1

:nopython
@echo ERROR: Python is not installed OR Python not in PATH
exit /B 1

:nojava
@echo ERROR: Java is not installed OR Java not in PATH
exit /B 1

:notexist1
@echo ERROR: Bot #1 ^"%1^" is not exist!
exit /B 1

:notexist2
@echo ERROR: Bot #2 ^"%2^" is not exist!
exit /B 1

:crashed1
@echo ERROR: ERROR: Bot #1 ^"%1^" crashed!
exit /B 1


:crashed2
@echo ERROR: ERROR: Bot #2 ^"%2^" crashed!
exit /B 1