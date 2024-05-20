import sqlite3
import uuid
from model.DataModel import DataModel
from model.sport import Sport
from model.athlete import Athlete
from model.SearchModel import SearchModel


class DbModel(DataModel):
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Sports (
                    name TEXT,
                    athletes_number INTEGER,
                    id TEXT PRIMARY KEY  
                )
            """)

        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Athletes (
                    sport_id INTEGER,
                    name TEXT,
                    cast TEXT,
                    position TEXT,
                    title INTEGER,
                    rank TEXT,
                    id TEXT PRIMARY KEY,
                    FOREIGN KEY (sport_id) REFERENCES Sports(id)
                )
            """)
        self.conn.commit()

    def get_cursor(self):
        return self.conn.cursor()

    def add_athlete(self, sport_name: str, name: str, cast: str, position: str, title: str, rank: str):
        athlete_id = str(uuid.uuid4())
        cursor = self.get_cursor()

        cursor.execute("SELECT athletes_number FROM Sports WHERE name = ?", (sport_name,))
        result = cursor.fetchone()
        if result:
            current_athletes_number = result[0]
        else:
            current_athletes_number = 0
        new_athletes_number = current_athletes_number + 1
        self.conn.execute("BEGIN TRANSACTION")
        cursor.execute("UPDATE Sports SET athletes_number = ? WHERE name = ?",
                       (new_athletes_number, sport_name))

        cursor.execute("""
            INSERT INTO Athletes (sport_id, name, cast, position, title, rank, id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (sport_name, name, cast, position, title, rank, athlete_id))
        self.conn.commit()

    def add_sport(self, name, athletes_number):
        sport_id = str(uuid.uuid4())
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO sports (name, athletes_number, id)
            VALUES (?, ?, ?)
        """, (name, athletes_number, sport_id))
        self.conn.commit()

    def get_athletes(self) -> list[Athlete]:
        self.cursor.execute('SELECT * FROM Athletes')
        tuple_list: list[tuple] = self.cursor.fetchall()
        athletes_list: list[Athlete] = []
        for i in tuple_list:
            athletes_list.append(Athlete(*i))
        return athletes_list

    def get_sports(self) -> list[Sport]:
        self.cursor.execute('SELECT * FROM Sports')
        tuple_list: list[tuple] = self.cursor.fetchall()
        sports_list: list[Sport] = []
        for i in tuple_list:
            sports_list.append(Sport(*i))
        return sports_list

    def get_sport_by_name(self, name) -> Sport | None:
        self.cursor.execute('SELECT * FROM Sports WHERE name=?', (name,))
        sport_tuple = self.cursor.fetchone()
        if sport_tuple:
            return Sport(*sport_tuple)
        else:
            return None

    def get_sport_name(self):
        sports = self.get_sports()
        sport_names = [sport['name'] for sport in sports]
        return sport_names

    def athlete_exists(self, sport_name, name, cast, position, title, rank):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM Athletes
            WHERE sport_id = ? AND name = ? AND "cast" = ? AND position = ? AND title = ? AND "rank" = ?
        """, (sport_name, name, cast, position, title, rank,))
        count = cursor.fetchone()[0]
        return count > 0

    def sport_exists(self, name):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM Sports
            WHERE name = ? """, (name,))
        count = cursor.fetchone()[0]
        return count > 0

    def search_athletes(self, search: SearchModel) -> list[Athlete]:
        conditions = []
        params = []

        if search.name:
            conditions.append('name LIKE ?')
            params.append('%' + search.name + '%')
        if search.sport_name:
            conditions.append('sport_id LIKE ?')
            params.append('%' + search.sport_name + '%')
        if search.title_min is not None and search.title_max is not None:
            conditions.append('title BETWEEN ? AND ?')
            params.extend([search.title_min, search.title_max])
        if search.rank:
            conditions.append('rank = ?')
            params.append(search.rank)

        query = 'SELECT * FROM athletes WHERE ' + ' AND '.join(conditions)
        self.cursor.execute(query, params)

        search_list: list[tuple] = self.cursor.fetchall()
        search_athlete_list: list[Athlete] = []
        for i in search_list:
            search_athlete_list.append(Athlete(*i))
        return search_athlete_list

    def delete_athletes(self, search: SearchModel) -> int:

        search_results = self.search_athletes(search)
        num_of_matched_athletes = len(search_results)

        cursor = self.get_cursor()
        for sport_name in [athlete.get_sport_name() for athlete in search_results]:
            cursor.execute("SELECT athletes_number FROM Sports WHERE name = ?", (sport_name,))
            result = cursor.fetchone()
            if result:
                current_athletes_number = result[0]
            else:
                current_athletes_number = 0
            new_athletes_number = current_athletes_number - 1
            self.conn.execute("BEGIN TRANSACTION")
            cursor.execute("UPDATE Sports SET athletes_number = ? WHERE name = ?",
                           (new_athletes_number, sport_name))
            self.conn.execute("END TRANSACTION")

        conditions = []
        params = []

        if search.name:
            conditions.append('name LIKE ?')
            params.append('%' + search.name + '%')
        if search.sport_name:
            conditions.append('sport_id LIKE ?')
            params.append('%' + search.sport_name + '%')
        if search.title_min is not None and search.title_max is not None:
            conditions.append('title BETWEEN ? AND ?')
            params.extend([search.title_min, search.title_max])
        if search.rank:
            conditions.append('rank = ?')
            params.append(search.rank)

        query = 'DELETE FROM athletes WHERE ' + ' AND '.join(conditions)
        self.cursor.execute(query, params)
        self.conn.commit()

        return num_of_matched_athletes

    def get_sport_name_by_id(self, sport_id):
        sport_name = self.cursor.execute('SELECT name FROM sports WHERE id = ?', (sport_id,)).fetchone()
        return sport_name[0] if sport_name else None

    def get_sport_id_by_name(self, sport_name):
        query = "SELECT id FROM sports WHERE name = ?"

        result = self.cursor.execute(query, (sport_name,)).fetchone()
        return result[0] if result else None

    def count_athletes_amount(self) -> int:
        self.cursor.execute('SELECT COUNT(*) FROM athletes')
        return int(self.cursor.fetchone()[0])

    def count_sports_amount(self) -> int:
        self.cursor.execute('SELECT COUNT(*) FROM sports')
        return int(self.cursor.fetchone()[0])

