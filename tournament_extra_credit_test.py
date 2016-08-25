#!/usr/bin/env python
#
# Test cases for tournament.py
# These tests are not exhaustive, but they should cover the majority of cases.
#
# If you do add any of the extra credit options, be sure to add/modify these test cases
# as appropriate to account for your module's added functionality.

from tournament import *
import math

def test_rematch_is_prevented():
    """
    Test for rematch between player is prevented
    """

    t_id = create_tournament('test')
    registerPlayer(t_id, 'Cheryl Shakin')
    registerPlayer(t_id, 'Tena Stone')
    registerPlayer(t_id, 'Norma Chapa')
    registerPlayer(t_id, 'Theresa Fisher')
    registerPlayer(t_id, 'Julio Thompson')
    registerPlayer(t_id, 'Frank Pabon')
    registerPlayer(t_id, 'Diana Twiford')
    registerPlayer(t_id, 'Chad Mason')
    swissPairings(t_id)
    rematch = False
    for i in range(3):
        matches = get_matches(t_id)[-4:]
        for match in matches:
            reportMatch(match[3],match[0],match[1],match[2])
        swissPairings(t_id)
        matches = get_matches(t_id)
        if not len(matches) == len(set(matches)):
            rematch = True
    if rematch:
        raise ValueError(
            "Rematch between players should be prevented, and total rematch occurred is %d" % (len(matches)- len(set(matches))))
    print "1. Rematch between players is prevented. Good Job!"

def test_assign_bye_for_odd_number_of_players():
    t_id = create_tournament('test')
    registerPlayer(t_id, 'Cheryl Shakin')
    registerPlayer(t_id, 'Tena Stone')
    registerPlayer(t_id, 'Norma Chapa')
    registerPlayer(t_id, 'Theresa Fisher')
    registerPlayer(t_id, 'Julio Thompson')
    swissPairings(t_id)
    player_byes = player_with_byes(t_id)
    if not len(player_byes) == 1:
        raise ValueError(
            "A player should be assigned a bye when odd number of players registered, total bye assigned is 0")
    print "2. A player is assigned a bye when odd number of players are registered"
    standings = playerStandings(t_id)
    for item in standings:
        if item[1] == player_byes[0][0]:
            if not item[5] == 3 and item[4] == 1:
                raise ValueError(
                    "A bye should be counted as free win and 3 points should be assigned to the user, total points %d" % item[5])
    print "3. A bye is counted as free win and player is assigned 3 points"



if __name__ == '__main__':
    test_rematch_is_prevented()
    test_assign_bye_for_odd_number_of_players()
    print "Success!  All tests pass!"
