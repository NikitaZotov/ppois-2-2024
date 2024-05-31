from .node import Node
from model.side import Side
from weakref import WeakValueDictionary


class Road(Node):
    from pygame import Vector2

    name = "Road"

    def __init__(
            self,
            position: Vector2 = Vector2()
    ):
        super().__init__(position)
        self._adjacent_nodes: WeakValueDictionary[Side, Node | None] = dict.fromkeys(Side, None)
        self._adjacent_nodes[Side.stop] = self

    @property
    def adjacent_nodes(self):
        return self._adjacent_nodes.copy()

    def remove_neighbor(self, side: Side):
        self._adjacent_nodes[side] = None

    def connect(self, side: Side, node):
        if (node.position - self.position).cross(side.value) != 0:
            raise ValueError("Nodes not on the same line")
        self._adjacent_nodes[side] = node
        node._adjacent_nodes[side.reverse()] = self

