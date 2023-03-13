CREATE TABLE "saves" (
    "id"  INTEGER,
    "name"  TEXT NOT NULL UNIQUE,
    "date_create"  TEXT,
    "date_update"  TEXT,
    "level"  TEXT NOT NULL DEFAULT 1,
    "current_xp"  NUMERIC NOT NULL DEFAULT 0,
    "current_chapter"  INTEGER NOT NULL DEFAULT 1,
    "current_step"  INTEGER NOT NULL DEFAULT 1,
    KEY("id")
)