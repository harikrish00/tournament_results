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

4545
def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("update standings set matches=0,wins=0");
    conn.commit()
    cursor.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('delete from standings;')
    cursor.execute('delete from players;')
    conn.commit()
    cursor.close()

def countPlayers():
    """Returns the number of players currently registered."""
    cursor = connect().cursor()
    cursor.execute("select * from players")
    count = len(cursor.fetchall())
    cursor.close()
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
    cursor.execute("select max(id) from players")
    player_id = cursor.fetchone()[0]
    cursor.execute("insert into standings (player_id, wins, matches) values (%d, 0, 0)" % player_id)
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
    cursor.execute("""select players.id, players.name, standings.wins, standings.matches from
    players join standings on players.id = standings.player_id order by standings.wins desc""")
    standings = cursor.fetchall()
    cursor.close()
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    #cursor.execute("select * from players where id = %d" % (winner))
    #winner = cursor.fetchone()
    #wins = winner[2] + 1
    cursor.execute("update standings set wins = wins+1, matches = matches+1 where player_id = %d" % winner)
    cursor.execute("update standings set matches = matches+1 where player_id = %d" % loser)
    conn.commit()
    cursor.close()


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
    game_pairs = get_game_pairs(order, total_players, standings)
    storePlayerPairings(game_pairs)
    return game_pairs

def storePlayerPairings(pairing):
    conn = connect()
    cursor = conn.cursor()
    for p in pairing:
        player_id1 = p[0]
        player_id2 = p[2]
        cursor.execute("insert into matches (player_one, player_two) values(%d,%d)" % (player_id1, player_id2))
        conn.commit()
    conn.close()

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
