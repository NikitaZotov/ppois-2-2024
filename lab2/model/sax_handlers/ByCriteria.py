import uuid
import xml.sax
from model.SearchModel import SearchModel


class PlayerByCriteriaHandler(xml.sax.ContentHandler):
    def __init__(self, search: SearchModel):
        self.result = []
        self.current_player = {}
        self.current_tag = None
        self.search = search

    def startElement(self, name, attrs):
        if name == 'player':
            player_id = attrs.get('id', str(uuid.uuid4()))
            self.current_player = {
                'sport_name': attrs.get('sport_name'),
                'name': attrs.get('name'),
                'cast': attrs.get('cast'),
                'position': attrs.get('position'),
                'hometown': attrs.get('hometown'),
                'birthdate': attrs.get('birthdate'),
                'id': player_id,
            }
        else:
            self.current_tag = name

    def characters(self, content):
        pass

    def endElement(self, name):
        if name == 'player':
            conditions = []
            if self.search.name:
                conditions.append(self.current_player['name'].lower().find(self.search.name.lower()) != -1)
            if self.search.sport_name:
                conditions.append(self.current_player['sport_name'].lower().find(self.search.sport_name.lower()) != -1)
            if self.search.hometown:
                conditions.append(self.current_player['hometown'] == self.search.hometown)
            if self.search.birthdate:
                conditions.append(self.current_player['birthdate'] == self.search.birthdate)
            if self.search.cast:
                conditions.append(self.current_player['cast'] == self.search.cast)
            if self.search.position:
                conditions.append(self.current_player['position'] == self.search.position)

            if all(conditions):
                self.result.append(self.current_player)
