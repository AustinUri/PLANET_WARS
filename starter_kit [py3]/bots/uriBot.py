def do_turn(pw):
    # Check if the bot has fleets currently in transit
    if len(pw.my_fleets()) >= 1:
        return

    # Get a list of planets owned by the bot
    my_planets = pw.my_planets()

    # Initialize variables to find the best source planet
    source = -1
    source_score = -999999.0
    source_num_ships = 0

    for p in my_planets:
        # Score based on the number of ships, growth rate, and threat level
        nearby_enemy_fleets = sum(1 for f in pw.enemy_fleets() if pw.distance(p.planet_id(), f.source_planet()) < 5)
        score = (float(p.num_ships()) + p.growth_rate() * 10 - nearby_enemy_fleets * 50)
        if score > source_score:
            source_score = score
            source = p.planet_id()
            source_num_ships = p.num_ships()

    # Get a list of all planets not owned by the bot
    not_my_planets = pw.not_my_planets()

    # Initialize variables to find the best destination planet
    dest = -1
    dest_score = -999999.0

    for p in not_my_planets:
        # Score based on the number of enemy ships, proximity to source, growth rate, and potential growth
        enemy_fleets_nearby = sum(1 for f in pw.enemy_fleets() if pw.distance(p.planet_id(), f.source_planet()) < 5)
        score = (1.0 / (1 + p.num_ships())) + (100 - pw.distance(p.planet_id(), source)) / 100 - enemy_fleets_nearby * 50
        if p.growth_rate() > 0:
            score += p.growth_rate() * 10
        if score > dest_score:
            dest_score = score
            dest = p.planet_id()

    # Issue orders if valid source and destination are found
    if source >= 0 and dest >= 0:
        # Maximize the number of ships sent to attack
        num_ships = int(source_num_ships * 0.95)  # Send 95% of available ships
        if pw.turn_number() > 900:
            num_ships = min(num_ships, int(source_num_ships))  # In the last 100 turns, send all remaining ships
        
        # Ensure the number of ships sent does not exceed the number of ships available
        num_ships = min(num_ships, source_num_ships)

        # Check if the source planet is under threat
        source_under_threat = any(
            pw.distance(source, p.planet_id()) < 5
            for p in pw.enemy_planets()
        )
        
        if source_under_threat:
            # Aggressively reinforce the source planet if it's under threat
            required_reinforcement = max(0, source_num_ships - num_ships)
            if required_reinforcement > 0:
                # Sort planets by the number of ships available and prioritize those with high growth rates
                reinforcement_sources = sorted(
                    (p for p in my_planets if p.planet_id() != source),
                    key=lambda p: (p.num_ships() + p.growth_rate() * 10),
                    reverse=True
                )
                
                for p in reinforcement_sources:
                    if required_reinforcement <= 0:
                        break
                    
                    available_ships = p.num_ships()
                    transfer_ships = min(available_ships, required_reinforcement)
                    # Send ships from the reinforcement planet to the threatened source planet
                    pw.issue_order(p.planet_id(), source, transfer_ships)
                    required_reinforcement -= transfer_ships

        # Issue the primary attack order
        pw.issue_order(source, dest, num_ships)

        # Additional aggressive actions
        if pw.turn_number() > 900:
            # Identify secondary targets for additional aggression
            secondary_targets = sorted(
                (p for p in not_my_planets if pw.distance(p.planet_id(), source) > 5),
                key=lambda p: (1.0 / (1 + p.num_ships()) + p.growth_rate() * 10),
                reverse=True
            )
            for target in secondary_targets:
                if pw.distance(target.planet_id(), source) > 5:
                    alt_dest = target.planet_id()
                    alt_num_ships = int(source_num_ships * 0.4)  # Use 40% of ships for secondary targets
                    if alt_num_ships > 0:
                        pw.issue_order(source, alt_dest, alt_num_ships)
                        break  # Issue order to only one additional target to avoid overcommitment

        # Aggressive fleet management: Consider sending ships from other planets
        if pw.turn_number() > 900:
            for p in my_planets:
                if p.planet_id() != source and p.num_ships() > 10:
                    alt_targets = sorted(
                        (p for p in not_my_planets if pw.distance(p.planet_id(), source) > 5),
                        key=lambda p: (1.0 / (1 + p.num_ships()) + p.growth_rate() * 10),
                        reverse=True
                    )
                    if alt_targets:
                        alt_target = alt_targets[0].planet_id()
                        num_ships = int(p.num_ships() * 0.6)  # Send 60% of ships from other planets
                        if num_ships > 0:
                            pw.issue_order(p.planet_id(), alt_target, num_ships)
                            break
