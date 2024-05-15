class WaveData:
    def __init__(self, name=None, duration=None, enemy_dict=None, obstacle=None, background_color=None, description=None):
        self._name = name
        self._duration = duration
        self._enemy_dict = enemy_dict if enemy_dict is not None else {}
        self._obstacle = obstacle
        self._background_color = background_color
        self._description=description

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    @property
    def enemy_dict(self):
        return self._enemy_dict

    def add_enemy(self, enemy_name, enemy_data):
        self._enemy_dict[enemy_name] = enemy_data

    @property
    def obstacle(self):
        return self._obstacle

    @property
    def description(self):
        return self._description

    @obstacle.setter
    def obstacle(self, value):
        self._obstacle = value

    @property
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self, value):
        self._background_color = value
