-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;
-- Players table definition
CREATE TABLE players (
    player_id SERIAL PRIMARY KEY,
    name TEXT
    );

-- matches table definition
CREATE TABLE matches (
    match_id SERIAL PRIMARY KEY,
    -- winner is foreign key from players table
    winner INTEGER references players (player_id),
    -- loser is a foreign key from players table
    loser INTEGER references players (player_id)
    );



-- Winstats is a view that computes statistics of how many wins a player has had
CREATE VIEW winstats AS
SELECT DISTINCT
    p.player_id,
    count(m.match_id) as wincount
FROM
    players p, matches m
WHERE
    p.player_id = m.winner
GROUP BY
    p.player_id
ORDER BY wincount DESC;


-- totalstats is a view that computes statistics of how many total matches a
-- player has played
CREATE VIEW totalstats AS
SELECT DISTINCT
    p.player_id,
    count(m.match_id) as totalmatchcount
FROM
    players p, matches m
WHERE
    p.player_id = m.winner OR p.player_id = m.loser
GROUP BY
    p.player_id
ORDER BY totalmatchcount DESC;


-- playerstats is a view that computes match statistics by player id and name
CREATE VIEW playerstats AS
SELECT
    p.player_id, p.name,
    COALESCE(w.wincount,0) as wincount,
    COALESCE(t.totalmatchcount,0) as totalmatchcount
FROM
    players p
    LEFT JOIN winstats w ON p.player_id = w.player_id
    LEFT JOIN totalstats t ON p.player_id = t.player_id
ORDER BY
    w.wincount DESC;