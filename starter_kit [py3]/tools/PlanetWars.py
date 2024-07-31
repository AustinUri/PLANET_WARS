#!/usr/bin/env python

from math import ceil, sqrt
from sys import stdout, stderr

turn_num = 0

class Fleet:
    def __init__(self, owner, num_ships, source_planet, destination_planet, \
     total_trip_length, turns_remaining):
        self._owner = owner
        self._num_ships = num_ships
        self._source_planet = source_planet
        self._destination_planet = destination_planet
        self._total_trip_length = total_trip_length
        self._turns_remaining = turns_remaining

    def owner(self):
        return self._owner

    def num_ships(self):
        return self._num_ships

    def source_planet(self):
        return self._source_planet

    def destination_planet(self):
        return self._destination_planet

    def total_trip_length(self):
        return self._total_trip_length

    def turns_remaining(self):
        return self._turns_remaining


class Planet:
    def __init__(self, planet_id, owner, num_ships, growth_rate, x, y):
        self._planet_id = planet_id
        self._owner = owner
        self._num_ships = num_ships
        self._growth_rate = growth_rate
        self._x = x
        self._y = y

    def planet_id(self):
        return self._planet_id

    def owner(self, new_owner=None):
        if new_owner == None:
            return self._owner
        self._owner = new_owner

    def num_ships(self, new_num_ships=None):
        if new_num_ships == None:
            return self._num_ships
        self._num_ships = new_num_ships

    def growth_rate(self):
        return self._growth_rate

    def x(self):
        return self._x

    def y(self):
        return self._y

    def add_ships(self, amount):
        self._num_ships += amount

    def remove_ships(self, amount):
        self._num_ships -= amount


class PlanetWars:
    def __init__(self, gameState):
        self._planets = []
        self._fleets = []
        self.parse_game_state(gameState)
        global turn_num
        turn_num += 1

    def num_planets(self):
        return len(self._planets)

    def get_planet(self, planet_id):
        return self._planets[planet_id]

    def num_fleets(self):
        return len(self._fleets)

    def get_fleet(self, fleet_id):
        return self._fleets[fleet_id]

    def planets(self):
        return self._planets

    def turn_number(self):
        return turn_num

    def my_planets(self):
        r = []
        for p in self._planets:
            if p.owner() != 1:
                continue
            r.append(p)
        return r

    def neutral_planets(self):
        r = []
        for p in self._planets:
            if p.owner() != 0:
                continue
            r.append(p)
        return r

    def enemy_planets(self):
        r = []
        for p in self._planets:
            if p.owner() <= 1:
                continue
            r.append(p)
        return r

    def not_my_planets(self):
        r = []
        for p in self._planets:
            if p.owner() == 1:
                continue
            r.append(p)
        return r

    def fleets(self):
        return self._fleets

    def my_fleets(self):
        r = []
        for f in self._fleets:
            if f.owner() != 1:
                continue
            r.append(f)
        return r

    def enemy_fleets(self):
        r = []
        for f in self._fleets:
            if f.owner() <= 1:
                continue
            r.append(f)
        return r

    def to_string(self):
        s = ''
        for p in self._planets:
            s += "P %f %f %d %d %d\n" % \
             (p.x(), p.y(), p.owner(), p.num_ships(), p.growth_rate())
        for f in self._fleets:
            s += "F %d %d %d %d %d %d\n" % \
             (f.owner(), f.num_ships(), f.source_planet(), f.destination_planet(), \
                f.total_trip_length(), f.turns_remaining())
        return s

    def distance(self, source_planet, destination_planet):
        if type(source_planet) != int:
            source_planet = source_planet.planet_id()
        if type(destination_planet) != int:
            destination_planet = destination_planet.planet_id()
        source = self._planets[source_planet]
        destination = self._planets[destination_planet]
        dx = source.x() - destination.x()
        dy = source.y() - destination.y()
        return int(ceil(sqrt(dx * dx + dy * dy)))

    def issue_order(self, source_planet, destination_planet, num_ships):
        if type(source_planet) != int:
            source_planet = source_planet.planet_id()
        if type(destination_planet) != int:
            destination_planet = destination_planet.planet_id()
        stdout.write("%d %d %d\n" % \
         (source_planet, destination_planet, num_ships))
        stdout.flush()

    def is_alive(self, player_id):
        for p in self._planets:
            if p.owner() == player_id:
                return True
        for f in self._fleets:
            if f.owner() == player_id:
                return True
        return False

    def parse_game_state(self, s):
        self._planets = []
        self._fleets = []
        lines = s.split("\n")
        planet_id = 0

        for line in lines:
            line = line.split("#")[0] # remove comments
            tokens = line.split(" ")
            if len(tokens) == 1:
                continue
            if tokens[0] == "P":
                if len(tokens) != 6:
                    return 0
                p = Planet(planet_id, # The ID of this planet
                                     int(tokens[3]), # Owner
                                     int(tokens[4]), # Num ships
                                     int(tokens[5]), # Growth rate
                                     float(tokens[1]), # X
                                     float(tokens[2])) # Y
                planet_id += 1
                self._planets.append(p)
            elif tokens[0] == "F":
                if len(tokens) != 7:
                    return 0
                f = Fleet(int(tokens[1]), # Owner
                                    int(tokens[2]), # Num ships
                                    int(tokens[3]), # Source
                                    int(tokens[4]), # Destination
                                    int(tokens[5]), # Total trip length
                                    int(tokens[6])) # Turns remaining
                self._fleets.append(f)
            else:
                return 0
        return 1

    def finish_turn(self):
        stdout.write("go\n")
        stdout.flush()

    def debug(self, message):
        print(message, file=stderr)
        stderr.flush()

