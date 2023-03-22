import sqlite3
import csv
import json

## load json version file

version_file = open('../version_file.json', 'r')
version = json.load(version_file)
print(version['version'])
version = str(version['version'])

conn = sqlite3.connect('game.db')
c = conn.cursor()

game_db_files = [
    '../sql/game_db_story.sql',
    '../sql/game_db_weapon.sql',
    '../sql/game_db_apparel.sql',
    '../sql/game_db_aid.sql',
    '../sql/game_db_misc.sql',
    '../sql/game_db_version.sql',
]

for game_db_file in game_db_files:
    with open(game_db_file, 'r') as file:
        sql = file.read()
        c.execute(sql)
        conn.commit()



c.execute('INSERT INTO db_version values(?)', (version,))
conn.commit()

with open('../sql/story.csv', 'r') as story_file:
    story = csv.reader(story_file)

    for row in story:
        # print(row)
        row = [None if value.strip() == '' else value.strip() for value in row]

        c.execute('INSERT INTO story VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', row)

    conn.commit()

    conn.close()

inventory_files = [
    {'name': 'apparel', 'file': '../sql/apparel.csv'},
    {'name': 'weapon', 'file': '../sql/weapon.csv'},
    {'name': 'misc', 'file': '../sql/misc.csv'},
]


conn = sqlite3.connect('game.db')
c = conn.cursor()

for inv_file in inventory_files:

    with open(inv_file['file'], 'r') as load_inv_file:
        inv = csv.reader(load_inv_file)

        for row in inv:
            # print(row)

            c.execute('INSERT INTO '+ inv_file['name'] +' VALUES (?, ?, ?, ?, ?)', (row))

conn.commit()

conn.close()



