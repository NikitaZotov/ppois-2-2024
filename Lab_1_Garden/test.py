import unittest
import garden as gr
import garden_administration as ga
import datetime as dt


class MyTestCase(unittest.TestCase):
    def test_garden_bed(self):
        garden_bed = gr.Garden_bed(2,4, 'soil1', 0)
        self.assertEqual(garden_bed.get_garden_bed_size(), 8)  # add assertion here
        self.assertEqual(garden_bed.get_garden_bed_solid_type(), 'soil1')
        self.assertEqual(garden_bed.get_garden_bed_id(), 0)
        self.assertEqual(garden_bed.get_plant(),'')
        self.assertEqual(garden_bed.fertilizing(), -1)
        self.assertEqual(garden_bed.take_care(), -1)
        self.assertEqual(garden_bed.watering(), -1)
        self.assertEqual(garden_bed.collect(), (0, ''))
        self.assertEqual(garden_bed.planting('cucumber'), 0)
        self.assertEqual(garden_bed.planting('cucumber'), -2)
        self.assertEqual(garden_bed.get_garden_bed_size(), 8)  # add assertion here
        self.assertEqual(garden_bed.get_garden_bed_solid_type(), 'soil1')
        self.assertEqual(garden_bed.get_garden_bed_id(), 0)
        self.assertEqual(garden_bed.get_plant(), 'cucumber')
        self.assertEqual(garden_bed.fertilizing(), 0)
        self.assertEqual(garden_bed.take_care(), 0)
        self.assertEqual(garden_bed.watering(), 0)
        self.assertEqual(garden_bed.collect(), (8, 'cucumber'))
        self.assertEqual(garden_bed.get_plant(), '')


    def test_plant_info(self):
        plant_info = ga.PlantInfo('cucumber', 'soil1', 2,2,2,2)
        soil = ['soil1', 'soil2']
        str = ['soil1']
        self.assertTrue(plant_info.prefered_solid, str)
        plant_info.add_pref_solid('soil2')
        #self.assertEqual(plant_info.prefered_solid, soil)
        self.assertEqual(plant_info.name, 'cucumber')
        self.assertEqual(plant_info.is_prefered('soil3'), -1)
        self.assertEqual(plant_info.is_prefered('soil2'), 0)
        self.assertEqual(plant_info.time_between_fertilizing, 2)
        self.assertEqual(plant_info.time_between_watering, 2)
        self.assertEqual(plant_info.time_before_colecting, 2)
        self.assertEqual(plant_info.time_between_taking_care, 2)

    def test_garden_administration(self):
        garden_adm = ga.GardenAdministration()
        self.assertEqual(garden_adm.add_garden_bed('d', 5, 'soil'), -1)
        self.assertEqual(garden_adm.plant_garden(3, 'cucumber'), -1)
        self.assertEqual(garden_adm.get_free_garden_beds(), [])
        self.assertEqual(garden_adm.collect_garden_bed(3), (-1, ''))
        self.assertEqual(garden_adm.ad_soil_type_to_enciclopedy('cucumber', 'soil'), -1)
        self.assertEqual(garden_adm.fertilizing_lant(3), -1)
        self.assertEqual(garden_adm.get_planted_beds(), [])
        self.assertEqual(garden_adm.get_seeds(), {})
        self.assertEqual(garden_adm.get_solid_type_free_beds('soil'), [])
        self.assertEqual(garden_adm.take_care_of_plant(3), -1)
        self.assertEqual(garden_adm.water_plants(3), -1)
        self.assertEqual(garden_adm.add_garden_bed(2,4,'soil1'), 0)
        self.assertEqual(garden_adm.get_free_garden_beds(), [])
        self.assertEqual(garden_adm.get_planted_beds(), [gr.Garden_bed(2.0,4.0,'soil', 0)])
        self.assertEqual(garden_adm.plant_garden(0, 'cucumber'), -3)
        self.assertEqual(garden_adm.buy_seeds('cucumber', 'l'), -1)
        self.assertEqual(garden_adm.buy_seeds('cucumber', 8), 0)
        self.assertEqual(garden_adm.plant_garden(0, 'cucumber'), 1)
        self.assertEqual(garden_adm.add_garden_bed(2,4,'soil2'), 0)
        self.assertEqual(garden_adm.collect_garden_bed(0), (8, 'cucumber'))
        self.assertEqual(garden_adm.collect_garden_bed(0), (0, ''))
        self.assertEqual(garden_adm.ad_plant_to_enciclopedy('cucumber', 'soil1', 2,2,2,'l'), -1)
        self.assertEqual(garden_adm.ad_plant_to_enciclopedy('cucumber', 'soil1', 2, 2, 2, 2), 0)
        self.assertEqual(garden_adm.buy_seeds('cucumber', 8), 0)
        self.assertEqual(garden_adm.plant_garden(1, 'cucumber'), 2)
        self.assertEqual(garden_adm.ad_soil_type_to_enciclopedy('cucumber', 'soil2'), 0)
        self.assertEqual(garden_adm.plant_garden(1, 'cucumber'), 0)

if __name__ == '__main__':
    unittest.main()
