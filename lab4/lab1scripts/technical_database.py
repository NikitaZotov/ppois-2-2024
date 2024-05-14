
from Technical_characteristics import Technic_charact
import sqlite3


conn = sqlite3.connect('../lab4scripts/templates/technical_database.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS Technical_Info
             (screen_diagonal TEXT, screen_resolution TEXT, matrix_type TEXT)''')


TC = Technic_charact('17 inches', '1280x720', 'LED')


TC_info = (TC._screen_diagonal, TC._screen_resolution, TC._matrix_type)
c.execute("INSERT INTO Technical_Info VALUES (?, ?, ?)", TC_info)


conn.commit()
conn.close()
