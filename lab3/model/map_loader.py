import yaml

from .object import Haste
from .object.ghosts import Akabei, Aosuke, Guzuta, Machibuse
from .object.ghosts.ghost_house import GhostHouse


class MapLoader:
    def load(self, filename: str):
        from .object.tracker import Tracker
        from pygame import Vector2
        from .object import Pacman, Crossroad, Road, Wall, Cookie, Powerup
        from model.map import Map
        from .side import Side

        map_ = Map()
        map_.p_tracker = Tracker()

        with open(filename) as file:
            templates = yaml.safe_load(file)

            char_map = templates["object_map"].split('\n')
            rotation_map = templates["rotation_map"].split('\n')

            for i, string in enumerate(char_map):
                for j, char in enumerate(string):
                    position = Vector2(j, i)

                    def register_road(road: Road):
                        for side in Side:
                            for n in map_[(j, i) + side.value]:
                                if isinstance(n, Road):
                                    road.connect(side, n)
                    node = None
                    match char:
                        case '+':
                            node = Crossroad(position)
                            map_.add(Cookie(position.copy()))
                            register_road(node)
                        case '.':
                            node = Road(position)
                            map_.add(Cookie(position.copy()))
                            register_road(node)
                        case 'p':
                            node = Pacman(crossroad := Crossroad(position))
                            map_.pacman_start_position = position.copy()
                            map_.p_tracker.set_pacman(node)
                            map_.add(crossroad)
                            register_road(crossroad)
                        case 'P':
                            node = Powerup(position)
                            road = Road(position.copy())
                            register_road(road)
                            map_.add(road)
                        case '-' | '|':
                            node = Road(position)
                            register_road(node)
                        case 'n':
                            node = Crossroad(position)
                            register_road(node)
                        case 'A':
                            node = Akabei(map_, position)
                            map_.p_tracker.set_akabei(node)
                            road = Crossroad(position.copy())
                            map_.akabei_start_position = position.copy()
                            map_.add(road)
                            register_road(road)
                        case 'M':
                            node = Machibuse(map_, position)
                            road = GhostHouse(position.copy())
                            map_.p_tracker.set_machibuse(node)
                            map_.machibuse_start_position = position.copy()
                            map_.add(road)
                            register_road(road)
                        case 'O':
                            node = Aosuke(map_, position)
                            road = GhostHouse(position.copy())
                            map_.p_tracker.set_aosuke(node)
                            map_.aosuke_start_position = position.copy()
                            map_.add(road)
                            register_road(road)
                        case 'G':
                            node = Guzuta(map_, position)
                            road = GhostHouse(position.copy())
                            map_.p_tracker.set_guzuta(node)
                            map_.guzuta_start_position = position.copy()
                            map_.add(road)
                            register_road(road)
                        case '^':
                            node = GhostHouse(position)
                            register_road(node)
                            pass
                        case 'H':
                            node = Haste(position)
                            road = Road(position.copy())
                            register_road(road)
                            map_.add(road)
                        case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
                            node = Wall(
                                int(char),
                                int(rotation_map[i][j]),
                                position
                            )
                    if node:
                        map_.add(node)
            for n in map_.nodes.copy():
                if isinstance(n, Road) and not isinstance(n, Crossroad):
                    for side in Side:
                        if neighbour := n.adjacent_nodes[side]:
                            (n.adjacent_nodes[side.reverse()]).connect(side, neighbour)
                    map_.remove(n)
        return map_
