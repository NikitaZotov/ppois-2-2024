from datetime import datetime as dt

import xml.sax as sax
from xml.sax.xmlreader import AttributesImpl

from controller.filter import Filter
from model.winner import Winner
from model.tournament import Tournament

class TournamentByFilterHandler(sax.ContentHandler):

    def __init__(self, filter: Filter):

        self.result: list[Tournament] = []
        self.tournament = None
        self.filter = filter
        self.skip = (filter.page_number - 1) * filter.page_size
        
    def startElement(self, name: str, attrs: AttributesImpl) -> None:
        if name == 'tournament':
            winner = Winner(attrs.get('winnername'), attrs.get('winnersurname'), attrs.get('winnermiddlename'))
            self.tournament = Tournament(attrs.get('title'), dt.strptime(attrs.get('date'), "%d.%m.%Y"), 
                                         attrs.get('sport'), winner, int(attrs.get('prize')))
            
    def endElement(self, name):

        if name == 'tournament':
            if self.filter.title and self.filter.title != self.tournament.title: return
            if self.filter.date and self.filter.date != self.tournament.date: return
            if self.filter.sport and self.filter.sport != self.tournament.sport: return 
            if self.filter.winner_name and self.filter.winner_name != self.tournament.winner.name: return
            if self.filter.winner_surname and self.filter.winner_surname != self.tournament.winner.surname: return   
            if self.filter.winner_middlename and self.filter.winner_middlename != self.tournament.winner.middlename: return 
            if self.filter.prize_range[0] and self.filter.prize_range[0] > self.tournament.prize: return
            if self.filter.prize_range[1] and self.filter.prize_range[1] < self.tournament.prize: return
            if self.filter.winner_prize_range[0] and self.filter.winner_prize_range[0] > self.tournament.winner_prize: return
            if self.filter.winner_prize_range[1] and self.filter.winner_prize_range[1] < self.tournament.winner_prize: return

            if self.skip: 
                self.skip -= 1
                return

            self.result.append(self.tournament)

    
            
            
                
