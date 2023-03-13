-- CREATE TABLE sqlite_sequence(name,seq)

CREATE TABLE "story" (
	"id"	INTEGER,
	"chapter"	INTEGER NOT NULL,
	"step"	INTEGER NOT NULL,
	"text"	TEXT,
	"choice_1"	INTEGER,
	"choice_2"	INTEGER,
	"choice_3"	INTEGER,
	"img"	TEXT,
	"end"	INTEGER DEFAULT 0,
	"choice_1_desc"	TEXT,
	"choice_2_desc"	TEXT,
	"choice_3_desc"	TEXT,
	"exp"	INTEGER DEFAULT 100,
	PRIMARY KEY("id" AUTOINCREMENT)
)