-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE matches (
  id SERIAL PRIMARY KEY,
  player_one INTEGER REFERENCES players(id) ON DELETE CASCADE,
  player_two INTEGER REFERENCES players(id) ON DELETE CASCADE
);

CREATE TABLE match_results (
  id SERIAL PRIMARY KEY,
  match_id INTEGER REFERENCES matches(id) ON DELETE CASCADE,
  winner INTEGER REFERENCES players(id) ON DELETE CASCADE,
  loser INTEGER REFERENCES players(id) ON DELETE CASCADE,
  draw BOOLEAN
);

CREATE TABLE player_match_points(
  id SERIAL PRIMARY KEY,
  match_id INTEGER REFERENCES matches(id) ON DELETE CASCADE,
  player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
  points INTEGER
);

CREATE TABLE player_byes(
    player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
    bye INTEGER DEFAULT 0
);

CREATE VIEW standings AS
SELECT players.t_id, players.id, players.name,
(SELECT count(*) FROM match_results WHERE players.id = match_results.winner and match_results.draw = FALSE AND ) AS wins,
(SELECT count(*) FROM match_results WHERE players.id = match_results.winner OR players.id = match_results.loser ) AS matches,
(SELECT COALESCE(SUM(points), 0) FROM player_match_points WHERE players.id = player_match_points.player_id) AS points
FROM players ORDER BY wins DESC;
