-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


CREATE TABLE PLAYERS (
  ID SERIAL PRIMARY KEY,
  NAME TEXT
);

CREATE TABLE STANDINGS (
  PLAYER_ID INTEGER REFERENCES PLAYERS(ID),
  WINS INTEGER,
  MATCHES INTEGER
);

CREATE TABLE MATCHES (
  ID SERIAL PRIMARY KEY,
  PLAYER_ONE INTEGER REFERENCES PLAYERS(ID),
  PLAYER_TWO INTEGER REFERENCES PLAYERS(ID)
);
