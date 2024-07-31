#! /bin/bash

if [ -z $1 ] || [ -z $2 ]; then
    echo "Usage $0 <Player One Bot> <Player Two Bot> [Map]"
    exit 1
fi

map=$3

if [ -z $map ]; then
    map="maps/default_map.txt"
fi

java -jar tools/PlayGame.jar $map 1000 1000 log.txt "python tools/run_bot.py $1" "python tools/run_bot.py $2" | java -jar tools/ShowGame.jar 10

