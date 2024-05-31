import unittest
from datetime import date, timedelta

from src.main.model.entity.building import Building
from src.main.model.entity.land_plot import LandPlot
from src.main.model.entity.owner import Owner
from src.main.model.entity.registration_document import BuildingRegistrationDocument, LandRegistrationDocument
from src.main.model.service.cadastral_agency import CadastralAgency


class ServiceTest(unittest.TestCase):

    def setUp(self):
        self.service = CadastralAgency()
        self.valid_land = LandPlot((1.65, 1.5), 0.01, "asd")
        self.valid_owner = Owner("0000000A000AA0", "Test", "Testor")
        self.valid_building = Building("test", self.valid_land)
        self.valid_building.area_in_square_meters = 50
        self.TEST_FILE_PATH = "resource/test_db"

    def tearDown(self):
        self.service.documents.clear()
        self.service.registered_buildings.clear()
        self.service.registered_land_plots.clear()
        self.service.registered_owners.clear()
        self.service.unregistered_land_plots.clear()

    def test_register_land_success(self):
        self.service.register_land_plot(self.valid_land, self.valid_owner)
        expected_document = LandRegistrationDocument(self.valid_owner, date.today(), self.valid_land)
        self.assertIn(self.valid_land, self.service.registered_land_plots)
        self.assertIn(expected_document, self.service.documents)
        self.assertNotIn(self.valid_land, self.service.unregistered_land_plots)

    def test_unregister_land_plot_success(self):
        valid_document = LandRegistrationDocument(self.valid_owner, date.today(), self.valid_land)
        self.service.documents.append(valid_document)
        self.service.registered_land_plots.append(self.valid_land)
        self.service.unregister_land_plot(valid_document)
        self.assertNotIn(valid_document, self.service.documents)
        self.assertIn(self.valid_land, self.service.unregistered_land_plots)

    def test_register_building_success(self):
        self.service.register_building(self.valid_building, self.valid_owner)
        expected_document = BuildingRegistrationDocument(self.valid_owner, date.today(), self.valid_building)
        self.assertIn(self.valid_building, self.service.registered_buildings)
        self.assertIn(expected_document, self.service.documents)

    def test_unregister_building_success(self):
        valid_document = BuildingRegistrationDocument(self.valid_owner, date.today(), self.valid_building)
        self.service.documents.append(valid_document)
        self.service.registered_buildings.append(self.valid_building)
        self.service.unregister_building(valid_document)
        self.assertNotIn(valid_document, self.service.documents)
        self.assertNotIn(self.valid_building, self.service.registered_buildings)

    def test_register_owner_success(self):
        self.service.register_owner(self.valid_owner)
        self.assertIn(self.valid_owner, self.service.registered_owners)

    def test_get_land_plot_left_area_success(self):
        self.service.register_land_plot(self.valid_land, self.valid_owner)
        self.service.register_building(self.valid_building, self.valid_owner)
        expected_left_area = 50.0
        self.assertEqual(expected_left_area, self.service.get_land_plot_left_area(self.valid_land))

    def test_save_and_load_success(self):
        self.service.registered_land_plots.append(self.valid_land)
        self.service.save_all(self.TEST_FILE_PATH)
        self.service.registered_land_plots.clear()
        self.service.load(self.TEST_FILE_PATH)
        self.assertIn(self.valid_land, self.service.registered_land_plots)

    def test_get_owner_documents_success(self):
        self.service.register_land_plot(self.valid_land, self.valid_owner)
        self.service.register_building(self.valid_building, self.valid_owner)
        self.assertEqual(2, len(self.service.get_owner_documents(self.valid_owner)))


if __name__ == '__main__':
    unittest.main()
