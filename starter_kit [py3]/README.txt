Welcome to the README file of the starter kit of PlanetWars.

Read this manual to understand how to use the simulator.

---- The files ----
Here is the list of files in the starter kit and an explanation on how to use them:
1. README.txt - This readme file
2. Readme.url - A link to an explaination about the game and the api
3. run.bat - The exectuable to run the simulator on Microsoft Windows
4. run.sh - The executable to run the simulator on OSX or Linux based systems
5. tools/ - A directory with all sorts of tools used to run the simulator
6. tools/PlanetWars.py - The api used to run the planet wars game
7. tools/run_bot.py - The python file used to by the simulator to run the bot
8. PlayGame.jar - The java archive used by the simulator to simulate the game
9. ShowGame.jar - The java acrhive used to show game results in a pretty ui
10. maps/ - A directory of maps to run the simulator on
11. maps/default_map.txt - The default map to start with
12. bots/ - A directory with the bot files
13 bots/DemoBot.pyc - An example bot to start running the simulator with

---- How to run ----

-- Windows --

1. Make sure you have java installed.
2. Open cmd (command line for windows)
3. Go to the starter kit directory (the directory of this file)
4. Run: run.bat <bot1 filename> <bot2 filename> [optional map file]

-- OSX/Linux --

1. Make sure you have java installed
2. Open terminal
3. Go to the starter kit directory (the directory of this file)
4. Run: ./run.sh <bot1 filename> <bot2 filename> [optional map file]

---- First Run ----

For the first run, please use the Demo bot. So in order to run the bot for the first time use:
Windows:   run.bat bots/DemoBot.pyc bots/DemoBot.pyc
OSX/Linux: ./run.sh bots/DemoBot.pyc bots/DemoBot.pyc

---- Using a different map ----

In order to use a different map, you first need to download a new map to the maps directory.
Then you need to provide a third argument to the run command which is the name of the new map file
Windows:   run.bar bots/bot1.py bots/bot2.py maps/new_map.txt
OXS/Linux: ./run.sh bots/bot1.py bots/bot2.py maps/new_map.txt

---- Summary ----

That's it! You're good to go.
Write the best bot player you can and may the force be with you!


