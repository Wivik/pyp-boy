import sqlite3
import csv

conn = sqlite3.connect('story.db')
c = conn.cursor()

with open('../sql/game.sql', 'r') as file:
    sql = file.read()

    c.execute(sql)
    conn.commit()

with open('../sql/story.csv', 'r') as story_file:
    story = csv.reader(story_file)

    for row in story:
        print(row)
        row = [None if value.strip() == '' else value.strip() for value in row]

        c.execute('INSERT INTO story VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', row)

    conn.commit()

    conn.close()
