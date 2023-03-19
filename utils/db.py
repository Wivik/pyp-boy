import sqlite3
from sqlite3.dbapi2 import Error
from datetime import datetime

## open the database connection
def get_db_connection(db_file):
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn

def run_db_change_query(db_file, query, values):
        conn = get_db_connection(db_file)
        try:
            print(query)
            print(values)
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

def run_db_select_one_query(db_file, query, values):
    conn = get_db_connection(db_file)
    print(query)
    print(values)
    results = conn.execute(query, values).fetchone()
    conn.close()
    return results

def run_db_select_all_query(db_file, query, values):
    conn = get_db_connection(db_file)
    print(query)
    print(values)
    results = conn.execute(query, values).fetchall()
    conn.close()
    return results


def create_save_database(save_file):
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
        conn.commit()
    except Error as e:
        print(e)
    finally:
        conn.close()

def create_character(save_file, character_name, gender):
    now = datetime.utcnow()
    iso8601 = now.isoformat()
    date_create = iso8601
    date_update = iso8601
    ret = run_db_change_query(save_file, 'INSERT INTO saves (name, gender, date_create, date_update) VALUES(?, ?, ?, ?)', (character_name, gender, date_create, date_update))
    if ret is None:
        return
    else:
        return ret

def list_save_data(save_file):
    ret = run_db_select_all_query(save_file, 'SELECT id, name, failed FROM saves ORDER BY date_update DESC', '')
    if ret is None:
        return
    else:
        return ret

def get_save_data(save_file, save_id):
    ret = run_db_select_one_query(save_file, 'SELECT * FROM saves WHERE id = ?', (save_id,))
    if ret is None:
        return
    else:
        return ret

def get_chapter_step(game_file, chapter, step):
    ret = run_db_select_one_query(game_file, 'SELECT * FROM story WHERE chapter = ? and step = ?', (chapter, step,))
    if ret is None:
        return
    else:
        return ret

def save_progress(save_file, save_id, **kwargs):
    chapter_id = kwargs.get('chapter')
    step_id = kwargs.get('step')
    current_xp = kwargs.get('current_xp')
    level = kwargs.get('level')
    end = kwargs.get('end', 0)
    now = datetime.utcnow()
    iso8601 = now.isoformat()
    ret = run_db_change_query(save_file, 'UPDATE saves set current_chapter = ?, current_step = ?, current_xp = ?, level= ?, date_update = ?, failed = ? WHERE id = ?', (chapter_id, step_id, current_xp, level, iso8601, end, save_id))
    if ret is None:
        return
    else:
        return ret

def get_game_db_version(game_file):
    ret = run_db_select_one_query(game_file, 'SELECT * FROM db_version', '')
    if ret is None:
        return
    else:
        return ret

def get_inventory(save_file, save_id, filter=''):
    ret = run_db_select_all_query(save_file, 'SELECT * FROM inventories WHERE save_id = ? AND type = ?', (save_id, filter))
    if ret is None:
        return
    else:
        return ret

def get_inv_items(game_file, items, item_type):
    if len(items) == 1:
        for item in items:
            list_items = item
        list_items = '('+ str(list_items) +')'
    else:
        list_items = str(tuple(items))
    query = f'SELECT * FROM {item_type} WHERE id IN {list_items} ORDER BY name ASC'
    ret = run_db_select_all_query(game_file, query, '')
    if ret is None:
        return
    else:
        return ret

def get_item(game_file, db, item_id):
    ret = run_db_select_one_query(game_file, 'SELECT * FROM '+ db +' WHERE id = ?', (item_id,))
    if ret is None:
        return
    else:
        return ret

def add_item(save_file, save_id, item_id, item_type):
    ret = run_db_change_query(save_file, 'INSERT INTO inventories (save_id, item_id, type) VALUES(?, ?, ?)', (save_id, item_id, item_type))
    if ret is None:
        return
    else:
        return ret

def loot(save_file, save_id, items):
    print('items')
    print(items)
    for loot in items.split(';'):
        print('loot')
        print(loot)
        item_type, item_id = loot.split(':')
        print(item_type)
        print(item_id)
        add_item(save_file, save_id, int(item_id), item_type)


