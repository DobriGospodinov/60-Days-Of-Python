import sqlite3

# Establish a connection and a cursor
connection = sqlite3.connect("data.db")
cursor = connection.cursor()

# Query all data, based on a condition
cursor.execute("SELECT * FROM events WHERE date='2022.10.11'")
rows = cursor.fetchall()
print(rows) # [('Lions', 'Lion City', '2022.10.11'), ('Tigers', 'Tiger City', '2022.10.11')]

# Query certain columns, based on a condition
cursor.execute("SELECT band, city FROM events WHERE date='2022.10.11'")
rows = cursor.fetchall()
print(rows) # [('Lions', 'Lion City'), ('Tigers', 'Tiger City')]

# Insert new rows
new_rows = [('Cats', 'Cat City', '2022.10.17'),
            ('Dogs', 'Dogo City', '2022.11.17')]

cursor.executemany("INSERT INTO events VALUES(?,?,?)", new_rows)
connection.commit()

# Select absolutely all data
cursor.execute("SELECT * FROM events")
rows = cursor.fetchall()
print(rows)