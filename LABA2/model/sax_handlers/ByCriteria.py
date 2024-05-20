import uuid
import xml.sax
from model.SearchModel import SearchModel


class AthleteByCriteriaHandler(xml.sax.ContentHandler):
    def __init__(self, search: SearchModel):
        self.result = []
        self.current_athlete = {}
        self.current_tag = None
        self.search = search

    def startElement(self, name, attrs):
        if name == 'athlete':
            athlete_id = attrs.get('id', str(uuid.uuid4()))
            self.current_athlete = {
                'sport_name': attrs.get('sport_name'),
                'name': attrs.get('name'),
                'cast': attrs.get('cast'),
                'position': attrs.get('position'),
                'title': attrs.get('title'),
                'rank': attrs.get('rank'),
                'id': athlete_id,
            }
        else:
            self.current_tag = name

    def characters(self, content):
        pass

    def endElement(self, name):
        if name == 'athlete':
            conditions = []
            if self.search.name:
                conditions.append(self.current_athlete['name'].lower().find(self.search.name.lower()) != -1)
            if self.search.sport_name:
                conditions.append(self.current_athlete['sport_name'].lower().find(self.search.sport_name.lower()) != -1)
            if self.search.title_min is not None and self.search.title_max is not None:
                title = int(self.current_athlete['title'])
                conditions.append(int(self.search.title_min) <= title <= int(self.search.title_max))
            if self.search.rank:
                conditions.append(self.current_athlete['rank'] == self.search.rank)

            if all(conditions):
                self.result.append(self.current_athlete)
