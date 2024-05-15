class EnemyData:
    def __init__(self, type, speed, score, lives,description):
        self._type = type
        self._speed = speed
        self._score = score
        self._lives = lives
        self._description=description

    @property
    def type(self):
        return self._type

    @property
    def speed(self):
        return self._speed

    @property
    def score(self):
        return self._score

    @property
    def lives(self):
        return self._lives

    @property
    def description(self):
        return self._description

    @type.setter
    def type(self, value):
        self._type = value

    @speed.setter
    def speed(self, value):
        self._speed = value

    @score.setter
    def score(self, value):
        self._score = value

    @lives.setter
    def lives(self, value):
        self._lives = value

    @lives.setter
    def description(self, value):
        self._description = value

