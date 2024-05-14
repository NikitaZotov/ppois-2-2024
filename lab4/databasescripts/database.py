from Television import Television
import sqlite3


conn = sqlite3.connect('../lab4scripts/templates/television_database.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS TelevisionInfo
             (model TEXT, price TEXT, color TEXT, operation_system TEXT, software_version TEXT)''')


TV1 = Television('LG', '2500$', 'Grey')
TV1.set_software('webOS', '3.41')


TV1_info = (TV1._model, TV1._price, TV1._color, TV1.operation_system, TV1.software_version)
c.execute("INSERT INTO TelevisionInfo VALUES (?, ?, ?, ?, ?)", TV1_info)


conn.commit()
conn.close()
