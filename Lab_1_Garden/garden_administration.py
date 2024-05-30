import garden as gr
from garden import Garden
from garden import Garden_bed
import datetime as dt

# уменьшения кол-во семян, логика отрицательных чисел
class GardenAdministration(gr.Garden):


    def __init__(self):
        Garden.__init__(self)
        self.seads_collection = {}
        self.plant_enciclopedy = {}


    def ad_plant_to_enciclopedy(self, name, prefered_solid, time_between_watering_days, time_before_colecting_week,
                                time_between_taking_care_days, time_between_fertilizing_days):

        try:
            time_between_fertilizing_days = int(time_between_fertilizing_days)
            time_before_colecting_week = int(time_before_colecting_week)
            time_between_watering_days = int(time_between_watering_days)
            time_between_taking_care_days = int(time_between_taking_care_days)
        except:
            return -1

        if self.plant_enciclopedy.get(name) == None:
            self.plant_enciclopedy[name] = PlantInfo(name, prefered_solid, dt.timedelta(days=time_between_watering_days),
                                                      dt.timedelta(weeks=time_before_colecting_week), dt.timedelta(days=time_between_taking_care_days),
                                                      dt.timedelta(days=time_between_fertilizing_days))
            return 0
        else:
            return -1

    def ad_soil_type_to_enciclopedy(self, name, soil):
        if(self.plant_enciclopedy.get(name)!= None):
            self.plant_enciclopedy[name].add_pref_solid(soil)
            return 0
        return -1

    def get_seeds(self):
        return self.seads_collection

    def buy_seeds(self, name, num):
        try:
            num = int(num)
        except:
            return -1
        if(self.seads_collection.get(name) == None):
            self.seads_collection[name] = num
        else:
            self.seads_collection[name] += num
        return 0
    def plant_garden(self, id_, plant_name):
        try:
            id_ = int(id_)
            self.garden_plan[id_]
        except:
            return -1
        if (self.seads_collection.get(plant_name) == None or self.seads_collection[plant_name] < self.garden_plan[id_].get_garden_bed_size()):
            return -3
        if(self.plant_enciclopedy.get(plant_name) == None):
            self.seads_collection[plant_name] -= self.garden_plan[id_].get_garden_bed_size()
            return self.plant_garden_bed(id_, plant_name) + 1
        else:
            if(self.plant_enciclopedy[plant_name].is_prefered(self.garden_plan[id_].get_garden_bed_solid_type()) == -1):
                return 2
            else:
                if(self.seads_collection[plant_name] == None or self.seads_collection[plant_name] < self.garden_plan[id_].get_garden_bed_size()):
                    return -3
                else:
                    self.seads_collection[plant_name] -= self.garden_plan[id_].get_garden_bed_size()
                    return self.plant_garden_bed(id_, plant_name)





class PlantInfo:
    name: str
    prefered_solid = []
    time_between_watering: dt.timedelta
    time_before_colecting: dt.timedelta
    time_between_taking_care: dt.timedelta
    time_between_fertilizing: dt.timedelta

    def __init__(self, name, solid, time_between_watering, time_before_coolection, time_between_taking_care, time_between_fertilizing):
        self.name = name
        self.prefered_solid.append(solid)
        self.time_between_watering = time_between_watering
        self.time_before_colecting = time_before_coolection
        self.time_between_taking_care = time_between_taking_care
        self.time_between_fertilizing = time_between_fertilizing

    def add_pref_solid(self, solid):
        self.prefered_solid.append(solid)

    def is_prefered(self, solid):
        try:
            self.prefered_solid.index(solid)
        except:
            return -1
        return 0
