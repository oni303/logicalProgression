BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `training` (
	`ID`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`sessionID`	INTEGER,
	`exersiseID`	INTEGER,
	`sets`	INTEGER,
	`reps`	INTEGER
);
CREATE TABLE IF NOT EXISTS `sessions` (
	`ID`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`date`	INTEGER,
	`type`	TEXT,
	`climbDuration`	INTEGER,
	`trainingDuration`	INTEGER,
	`density`	REAL,
	`sum`	INTEGER,
	`avgGrade`	REAL,
	`avgSent`	REAL
);
CREATE TABLE IF NOT EXISTS `exersises` (
	`ID`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT UNIQUE,
	`muscleGroup`	TEXT,
	`multiplier`	REAL
);
CREATE TABLE IF NOT EXISTS `boulder` (
	`ID`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`sessionID`	INTEGER,
	`grade`	INTEGER,
	`tries`	INTEGER,
	`sent`	INTEGER,
	`steepness`	REAL,
	`holdType`	TEXT,
	`comment`	TEXT
);
COMMIT;
