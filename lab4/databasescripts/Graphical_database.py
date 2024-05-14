from Television import Television
from Screen import Screen
import sqlite3


conn = sqlite3.connect('../lab4scripts/templates/graphical_database.db')
c = conn.cursor()


c.execute("DROP TABLE IF EXISTS Graphical_Info")

c.execute('''CREATE TABLE IF NOT EXISTS Graphical_Info
             (britness TEXT, contrast TEXT, saturation TEXT)''')


TV1 = Television('LG', '2500$', 'Grey')
screen = Screen()


screen1_info = (screen.britness, screen.contrast, screen.saturation)
c.execute("INSERT INTO Graphical_Info VALUES (?, ?, ?)", screen1_info)


conn.commit()
conn.close()
