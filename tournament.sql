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
  winner INTEGER REFERENCES players(id) ON DELETE CASCADE,
  loser INTEGER REFERENCES players(id) ON DELETE CASCADE,
  draw BOOLEAN
);

create table match_players(
  id serial PRIMARY KEY,
  player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
  match_id INTEGER REFERENCES matches(id) ON DELETE CASCADE
);
-- CREATE TABLE match_players(
--   id SERIAL PRIMARY KEY,
--   player_id INTEGER REFERENCES players(id),
--   match_id INTEGER REFERENCES matches(id)
-- );

CREATE VIEW standings AS
SELECT players.id, players.name,
(SELECT count(*) FROM matches WHERE players.id = matches.winner) AS wins,
(SELECT count(*) FROM matches WHERE players.id = matches.winner OR players.id = matches.loser ) AS matches
FROM players ORDER BY wins DESC;
