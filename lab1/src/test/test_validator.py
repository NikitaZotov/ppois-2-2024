import unittest

from src.main.model.entity.building import Building
from src.main.model.entity.cadastral_number import CadastralNumber
from src.main.model.entity.enum.region import Region
from src.main.model.entity.land_plot import LandPlot
from src.main.model.service.cadastral_agency import CadastralAgency
from src.main.validator.building_validator import BuildingValidator
from src.main.validator.land_plot_validator import LandPlotValidator
from src.main.validator.owner_validator import OwnerValidator


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.owner_validator = OwnerValidator()
        self.building_validator = BuildingValidator()
        self.land_validator = LandPlotValidator()
        self.service = CadastralAgency()

    def tearDown(self):
        self.service.documents.clear()
        self.service.registered_buildings.clear()
        self.service.registered_land_plots.clear()
        self.service.registered_owners.clear()
        self.service.unregistered_land_plots.clear()

    # OWNER VALIDATOR TESTS

    def test_validate_passport_id_success(self):
        valid_pass_id = "0000000A000AA0"
        self.assertEqual(valid_pass_id, self.owner_validator.validate_passport_id(valid_pass_id))

    def test_validate_passport_id_value_error_invalid(self):
        invalid_pass_id = "0000000AA00AA0"
        self.assertRaises(ValueError, self.owner_validator.validate_passport_id, invalid_pass_id)

    def test_validate_name_or_surname_success(self):
        valid_name_or_surname = "Test"
        self.assertEqual(valid_name_or_surname, self.owner_validator.validate_name_or_surname(valid_name_or_surname))

    def test_validate_name_or_surname_value_error_invalid(self):
        invalid_name_or_surname = "test132"
        self.assertRaises(ValueError, self.owner_validator.validate_name_or_surname, invalid_name_or_surname)

    # BUILDING VALIDATOR TESTS

    def test_validate_building_name_success(self):
        valid_building_name = "Test"
        self.assertEqual(valid_building_name, self.building_validator.validate_building_name(valid_building_name))

    def test_validate_building_name_value_error_already_exists(self):
        valid_building_name = "Test"
        self.service.registered_buildings.append(Building(valid_building_name))
        self.assertRaises(ValueError, self.building_validator.validate_building_name, valid_building_name)

    def test_validate_area_in_sq_m_success(self):
        valid_land = LandPlot((1, 1), 0.01)
        self.assertEqual(50.5, self.building_validator.validate_area_in_square_meters("50.5", valid_land))

    def test_validate_area_in_sq_m_value_error_invalid(self):
        valid_land = LandPlot((1, 1), 0.01)
        self.assertRaises(ValueError, self.building_validator.validate_area_in_square_meters, "asdasds", valid_land)
        self.assertRaises(ValueError, self.building_validator.validate_area_in_square_meters, "-51.5", valid_land)

    def test_validate_area_in_sq_m_value_error_not_enough_land(self):
        valid_land = LandPlot((1, 1), 0.01)
        self.assertRaises(ValueError, self.building_validator.validate_area_in_square_meters, "60000", valid_land)

    def test_validate_floors_success(self):
        self.assertEqual(5, self.building_validator.validate_floors("5"))

    def test_validate_floors_value_error_invalid(self):
        self.assertRaises(ValueError, self.building_validator.validate_floors, "asdasd")
        self.assertRaises(ValueError, self.building_validator.validate_floors, "-5")

    # LAND PLOT VALIDATOR TEST

    def test_validate_coordinates_success(self):
        valid_coordinates = (1, 1)
        self.assertEqual(valid_coordinates, self.land_validator.validate_coordinates("1, 1"))

    def test_validate_coordinates_value_error_invalid(self):
        self.assertRaises(ValueError, self.land_validator.validate_coordinates, "asdasd")
        self.assertRaises(ValueError, self.land_validator.validate_coordinates, "15")
        self.assertRaises(ValueError, self.land_validator.validate_coordinates, "15 79")

    def test_validate_area_success(self):
        valid_area = 15.5
        self.assertEqual(valid_area, self.land_validator.validate_area("15.5"))

    def test_validate_area_value_error_invalid(self):
        self.assertRaises(ValueError, self.land_validator.validate_area, "asdasd")
        self.assertRaises(ValueError, self.land_validator.validate_area, "-15.6")

    def test_validate_cadastral_number_success(self):
        valid_cad_num = CadastralNumber(Region.DEFAULT, 156)
        valid_cad_num.cadastral_block_number = 0
        self.assertEqual(str(valid_cad_num), self.land_validator.validate_cadastral_number(valid_cad_num, 0))

    def test_validate_cadastral_number_value_error_invalid(self):
        valid_cad_num = CadastralNumber(Region.DEFAULT, 156)
        self.assertRaises(ValueError, self.land_validator.validate_cadastral_number, valid_cad_num, 15)

    def test_validate_cadastral_number_value_error_already_exists(self):
        valid_cad_num = CadastralNumber(Region.DEFAULT, 156)
        valid_cad_num.cadastral_block_number = 0
        valid_land_plot = LandPlot((1, 1), 0.01)
        valid_land_plot.cadastral_number = valid_cad_num
        self.service.registered_land_plots.append(valid_land_plot)
        self.assertRaises(ValueError, self.land_validator.validate_cadastral_number, valid_cad_num, 0)


if __name__ == '__main__':
    unittest.main()
