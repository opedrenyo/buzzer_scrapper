CREATE TABLE countries(
	id_country SERIAL PRIMARY KEY,
	country VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE players(
	id_player INTEGER PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	age SMALLINT NOT NULL
);

CREATE TABLE linktable(
	id_link SERIAL PRIMARY KEY,
	id_country INTEGER REFERENCES countries(id_country),
	id_player INTEGER REFERENCES players(id_player),
	id_season SMALLINT NOT NULL
);

CREATE TABLE performance(
	id_link INTEGER REFERENCES linktable(id_link),
	week SMALLINT NOT NULL,
	DMI INTEGER NOT NULL,
	shape SMALLINT NOT NULL,
	PRIMARY KEY(id_link, week)
);