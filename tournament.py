#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import math
import random

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteTable(table_name):
    """Remove all the records from the given table."""
    conn = connect()
    cursor = conn.cursor()
    query = "delete from " + table_name
    cursor.execute(query);
    conn.commit()
    cursor.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("select count(*) from players")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("insert into players (name) values (%s)", (name,))
    conn.commit()
    cursor.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    cursor = connect().cursor()
    cursor.execute("select * from standings")
    standings = cursor.fetchall()
    cursor.close()
    return standings

def reportMatch(match_id, winner, loser, draw = False):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("insert into match_results(match_id, winner, loser, draw) \
                        values(%d, %d, %d, %s)" % (match_id, winner, loser, draw))

    if draw == True:
        winner_points = 1
        loser_points = 1
    else:
        winner_points = 3
        loser_points = 0

    cursor.execute("insert into player_match_points (match_id, player_id, points) \
                        values (%d,%d,%d)" % (match_id, winner, winner_points))
    cursor.execute("insert into player_match_points (match_id, player_id, points) \
                        values (%d,%d,%d)" % (match_id, loser, loser_points))
    conn.commit()
    conn.close()

def player_with_no_bye():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("select players.id from players, player_byes where player_byes.player_id <> players.id;")
    player = cursor.fetchone()[0]
    conn.close()
    return player

def report_bye(player_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("insert into matches (player_one) values(%d)" % player_id)
    conn.commit()
    cursor.execute("select max(id) from matches")
    match_id = cursor.fetchone()[0]
    points = 3
    bye = 1
    cursor.execute("insert into player_match_points (match_id, player_id, points) \
                        values(%d, %d, %d)" % (match_id, player_id, points))
    cursor.execute("insert into player_byes (player_id, bye) \
                        values(%d, %d)" % (player_id, bye))
    conn.commit()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    total_players = len(standings)
    game_pairs = []
    if standings[0][3] == 0:
        order = get_random_pairs(0, total_players - 1)
        # check if even numbers of players are there
        if not total_players % 2 == 0:
            report_bye(standings[order[-1]][0])
            del order[-1]
    else:
        order = [i for i in range(total_players)]
        matches = get_matches()
        i = 0
        matches = get_sorted_matches(matches)

        for i in range(0,total_players - 1,2):
            pair = (standings[i][0],standings[i+1][0])
            if sorted(pair) in matches:
                temp = order[i+1]
                order[i+1] = order[i+2]
                order[i+2] = temp
        if not total_players % 2 == 0:
            player = player_with_no_bye()
            for i in range(total_players-1,0,-1):
                if player == standings[i][0]:
                    report_bye(player)
                    del order[i]
                    break
    game_pairs = get_game_pairs(order, standings)
    create_matches(game_pairs)
    return game_pairs

def create_matches(game_pairs):
    conn = connect()
    cursor = conn.cursor()
    for pair in game_pairs:
        cursor.execute("insert into matches (player_one, player_two) values(%d,%d)" % (pair[0],pair[2]))
        conn.commit()
    conn.close()

def get_sorted_matches(matches):
    sorted_matches = []
    for match in matches:
        sorted_matches.append(sorted(match))
    return sorted_matches

def get_matches():
    conn = connect()
    c = conn.cursor()
    c.execute("select * from matches")
    return c.fetchall()

def get_game_pairs(order, standings):
    game_pairs = [(standings[i][0], standings[i][1]) for i in order]
    return [game_pairs[i] + game_pairs[i+1] for i in range(0, len(order), 2)]

def get_random_pairs(low,high,rand_order=[]):
    while len(rand_order) <= high:
        randNum = random.randint(low,high)
        if not randNum in rand_order:
            rand_order.append(randNum)
        else:
            get_random_pairs(low,high,rand_order)
    return rand_order
