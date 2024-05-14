from Television import Television
from Remote_controle import Remote_control
import sqlite3


conn = sqlite3.connect('../lab4scripts/templates/controle_database.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS ControleInfo
             (model TEXT, price TEXT, color TEXT)''')


TV1 = Television('LG', '2500$', 'Grey')
TV1.set_software('webOS', '3.41')
PULT1 = Remote_control('Samsung', '250$', 'Black', TV1)


PULT1_info = (PULT1._model, PULT1._price, PULT1._color)
c.execute("INSERT INTO ControleInfo VALUES (?, ?, ?)", PULT1_info)

# Commit changes and close the connection
conn.commit()
conn.close()
