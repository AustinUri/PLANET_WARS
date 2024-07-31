def do_turn(pw):
    if len(pw.my_fleets()) >= 1:
        return
    source = -1
    source_score = -999999.0
    source_num_ships = 0
    my_planets = pw.my_planets()
    for p in my_planets:
        score = float(p.num_ships())
        if score > source_score:
            source_score = score
            source = p.planet_id()
            source_num_ships = p.num_ships()

    dest = -1
    dest_score = -999999.0
    not_my_planets = pw.not_my_planets()
    for p in not_my_planets:
        score = 1.0 / (1 + p.num_ships())
        if score > dest_score:
            dest_score = score
            dest = p.planet_id()

    if source >= 0 and dest >= 0:
        num_ships = source_num_ships / 2
        pw.issue_order(source, dest, num_ships)
