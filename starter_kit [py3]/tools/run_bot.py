import sys
import os
import importlib

from PlanetWars import PlanetWars

def main():
    map_data = ''
    while(True):
        current_line = input()
        if len(current_line) >= 2 and current_line.startswith("go"):
            pw = PlanetWars(map_data)
            do_turn(pw)
            pw.finish_turn()
            map_data = ''
        else:
            map_data += current_line + '\n'

if __name__ == '__main__':

    assert len(sys.argv) == 2

    bot_path = sys.argv[1]
    bot_dir = os.path.dirname(bot_path)
    bot_filename = os.path.basename(bot_path)
    bot_modulename = os.path.splitext(bot_filename)[0]

    sys.path.append(bot_dir)

    bot_module = importlib.import_module(bot_modulename)

    do_turn = bot_module.do_turn

    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    try:
        main()
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
