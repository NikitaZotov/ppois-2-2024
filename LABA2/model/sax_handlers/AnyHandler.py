import uuid
import xml.sax


class AthleteAnyHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.result = []
        self.current_athlete = {}
        self.current_tag = None

    def startElement(self, name, attrs):
        if name == 'athlete':
            athlete_id = attrs.get('id', str(uuid.uuid4()))
            self.current_athlete = {
                'name': attrs.get('name'),
                'sport_name': attrs.get('sport_name'),
                'cast': attrs.get('cast'),
                'position': attrs.get('position'),
                'title': attrs.get('title'),
                'rank': attrs.get('rank'),
                'id': athlete_id,
            }
        else:
            self.current_tag = name

    def characters(self, content):
        if self.current_tag is not None and self.current_athlete is not None:
            self.current_athlete[self.current_tag] = content

    def endElement(self, name):
        if name == 'athlete' and self.current_athlete is not None:
            self.result.append(self.current_athlete)
            self.current_athlete = None
        self.current_tag = None


class SportAnyHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.result = []  # List to store results
        self.current_sport = {}
        self.current_tag = None
        self.inside_sports = False  # Flag to indicate if inside <sports> tag

    def startElement(self, name, attrs):
        if name == 'sports':
            self.inside_sports = True
        elif name == 'sport' and self.inside_sports:
            sport_id = attrs.get('id', str(uuid.uuid4()))  # Generate UUID if 'id' is not provided  # Debugging line
            self.current_sport = {
                'name': attrs.get('name'),
                'athletes_number': attrs.get('athletes_number'),
                'id': sport_id,
            }
        else:
            self.current_tag = name

    def characters(self, content):
        if self.current_tag is not None and self.current_sport:
            self.current_sport[self.current_tag] = content

    def endElement(self, name):
        if name == 'sport' and self.inside_sports:
            # Check if 'id' is missing or empty, generate UUID in that case
            if 'id' not in self.current_sport or not self.current_sport['id']:
                self.current_sport['id'] = str(uuid.uuid4())  # Debugging line
            self.result.append(self.current_sport)
            self.current_sport = {}
        elif name == 'sports':
            self.inside_sports = False
        self.current_tag = None