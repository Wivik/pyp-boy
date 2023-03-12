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
    results = conn.execute(query, values).fetchone()
    conn.close()
    return results

def run_db_select_all_query(db_file, query, values):
    conn = get_db_connection(db_file)
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
            CREATE TABLE IF NOT EXISTS saves
            (id INTEGER PRIMARY KEY, name TEXT UNIQUE, date_create TEXT, date_update TEXT)
        ''')
        conn.commit()
    except Error as e:
        print(e)
    finally:
        conn.close()

def create_character(save_file, character_name):
    now = datetime.utcnow()
    iso8601 = now.isoformat()
    date_create = iso8601
    date_update = iso8601
    ret = run_db_change_query(save_file, 'INSERT INTO saves (name, date_create, date_update) VALUES(?, ?, ?)', (character_name, date_create, date_update))
    if ret is None:
        return
    else:
        return ret

def list_save_data(save_file):
    ret = run_db_select_all_query(save_file, 'SELECT id, name FROM saves ORDER BY date_update DESC', '')
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
    now = datetime.utcnow()
    iso8601 = now.isoformat()
    ret = run_db_change_query(save_file, 'UPDATE saves set current_chapter = ?, current_step = ?, current_xp = ?, level= ?, date_update = ? WHERE id = ?', (chapter_id, step_id, current_xp, level, iso8601, save_id))
    if ret is None:
        return
    else:
        return ret

