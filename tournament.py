#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    # return psycopg2.connect("dbname=tournament")
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")


def deleteMatches():
    """Remove all the match records from the database."""
    qry = "delete from matches;"
    conn, cursor = connect()
    cursor.execute(qry)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    qry = "TRUNCATE TABLE players CASCADE;"
    conn, cursor = connect()
    cursor.execute(qry)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    qry = "select count(*) from players;"
    conn, cursor = connect()
    cursor.execute(qry)
    results = cursor.fetchone()
    conn.close()
    return results[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    qry = "INSERT INTO players (name) VALUES (%s);"
    params = (name,)
    conn, cursor = connect()
    # pass name as a tuple to avoid sql injection attack
    cursor.execute(qry, params)
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    qry = "SELECT * FROM playerstats;"
    conn, cursor = connect()
    # pass name as a tuple to avoid sql injection attack
    cursor.execute(qry)
    results = cursor.fetchall()
    conn.close()
    return results

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    qry = "INSERT INTO matches (winner, loser) VALUES (%s, %s)"
    conn, cursor = connect()
    params = (winner, loser)
    # pass name as a tuple to avoid sql injection attack
    cursor.execute(qry, params)
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
        sp.append((players[i][0], players[i][1], players[i+1][0],
            players[i+1][1]))
        i = i + 2
    return sp
