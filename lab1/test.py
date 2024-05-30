from unittest import TestCase, main
from space_object import SpaceObject
from star import Star
from cometa import Cometa
from planet import Planet
from satellite import Satellite
from asteroid import Asteroid
from spacecraft import Spacecraft
from star_system import StarSystem


class SpacecraftTest(TestCase):
    def SetUp(self):
        self.planet = Planet('sunsara', 4800, 78129, 123, 31, 401, 4800)
        self.error_planet = Planet('sunsara', 4800, 78129, 124, 32, 1, 4800)
        self.spacecraft = Spacecraft("death", self.planet)

    def test_speed_exploration(self):
        self.SetUp()
        self.assertEqual(self.spacecraft.speed_exploration(self.planet), 4800)

    def test_modelling_orbit(self):
        self.SetUp()
        self.assertEqual(self.spacecraft.modeling_orbit(self.planet, self.error_planet), 400.00249999218755)
        with self.assertRaises(Exception) as e:
            self.spacecraft.modeling_orbit(self.planet, self.planet)
        self.assertEqual("It's one object", e.exception.args[0])



class StarTest(TestCase):
    def SetUp(self):
        self.star = Star("sun", 'carlic', 480.20, 60**10, 0, 0, 0, 40**4)

    def test_star(self):
        self.SetUp()
        #self.star = Star("sun", 'carlic', 480.20, 60 ** 10, 0, 0, 0, 40 ** 4)
        self.assertEqual(self.star.get_name(), "sun")
        self.assertEqual(self.star.get_x(), 0)
        self.assertEqual(self.star.get_y(), 0)
        self.assertEqual(self.star.get_z(), 0)
        self.assertEqual(self.star.get_speed(), 480.20)
        self.assertEqual(self.star.get_mass(), 60**10)
        self.assertEqual(self.star.get_radius(), 40**4)
        self.assertEqual(self.star.get_atmosphere(), None)
        self.assertEqual(self.star.get_type(), "carlic")
        self.assertEqual(self.star.get_gravity(), 6.1577773425e-06)


class StarSystemTest(TestCase):
    def SetUp(self):
        self.star = Star("sun", 'carlic', 480.20, 60**10, 0, 0, 0, 40**4)
        self.planet = Planet('sunsara', 4800, 78129, 123, 31, 401, 4800)
        self.error_planet = Planet('sara', 4800, 78129, 124, 32, 1, 4800)
        self.spacecraft = Spacecraft("death", self.planet)
        self.star_system = StarSystem(star=self.star, planets=[self.planet])

    def test_add(self):
        self.SetUp()
        self.star_system.add_planet(self.error_planet)
        self.assertEqual(self.star_system.search_planet('sara'), self.error_planet)
        self.star_system.add_spacecraft(self.spacecraft)
        self.assertEqual(self.star_system.get_star(), self.star)
        self.assertEqual(self.star_system.search_spacecraft('death'), self.spacecraft)
        self.assertEqual(self.star_system.search_space_object("sun"), self.star)

    def test_error(self):
        self.SetUp()
        with self.assertRaises(ValueError) as context:
            self.star_system.search_planet("sdasd")
        self.assertEqual(context.exception.args[0], 'not found')
        with self.assertRaises(ValueError) as context:
            self.star_system.search_spacecraft("sadadsdasf")
        self.assertEqual(context.exception.args[0], 'not found')
        with self.assertRaises(ValueError) as context:
            self.star_system.search_space_object("sal")
        self.assertEqual(context.exception.args[0], 'Not found')


class CometaTest(TestCase):
    def SetUp(self):
        self.star = Star("sun", 'carlic', 480.20, 60 ** 10, 0, 0, 0, 40 ** 4)
        self.cometa = Cometa('sad', 456, 123413, 3, 6, 7, 231, star=self.star)

    def test_get(self):
        self.SetUp()
        self.assertEqual(self.cometa.get_star_orbit(), self.star)

if __name__ == '__main__':
    main()