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

def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("delete from matches");
    conn.commit()
    cursor.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('delete from players;')
    conn.commit()
    conn.close()

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

def reportMatch(winner, loser, draw = False):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("insert into matches(winner, loser) values(%d, %d)" % (winner,loser))
    conn.commit()
    cursor.execute("select max(id) from matches")
    match_id = cursor.fetchone()[0]
    cursor.execute("insert into match_players (player_id, match_id) values (%d,%d)" % (winner,match_id))
    cursor.execute("insert into match_players (player_id, match_id) values (%d,%d)" % (loser,match_id))
    conn.commit()
    conn.close()

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
    game_pairs = get_game_pairs(order, total_players, standings)
    return game_pairs

def get_sorted_matches(matches):
    sorted_matches = []
    for match in matches:
        sorted_matches.append(sorted(match))
    return sorted_matches

def get_matches():
    conn = connect()
    c = conn.cursor()
    c.execute("select winner, loser from matches")
    return c.fetchall()

def get_game_pairs(order, total_pairings, standings):
    game_pairs = [(standings[i][0], standings[i][1]) for i in order]
    return [game_pairs[i] + game_pairs[i+1] for i in range(0, total_pairings, 2)]

def get_random_pairs(low,high,rand_order=[]):
    while len(rand_order) <= high:
        randNum = random.randint(low,high)
        if not randNum in rand_order:
            rand_order.append(randNum)
        else:
            get_random_pairs(low,high,rand_order)
    return rand_order
