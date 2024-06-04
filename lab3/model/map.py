from model.object.node import Node
from model.object.game_object import GameObject
from model.object import Cookie


class Map:
    def __init__(
            self,
            width: int = 28,
            height: int = 36,
            on_adding=None
    ):
        self.nodes: list[Node] = []
        self.cookies_count = 0
        self.eaten_cookies_count = 0
        self.width = width
        self.height = height
        self.on_adding = on_adding
        self.p_tracker = None
        self.pacman_start_position = None
        self.akabei_start_position = None
        self.machibuse_start_position = None
        self.aosuke_start_position = None
        self.guzuta_start_position = None

    def set_game_object_handler(self, game_object: GameObject):
        game_object.on_move = self.__get_on_moving()

    def add(self, node: Node):
        self.nodes.append(node)
        if isinstance(node, GameObject):
            self.set_game_object_handler(node)
        if isinstance(node, Cookie):
            self.cookies_count += 1
        if self.on_adding:
            self.on_adding(node)

    def remove(self, node: Node):
        from event import DeletingEvent
        from event.event_manager import ev_manager

        self.nodes.remove(node)
        if isinstance(node, Cookie):
            self.eaten_cookies_count += 1

        ev_manager.notify(DeletingEvent(node))

    def __get_on_moving(self):
        width = self.width
        height = self.height
        nodes = self.nodes

        def on_moving(moving: GameObject):
            nonlocal width, height, nodes

            if moving.position[0] >= width:
                moving._position[0] = 0

            if moving.position[0] < 0:
                moving._position[0] = width - 1

            if moving.position[1] >= height:
                moving._position[1] = 0

            if moving.position[1] < 0:
                moving._position[1] = height - 1

            for node in [x for x in nodes if x._position == moving._position]:
                if node is not moving:
                    moving.collision(node)

        return on_moving

    def __contains__(self, item):
        return self.nodes in item

    def __getitem__(self, item: (int, int)):
        item = (item[0] % self.width, item[1] % self.height)
        return [x for x in self.nodes if x._position == item]

    def __iter__(self):
        return iter(self.nodes)
