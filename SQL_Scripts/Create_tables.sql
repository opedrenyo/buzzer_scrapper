CREATE TABLE countries(
	id_country SERIAL PRIMARY KEY,
	country VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE players(
	id_player INTEGER PRIMARY KEY,
	id_country INTEGER NOT NULL,
	name VARCHAR(100) NOT NULL,
	age SMALLINT NOT NULL
);

CREATE TABLE seasons(
	id_season SMALLINT PRIMARY KEY,
	start_date DATE UNIQUE NOT NULL,
	end_date DATE UNIQUE NOT NULL
);

CREATE TABLE performance(
	id_player INTEGER REFERENCES players(id_player),
	id_season INTEGER REFERENCES seasons(id_season),
	week SMALLINT NOT NULL,
	DMI INTEGER NOT NULL,
	shape SMALLINT NOT NULL,
	PRIMARY KEY(id_player, id_season, week)
);

CREATE TABLE skills(
	id_player INTEGER REFERENCES players(id_player),
	check_date TIMESTAMP NOT NULL,
	jumpshot INTEGER NOT NULL,
	shot_range INTEGER NOT NULL,
	outside_defense INTEGER NOT NULL,
	handling INTEGER NOT NULL,
	driving INTEGER NOT NULL,
	passes INTEGER NOT NULL,
	inside_shot INTEGER NOT NULL,
	inside_defense INTEGER NOT NULL,
	rebounds INTEGER NOT NULL,
	blocks INTEGER NOT NULL,
	resist INTEGER NOT NULL,
	free_throws INTEGER NOT NULL,
	PRIMARY KEY(id_player)
)

-- modificar columnas de tipo date a timestamp para añadir hora, minuto, segundo
ALTER TABLE public.seasons ALTER COLUMN start_date TYPE timestamp USING start_date::timestamp;
ALTER TABLE public.seasons ALTER COLUMN end_date TYPE timestamp USING end_date::timestamp;
