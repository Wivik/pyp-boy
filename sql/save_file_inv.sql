CREATE TABLE "inventories" (
	"id"	INTEGER,
	"save_id"	INTEGER NOT NULL,
	"item_id"	INTEGER NOT NULL,
	"type"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
)