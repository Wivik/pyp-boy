CREATE TABLE "characters" (
	"id"	INTEGER,
	"save_id"	INTEGER,
	"character_id"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	UNIQUE("save_id","character_id")
);