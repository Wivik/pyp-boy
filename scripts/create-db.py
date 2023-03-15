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

with open('../sql/game_db_story.sql', 'r') as file:
    sql = file.read()
    c.execute(sql)
    conn.commit()

with open('../sql/game_db_version.sql', 'r') as file:
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

        c.execute('INSERT INTO story VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', row)

    conn.commit()

    conn.close()
