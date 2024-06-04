import uuid
import xml.sax


class PlayerAnyHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.result = []
        self.current_player = {}
        self.current_tag = None

    def startElement(self, name, attrs):
        if name == 'player':
            player_id = attrs.get('id', str(uuid.uuid4()))
            self.current_player = {
                'sport_name': attrs.get('sport_name'),
                'name': attrs.get('name'),
                'cast': attrs.get('cast'),
                'position': attrs.get('position'),
                'hometown': attrs.get('hometown'),
                'birthday': attrs.get('birthday'),
                'id': player_id,
            }
        else:
            self.current_tag = name

    def characters(self, content):
        if self.current_tag is not None and self.current_player is not None:
            self.current_player[self.current_tag] = content

    def endElement(self, name):
        if name == 'player' and self.current_player is not None:
            self.result.append(self.current_player)
            self.current_player = None
        self.current_tag = None


class TeamAnyHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.result = []  # List to store results
        self.current_sport = {}
        self.current_tag = None
        self.inside_sports = False  # Flag to indicate if inside <sports> tag

    def startElement(self, name, attrs):
        if name == 'football_teams':
            self.inside_sports = True
        elif name == 'football_team' and self.inside_sports:
            sport_id = attrs.get('id', str(uuid.uuid4()))  # Generate UUID if 'id' is not provided  # Debugging line
            self.current_sport = {
                'name': attrs.get('name'),
                'players_number': attrs.get('players_number'),
                'id': sport_id,
            }
        else:
            self.current_tag = name

    def characters(self, content):
        if self.current_tag is not None and self.current_sport:
            self.current_sport[self.current_tag] = content

    def endElement(self, name):
        if name == 'football_team' and self.inside_sports:
            # Check if 'id' is missing or empty, generate UUID in that case
            if 'id' not in self.current_sport or not self.current_sport['id']:
                self.current_sport['id'] = str(uuid.uuid4())  # Debugging line
            self.result.append(self.current_sport)
            self.current_sport = {}
        elif name == 'football_teams':
            self.inside_sports = False
        self.current_tag = None