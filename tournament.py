#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    qry = "delete from matches;"
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(qry)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    qry = "delete from players;"
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(qry)
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    qry = "select * from players;"
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(qry)
    results = cursor.fetchall()
    conn.close()
    return len(results)#if results is not None else 0

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    qry = "INSERT INTO players (name) VALUES (%s);"
    conn = connect()
    cursor = conn.cursor()
    #pass name as a tuple to avoid sql injection attack
    cursor.execute(qry, (name,))
    conn.commit()
    conn.close()

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
    qry = "SELECT p.player_id, p.name, COALESCE(w.wincount,0) as wincount, "\
          "COALESCE(t.totalmatchcount,0) as totalmatchcount "\
          "FROM players p LEFT JOIN winstats w ON p.player_id = w.player_id "\
          "LEFT JOIN totalstats t ON p.player_id = t.player_id "\
          "ORDER BY w.wincount DESC;"
    #ps = []
    conn = connect()
    cursor = conn.cursor()
    #pass name as a tuple to avoid sql injection attack
    cursor.execute(qry)
    results = cursor.fetchall()
    conn.close()
    #ps.append(results)
    #return ps
    return results

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    qry = "INSERT INTO matches (winner, loser) VALUES (%s, %s)"
    conn = connect()
    cursor = conn.cursor()
    #pass name as a tuple to avoid sql injection attack
    cursor.execute(qry, (winner,loser))
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
    players = playerStandings()
    sp = []
    i = 0
    while i < len(players):
        sp.append((players[i][0], players[i][1], players[i+1][0], players[i+1][1]))
        i = i + 2
    return sp




