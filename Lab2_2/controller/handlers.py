from datetime import date

import xml.sax as sax
from xml.sax.xmlreader import AttributesImpl

from model.winner import Winner
from model.tournament import Tournament

class SportHandler(sax.ContentHandler):

    def __init__(self):
        self.result: set[str] = set()
        self.sport = None

    def startElement(self, name: str, attrs: AttributesImpl):
        if name == 'tournament':
            self.sport = attrs.get('sport').capitalize()
        
    def endElement(self, name: str):
        if name == 'tournament': self.result.add(self.sport)
            
class TournamentHandler(sax.ContentHandler):

    def __init__(self):

        self.result: list[Tournament] = []
        self.tournament = None

    def startElement(self, name: str, attrs: AttributesImpl):
        if name == 'tournament':
            self.tournament = Tournament(attrs.get('title'), attrs.get('date'), attrs.get('sport'),
                                         Winner(attrs.get('winnername'), attrs.get('winnersurname'), attrs.get('winnermiddlename')),
                                         attrs.get('prize'))
        
    def endElement(self, name: str):
        if name == 'tournament': self.result.append(self.tournament)
        