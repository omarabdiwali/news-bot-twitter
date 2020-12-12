import sqlite3

#Create new database
name = 'enter Database Name (end it with .db)'
conn = sqlite3.connect(name)
c = conn.cursor()

#Create a table in the database
c.execute("""create Articles(ids integer, headline string)""")

conn.commit()
conn.close()
