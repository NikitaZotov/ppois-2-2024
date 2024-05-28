from unittest import TestCase

from atmosphere import Atmosphere


class TestAtmosphere(TestCase):
    def setUp(self):
        self.atmosphere: Atmosphere = Atmosphere()

    def test_set_atmosphere(self):
        self.atmosphere.set_atmosphere(15.0)
        self.assertEqual(self.atmosphere.atmosphere, 15.0)

    def test_switch_music(self):
        self.assertEqual(self.atmosphere.music, False)
        self.atmosphere.switch_music()
        self.assertEqual(self.atmosphere.music, True)
        self.atmosphere.switch_music()
        self.assertEqual(self.atmosphere.music,False)

    def test_add_plants(self):
        self.atmosphere.add_plants()
        self.assertEqual(self.atmosphere.plants, 1)

    def test_add_decorations(self):
        self.atmosphere.add_decorations()
        self.assertEqual(self.atmosphere.decorations, 1)
