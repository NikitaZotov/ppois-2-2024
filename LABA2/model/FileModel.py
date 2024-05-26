import xml.sax
from model.SearchModel import SearchModel
from model.sax_handlers.ByCriteria import AthleteByCriteriaHandler
from model.sax_handlers.AnyHandler import SportAnyHandler
from model.sax_handlers.AnyHandler import AthleteAnyHandler
from model.DataModel import DataModel

from model.athlete import Athlete
from model.sport import Sport

from xml.dom.minidom import *
import xml.sax
from xml.dom.minidom import parse
from xml.dom.minidom import Document

import uuid


class FileModel(DataModel):
    def __init__(self, path: str):
        self.path = path

    def creation(self):
        doc: Document = getDOMImplementation().createDocument(None, 'LAB2', None)
        doc.documentElement.appendChild(doc.createElement('sports'))
        doc.documentElement.appendChild(doc.createElement('athletes'))
        self._save_doc(doc)

    def _parse_doc(self) -> Document:
        doc = parse(self.path)
        return doc

    def _save_doc(self, doc):
        with open(self.path, 'w') as file:
            file.write(doc.toxml())

    def delete_athletes(self, search: SearchModel) -> int:
        doc: Document = parse(self.path)
        deleted_count: int = 0
        athletes = doc.getElementsByTagName('athlete')
        athletes_to_delete = []
        for athlete in athletes:
            conditions = []
            if search.name:
                conditions.append(athlete.getAttribute('name').lower().find(search.name.lower()) != -1)
            if search.sport_name:
                conditions.append(athlete.getAttribute('sport_name').lower().find(search.sport_name.lower()) != -1)
            if search.title_min is not None and search.title_max is not None:
                title = int(athlete.getAttribute('title'))
                conditions.append(int(search.title_min) <= title <= int(search.title_max))
            if search.rank:
                conditions.append(athlete.getAttribute('rank') == str(search.rank))

            if all(conditions):
                sports_element = doc.getElementsByTagName('sports')[0]
                sport_elements = sports_element.getElementsByTagName('sport')
                for sport_element in sport_elements:
                    if sport_element.attributes['name'].value == athlete.getAttribute('sport_name'):
                        current_athletes_number = int(sport_element.attributes['athletes_number'].value)
                        sport_element.attributes['athletes_number'].value = str(current_athletes_number - 1)
                        break
                athletes_to_delete.append(athlete)
                deleted_count += 1
        for athlete in athletes_to_delete:
            parent = athlete.parentNode
            parent.removeChild(athlete)
        self._save_doc(doc)
        return deleted_count

    def search_athletes(self, search: SearchModel) -> list[Athlete]:
        handler = AthleteByCriteriaHandler(search)
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(self.path)
        dict_athletes: list[dict] = handler.result
        athletes: list[Athlete] = []
        for dict_athlete in dict_athletes:
            athletes.append(Athlete(dict_athlete['sport_name'], dict_athlete['name'],
                                    dict_athlete['cast'], dict_athlete['position'],
                                    dict_athlete['title'], dict_athlete['rank'], uuid.UUID(dict_athlete['id'])))
        return athletes

    def get_athletes(self, search_criteria: SearchModel | None = None) -> list[Athlete]:
        handler = AthleteAnyHandler()

        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(self.path)
        dict_athletes: list[dict] = handler.result
        athletes: list[Athlete] = []

        for dict_athlete in dict_athletes:
            id = uuid.UUID(hex=dict_athlete['id'])
            athletes.append(Athlete(dict_athlete['sport_name'], dict_athlete['name'],
                                    dict_athlete['cast'], dict_athlete['position'],
                                    dict_athlete['title'], dict_athlete['rank'], id))
        return athletes

    def athlete_exists(self, sport_name, name, cast, position, title, rank) -> bool:
        athletes = self.get_athletes()

        for athlete in athletes:
            if (athlete.get_sport_name() == sport_name and athlete.get_name() == name
                    and athlete.get_cast() == cast and athlete.get_position() == position
                    and athlete.get_title() == title and athlete.get_rank() == rank):
                return True
        return False

    def sport_exists(self, name) -> bool:
        sports = self.get_sports()

        for sport in sports:
            if sport.get_name() == name:
                return True
        return False

    def add_athlete(self, sport_name: str, name: str, cast: str, position: str, title: str, rank: str):
        doc = self._parse_doc()

        athlete_element = doc.createElement('athlete')
        athlete_element.attributes['sport_name'] = sport_name
        athlete_element.attributes['name'] = name
        athlete_element.attributes['cast'] = cast
        athlete_element.attributes['position'] = position
        athlete_element.attributes['title'] = title
        athlete_element.attributes['rank'] = rank
        athlete_element.attributes['id'] = uuid.uuid4().__str__()

        sports_element = doc.getElementsByTagName('sports')[0]
        sport_elements = sports_element.getElementsByTagName('sport')
        for sport_element in sport_elements:
            if sport_element.attributes['name'].value == sport_name:
                current_athletes_number = int(sport_element.attributes['athletes_number'].value)
                sport_element.attributes['athletes_number'].value = str(current_athletes_number + 1)
                break

        items_element = doc.getElementsByTagName('athletes')[0]
        items_element.appendChild(athlete_element)

        self._save_doc(doc)

    def add_sport(self, name: str, athletes_number: str) -> None:
        document = self._parse_doc()

        doc_element = document.createElement('sport')
        doc_element.attributes['name'] = name
        doc_element.attributes['athletes_number'] = str(athletes_number)
        doc_element.attributes['id'] = uuid.uuid4().__str__()

        items_element = document.getElementsByTagName('sports')[0]
        items_element.appendChild(doc_element)

        self._save_doc(document)

    def get_sports(self) -> list[Sport]:
        handler = SportAnyHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(self.path)
        dict_sports: list[dict] = handler.result
        sports: list[Sport] = []

        for dict_sport in dict_sports:
            id = uuid.UUID(hex=dict_sport['id'])
            sports.append(Sport(dict_sport['name'], dict_sport['athletes_number'], id))
        return sports

    def get_sport_by_name(self, name) -> Sport | None:
        handler = SportAnyHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(self.path)
        dict_sports: list[dict] = handler.result

        for dict_sport in dict_sports:
            if 'name' in dict_sport and dict_sport['name'] == name:
                id = uuid.UUID(hex=dict_sport['id'])
                return Sport(dict_sport['name'], dict_sport['athletes_number'], id)
        return None

    def count_athletes_amount(self) -> int:
        athletes = self.get_athletes()
        return len(athletes)

    def count_sports_amount(self) -> int:
        sports = self.get_sports()
        return len(sports)

