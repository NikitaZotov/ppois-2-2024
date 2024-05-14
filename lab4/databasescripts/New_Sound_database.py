from Television import Television
from Sound_system import Sound_system
import sqlite3


conn = sqlite3.connect('../lab4scripts/templates/sound_database.db')
c = conn.cursor()


c.execute("DROP TABLE IF EXISTS Sound_Info")

c.execute('''CREATE TABLE IF NOT EXISTS Sound_Info
             (soundlevel TEXT)''')


TV1 = Television('LG', '2500$', 'Grey')
sound = Sound_system()
sound.change_sound_level(54)


sound1_info = (sound.sound_level)
c.execute("INSERT INTO Sound_Info VALUES (?)", (sound1_info,))


conn.commit()
conn.close()
