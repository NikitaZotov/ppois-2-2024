import xml.sax
from model.SearchModel import SearchModel
from model.sax_handlers.ByCriteria import PlayerByCriteriaHandler
from model.sax_handlers.AnyHandler import TeamAnyHandler
from model.sax_handlers.AnyHandler import PlayerAnyHandler
from model.DataModel import DataModel

from model.player import Player
from model.team import Team

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
        doc.documentElement.appendChild(doc.createElement('football_teams'))
        doc.documentElement.appendChild(doc.createElement('players'))
        self._save_doc(doc)

    def _parse_doc(self) -> Document:
        doc = parse(self.path)
        return doc

    def _save_doc(self, doc):
        with open(self.path, 'w') as file:
            file.write(doc.toxml())

    def delete_players(self, search: SearchModel) -> int:
        doc: Document = parse(self.path)
        deleted_count: int = 0
        players = doc.getElementsByTagName('player')
        players_to_delete = []
        for player in players:
            conditions = []
            if search.name:
                conditions.append(player.getAttribute('name').lower().find(search.name.lower()) != -1)
            if search.sport_name:
                conditions.append(player.getAttribute('sport_name').lower().find(search.sport_name.lower()) != -1)
            if search.birthdate:
                conditions.append(conditions.append(player.getAttribute('birthdate') == search.birthdate))

            if all(conditions):
                sports_element = doc.getElementsByTagName('football_teams')[0]
                sport_elements = sports_element.getElementsByTagName('football_team')
                for sport_element in sport_elements:
                    if sport_element.attributes['name'].value == player.getAttribute('sport_name'):
                        current_players_number = int(sport_element.attributes['players_number'].value)
                        sport_element.attributes['players_number'].value = str(current_players_number - 1)
                        break
                players_to_delete.append(player)
                deleted_count += 1
        for player in players_to_delete:
            parent = player.parentNode
            parent.removeChild(player)
        self._save_doc(doc)
        return deleted_count

    def search_players(self, search: SearchModel) -> list[Player]:
        handler = PlayerByCriteriaHandler(search)
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(self.path)
        dict_players: list[dict] = handler.result
        players: list[Player] = []
        for dict_player in dict_players:
            players.append(Player(dict_player['sport_name'], dict_player['name'],
                                  dict_player['cast'], dict_player['position'],
                                  dict_player['hometown'], dict_player['birthdate'], uuid.UUID(dict_player['id'])))
        return players

    def get_players(self, search_criteria: SearchModel | None = None) -> list[Player]:
        handler = PlayerAnyHandler()

        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(self.path)
        dict_players: list[dict] = handler.result
        players: list[Player] = []

        for dict_player in dict_players:
            id = uuid.UUID(hex=dict_player['id'])
            players.append(Player(dict_player['name'], dict_player['sport_name'],
                                  dict_player['cast'], dict_player['position'],
                                  dict_player['hometown'], dict_player['birthday'], id))
        return players

    def player_exists(self, name, sport_name, cast, position, hometown, birthday) -> bool:
        players = self.get_players()

        for player in players:
            if (player.get_sport_name() == sport_name and player.get_name() == name
                    and player.get_cast() == cast and player.get_position() == position
                    and player.get_hometown() == hometown and player.get_birthday() == birthday):
                return True
        return False

    def sport_exists(self, name) -> bool:
        sports = self.get_sports()

        for team in sports:
            if team.get_name() == name:
                return True
        return False

    def add_player(self, sport_name: str, name: str, cast: str, position: str, hometown: str, birthday: str):
        doc = self._parse_doc()

        player_element = doc.createElement('player')
        player_element.attributes['sport_name'] = sport_name
        player_element.attributes['name'] = name
        player_element.attributes['cast'] = cast
        player_element.attributes['position'] = position
        player_element.attributes['hometown'] = hometown
        player_element.attributes['birthday'] = birthday
        player_element.attributes['id'] = uuid.uuid4().__str__()

        sports_element = doc.getElementsByTagName('football_teams')[0]
        sport_elements = sports_element.getElementsByTagName('football_team')
        for sport_element in sport_elements:
            if sport_element.attributes['name'].value == sport_name:
                current_players_number = int(sport_element.attributes['players_number'].value)
                sport_element.attributes['players_number'].value = str(current_players_number + 1)
                break

        items_element = doc.getElementsByTagName('players')[0]
        items_element.appendChild(player_element)

        self._save_doc(doc)

    def add_sport(self, name: str, players_number: str) -> None:
        document = self._parse_doc()

        doc_element = document.createElement('football_team')
        doc_element.attributes['name'] = name
        doc_element.attributes['players_number'] = str(players_number)
        doc_element.attributes['id'] = uuid.uuid4().__str__()

        items_element = document.getElementsByTagName('football_teams')[0]
        items_element.appendChild(doc_element)

        self._save_doc(document)

    def get_sports(self) -> list[Team]:
        handler = TeamAnyHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(self.path)
        dict_sports: list[dict] = handler.result
        sports: list[Team] = []

        for dict_sport in dict_sports:
            id = uuid.UUID(hex=dict_sport['id'])
            sports.append(Team(dict_sport['name'], dict_sport['players_number'], id))
        return sports

    def get_sport_by_name(self, name) -> Team | None:
        handler = TeamAnyHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(self.path)
        dict_sports: list[dict] = handler.result

        for dict_sport in dict_sports:
            if 'name' in dict_sport and dict_sport['name'] == name:
                id = uuid.UUID(hex=dict_sport['id'])
                return Team(dict_sport['name'], dict_sport['players_number'], id)
        return None

    def count_players_amount(self) -> int:
        players = self.get_players()
        return len(players)

    def count_sports_amount(self) -> int:
        sports = self.get_sports()
        return len(sports)
