import sys
import os
import importlib

from PlanetWars import PlanetWars

def main():
    pw = PlanetWars('')
    do_turn(pw)

if __name__ == '__main__':
	assert len(sys.argv) == 2

	bot_path = sys.argv[1]
	bot_dir = os.path.dirname(bot_path)
	bot_filename = os.path.basename(bot_path)
	bot_modulename = os.path.splitext(bot_filename)[0]
	
	sys.path.append(bot_dir)
	
	bot_module = importlib.import_module(bot_modulename)
		
	do_turn = bot_module.do_turn

	main()
