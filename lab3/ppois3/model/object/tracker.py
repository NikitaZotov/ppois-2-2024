from weakref import ref
from .pacman import Pacman
from .ghosts import Akabei, Guzuta, Machibuse, Aosuke


class Tracker:
    def __init__(self):
        self._pacman: ref[Pacman] = None
        self._akabei: ref[Akabei] = None
        self._guzuta: ref[Guzuta] = None
        self._machibuse: ref[Machibuse] = None
        self._aosuke: ref[Aosuke] = None

    @property
    def pacman(self):
        return self._pacman() if self._pacman else None

    @property
    def akabei(self):
        return self._akabei() if self._akabei else None

    @property
    def guzuta(self):
        return self._guzuta() if self._guzuta else None

    @property
    def machibuse(self):
        return self._machibuse() if self._machibuse else None

    @property
    def aosuke(self):
        return self._aosuke() if self._aosuke else None

    @property
    def pacman_position(self):
        if pacman := self.pacman:
            return pacman.position

    @property
    def akabei_position(self):
        if akabei := self.akabei:
            return akabei.position

    def set_pacman(self, pacman: Pacman):
        self._pacman = ref(pacman)

    def set_akabei(self, akabei: Akabei):
        self._akabei = ref(akabei)

    def set_guzuta(self, guzuta: Guzuta):
        self._guzuta = ref(guzuta)

    def set_machibuse(self, machibuse: Machibuse):
        self._machibuse = ref(machibuse)

    def set_aosuke(self, aosuke: Aosuke):
        self._aosuke = ref(aosuke)
