def do_turn(pw):
    if len(pw.my_fleets()) >= 1:
        return

    current_turn = pw.turn_number()
    num_planets = pw.num_planets()
    
    # Prioritize targets: closest with higher growth rate
    best_target = None
    min_distance = float('inf')
    max_growth_rate = float('-inf')
    for p in pw.not_my_planets():
        for mp in pw.my_planets():
            dist = pw.distance(mp.planet_id(), p.planet_id())
            growth_rate = p.growth_rate()
            if dist < min_distance or (dist == min_distance and growth_rate > max_growth_rate):
                min_distance = dist
                max_growth_rate = growth_rate
                best_target = p

    if best_target is None:
        return

    target_id = best_target.planet_id()
    target_ships = best_target.num_ships()
    buffer = min_distance // 2
    required_ships = target_ships + buffer + 1

    ships_to_send = 0
    sources = []
    for p in pw.my_planets():
        if p.num_ships() > 10:
            available_ships = p.num_ships()
            to_send = min(available_ships // 2, required_ships - ships_to_send)
            if to_send > 0:
                ships_to_send += to_send
                sources.append((p.planet_id(), to_send))
            if ships_to_send >= required_ships:
                break

    if ships_to_send >= required_ships:
        for source_id, num_ships in sources:
            source_planet = pw.get_planet(source_id)
            if source_planet.num_ships() >= num_ships and source_planet.num_ships() >= 10:
                # Check if the source planet has enough ships
                if source_id != target_id:
                    pw.issue_order(source_id, target_id, num_ships)
                else:
                    print(f"Skipping order: Source and target are the same ({source_id})")

    weak_planets = [p for p in pw.my_planets() if p.num_ships() < 10]
    for weak in weak_planets:
        if weak.growth_rate() > 0:
            for p in pw.my_planets():
                if weak.planet_id() != p.planet_id() and p.num_ships() > 10:
                    reinforce_ships = min(p.num_ships() // 2, 10)
                    if reinforce_ships > 0:
                        pw.issue_order(p.planet_id(), weak.planet_id(), reinforce_ships)

    if ships_to_send > required_ships * 2:
        secondary_targets = sorted(pw.not_my_planets(), key=lambda p: (pw.distance(sources[0][0], p.planet_id()), -p.growth_rate()))
        for secondary_target in secondary_targets[:2]:
            target_id = secondary_target.planet_id()
            target_ships = secondary_target.num_ships()
            required_ships = target_ships + min_distance // 2 + 1
            for source_id, num_ships in sources:
                if num_ships >= required_ships:
                    source_planet = pw.get_planet(source_id)
                    if source_planet.num_ships() >= required_ships:
                        if source_id != target_id:
                            pw.issue_order(source_id, target_id, required_ships)
                        else:
                            print(f"Skipping order: Source and target are the same ({source_id})")

    for fleet in pw.my_fleets():
        target_planet_id = fleet.target_planet_id()
        turns_remaining = fleet.turns_remaining()

        if pw.get_planet(target_planet_id).owner() == pw.MY_ID:
            if turns_remaining <= 2:
                source_planets = sorted(pw.my_planets(), key=lambda p: pw.distance(p.planet_id(), target_planet_id))
                for source in source_planets:
                    if source.num_ships() > 10:
                        ships_needed = max(0, pw.get_planet(target_planet_id).num_ships() + 1 - source.num_ships())
                        if ships_needed > 0:
                            if source.num_ships() >= ships_needed:
                                pw.issue_order(source.planet_id(), target_planet_id, ships_needed)
                            else:
                                print(f"Skipping reinforcement: Insufficient ships or not owned planet ({source.planet_id()})")
                            break