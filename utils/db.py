import sqlite3
from sqlite3.dbapi2 import Error
from datetime import datetime

## open the database connection
def get_db_connection(db_file, logger):
    logger.debug('Open sqlite file ' + str(db_file))
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn

def run_db_change_query(db_file, query, values, logger):
    conn = get_db_connection(db_file, logger=logger)
    try:
        logger.debug(query)
        logger.debug(values)
        conn.execute(query, values)
        conn.commit()
        conn.close()
        return
    except sqlite3.IntegrityError:
        return sqlite3.IntegrityError
    except sqlite3.Error as er:
        return er
    finally:
        if conn:
            conn.close()

def run_db_select_one_query(db_file, query, values, logger):
    conn = get_db_connection(db_file, logger)
    logger.debug(query)
    logger.debug(values)
    results = conn.execute(query, values).fetchone()
    conn.close()
    return results

def run_db_select_all_query(db_file, query, values, logger):
    conn = get_db_connection(db_file, logger)
    logger.debug(query)
    logger.debug(values)
    results = conn.execute(query, values).fetchall()
    conn.close()
    return results


def create_save_database(save_file, logger):
    conn = None
    try:
        conn = sqlite3.connect(save_file)
        c = conn.cursor()
        # Create the saves table
        c.execute('''
            CREATE TABLE "saves" (
            "id"	INTEGER,
            "name"	TEXT NOT NULL UNIQUE,
            "date_create"	TEXT,
            "date_update"	TEXT,
            "level"	TEXT NOT NULL DEFAULT 1,
            "current_xp"	NUMERIC NOT NULL DEFAULT 0,
            "current_chapter"	INTEGER NOT NULL DEFAULT 1,
            "current_step"	INTEGER NOT NULL DEFAULT 1,
            "failed"	INTEGER NOT NULL DEFAULT 0,
            "gender"	TEXT,
            PRIMARY KEY("id")
        )
        ''')
        c.execute('''
            CREATE TABLE "story_path" (
                "save_id"	INTEGER,
                "chapter"	INTEGER NOT NULL,
                "step"	INTEGER NOT NULL,
                CONSTRAINT "pk" PRIMARY KEY("save_id","chapter","step")
            );
        ''')
        c.execute('''
            CREATE TABLE "inventories" (
                "id"	INTEGER,
                "save_id"	INTEGER NOT NULL,
                "item_id"	INTEGER NOT NULL,
                "type"	TEXT NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            )
        ''')
        c.execute('''
            CREATE TABLE "locations" (
                "id"	INTEGER,
                "save_id"	INTEGER,
                "location"	INTEGER,
                PRIMARY KEY("id" AUTOINCREMENT),
                UNIQUE("save_id","location")
            )
        ''')
        conn.commit()
    except Error as e:
        logger.error(e)
    finally:
        conn.close()

def create_character(save_file, character_name, gender, logger):
    now = datetime.utcnow()
    iso8601 = now.isoformat()
    date_create = iso8601
    date_update = iso8601
    ret = run_db_change_query(save_file, 'INSERT INTO saves (name, gender, date_create, date_update) VALUES(?, ?, ?, ?)', (character_name, gender, date_create, date_update), logger)
    if ret is None:
        return
    else:
        return ret

def list_save_data(save_file, logger):
    ret = run_db_select_all_query(save_file, 'SELECT id, name, failed FROM saves ORDER BY date_update DESC', '', logger=logger)
    if ret is None:
        return
    else:
        return ret

def get_save_data(save_file, save_id, logger):
    ret = run_db_select_one_query(save_file, 'SELECT * FROM saves WHERE id = ?', (save_id,), logger)
    if ret is None:
        return
    else:
        return ret

def get_chapter_step(game_file, chapter, step, logger):
    ret = run_db_select_one_query(game_file, 'SELECT * FROM story WHERE chapter = ? and step = ?', (chapter, step,), logger)
    if ret is None:
        return
    else:
        return ret

def save_progress(save_file, save_id, logger, **kwargs):
    chapter_id = kwargs.get('chapter')
    step_id = kwargs.get('step')
    current_xp = kwargs.get('current_xp')
    level = kwargs.get('level')
    end = kwargs.get('end', 0)
    now = datetime.utcnow()
    iso8601 = now.isoformat()
    ret = run_db_change_query(save_file, 'UPDATE saves set current_chapter = ?, current_step = ?, current_xp = ?, level= ?, date_update = ?, failed = ? WHERE id = ?', (chapter_id, step_id, current_xp, level, iso8601, end, save_id), logger)
    if ret is None:
        return
    else:
        return ret

def get_game_db_version(game_file, logger):
    ret = run_db_select_one_query(game_file, 'SELECT * FROM db_version', '', logger)
    if ret is None:
        return
    else:
        return ret

def get_inventory(save_file, save_id, logger, filter=''):
    ret = run_db_select_all_query(save_file, 'SELECT * FROM inventories WHERE save_id = ? AND type = ?', (save_id, filter), logger=logger)
    if ret is None:
        return
    else:
        return ret

def get_inv_items(game_file, items, item_type, logger):
    if len(items) == 1:
        for item in items:
            list_items = item
        list_items = '('+ str(list_items) +')'
    else:
        list_items = str(tuple(items))
    query = f'SELECT * FROM {item_type} WHERE id IN {list_items} ORDER BY name ASC'
    ret = run_db_select_all_query(game_file, query, '', logger)
    if ret is None:
        return
    else:
        return ret

def get_item(game_file, db, item_id, logger):
    ret = run_db_select_one_query(game_file, 'SELECT * FROM '+ db +' WHERE id = ?', (item_id,), logger)
    if ret is None:
        return
    else:
        return ret

def add_item(save_file, save_id, item_id, item_type, logger):
    ret = run_db_change_query(save_file, 'INSERT INTO inventories (save_id, item_id, type) VALUES(?, ?, ?)', (save_id, item_id, item_type), logger)
    if ret is None:
        return
    else:
        return ret

def loot(save_file, save_id, items, logger):
    logger.debug('items ' + str(items))
    for loot in items.split(';'):
        logger.debug('loot '+ str(loot))
        item_type, item_id = loot.split(':')
        logger.debug('item_type ' + str(item_type))
        logger.debug('item_id ' + str(item_id))
        add_item(save_file, save_id, int(item_id), item_type, logger)

def save_story_path(save_file, save_id, chapter, step, logger):
    ret = run_db_change_query(save_file, 'INSERT INTO story_path (save_id, chapter, step) VALUES(?, ?, ?)', (save_id, chapter, step), logger)
    if ret is None:
        return
    else:
        return ret

def get_story_path(save_file, save_id, logger):
    ret = run_db_select_all_query(save_file, 'SELECT * FROM story_path WHERE save_id = ? ORDER BY chapter, step ASC', (save_id,), logger)
    if ret is None:
        return
    else:
        return ret

def discover_location(save_file, save_id, location, logger):
    ret = run_db_change_query(save_file, 'INSERT INTO locations (save_id, location) VALUES(?, ?)', (save_id, location), logger)
    if ret is None:
        return
    else:
        return ret

def get_discovered_locations(save_file, game_file, save_id, logger):
    locations = []
    get_locations = run_db_select_all_query(save_file, 'SELECT id FROM locations WHERE save_id = ?', (save_id,), logger)
    for location in get_locations:
        locations.append(location['id'])
    if len(locations) == 1:
        for location in locations:
            list_locations = location
        list_locations = '('+ str(list_locations) +')'
    else:
        list_locations = str(tuple(locations))
    query = f'SELECT * FROM map WHERE id IN {list_locations} ORDER BY name ASC'
    ret = run_db_select_all_query(game_file, query, '', logger)
    if ret is None:
        return
    else:
        return ret

def get_location(game_file, location, logger):
    ret = run_db_select_one_query(game_file, 'SELECT * FROM map WHERE id = ?', (location,), logger)
    if ret is None:
        return
    else:
        return ret
