from datetime import date

import xml.sax as sax
import xml.dom.minidom as mdom

from tkinter.messagebox import showinfo

from controller.handlers import SportHandler
from controller.filter import Filter
from controller.byfilterhandlers import TournamentByFilterHandler
from model.winner import Winner
from model.tournament import Tournament

class XMLParser():

    def __init__(self, path: str):
        self.path = path

    def init_xml(self):

        doc = mdom.getDOMImplementation().createDocument(None, 'tkinter', None)

        doc.documentElement.appendChild(doc.createElement('tournaments'))

        self.save_xml(doc)

    def parse_xml(self) -> mdom.Document:

        doc = mdom.parse(self.path)
        return doc
    
    def save_xml(self, doc: mdom.Document):
        with open(self.path, 'w') as file:
            file.write(doc.toxml())

    def get_sports(self) -> set[str]:

        handler = SportHandler()
        sax.parse(self.path, handler)

        return handler.result

    def filter_tournaments(self, filter: Filter) -> list[Tournament]:
            
        handler_by_filter = TournamentByFilterHandler(filter)
        sax.parse(self.path, handler_by_filter)

        return handler_by_filter.result
    
    def add_tournament(self, title: str, date: date, sport: str, winner: Winner,  
                       prize: int):
        
        doc = self.parse_xml()

        tournament_element = doc.createElement('tournament')
        tournament_element.attributes['title'] = title
        tournament_element.attributes['date'] = f"{date.day}.{date.month}.{date.year}"
        tournament_element.attributes['sport'] = sport
        tournament_element.attributes['winnername'] = winner.name
        tournament_element.attributes['winnersurname'] = winner.surname
        tournament_element.attributes['winnermiddlename'] = winner.middlename
        tournament_element.attributes['prize'] = str(prize)
        tournament_element.attributes['winnerprize'] = str(int(0.6 * prize))

        tournaments_element = doc.getElementsByTagName('tournaments')[0]
        tournaments_element.appendChild(tournament_element)

        self.save_xml(doc)

    def delete_tournaments(self, filter: Filter):
        
        doc = self.parse_xml()

        handler_by_filter = TournamentByFilterHandler(filter)
        sax.parse(self.path, handler_by_filter)

        titles_tournaments_to_delete = list(map(lambda a: a.title, handler_by_filter.result))
        tournaments = doc.getElementsByTagName('tournament')
        
        for tournament in tournaments:
            if tournament.getAttribute('title') in titles_tournaments_to_delete:
                parent = tournament.parentNode
                parent.removeChild(tournament)
                self.save_xml(doc)
                

        showinfo(title="Deleted tournaments", message=f"Amount of deleted tournaments is: {len(handler_by_filter.result)}")
        
        


    



        




