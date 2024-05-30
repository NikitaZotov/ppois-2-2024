import datetime as dt
import markdown

class Garden:

    """"This class creates model of garden as place"""

    def __init__(self):
        self.garden_plan = []
        self.solid_type = []

    """"Function for adding garden bed"""

    def add_garden_bed(self, length, width, soil_typ):
        """"Function for adding garden bed"""
        id_ = len(self.garden_plan)
        try:
            length = abs(int(length))
            width = abs(int(width))
        except ValueError:
            return -1
        #добавить если элемента нет в массиве видов почв добавить
        self.garden_plan.append(Garden_bed(length, width, soil_typ, id_))
        return 0



    def water_plants(self, id_):
        """"Function for watering plants"""
        try:
            id_ = int(id_)
            self.garden_plan[id_]
        except:
            return -1
        return self.garden_plan[id_].watering(self)



    def take_care_of_plant(self, id_):
        """"Function for taking care of plants"""
        try:
            id_ = int(id_)
            self.garden_plan[id_]
        except:
            return -1
        return  self.garden_plan[id_].take_care(self)



    def fertilizing_lant(self, id_):
        """"Function for fertilizing plants"""
        try:
            id_ = int(id_)
            self.garden_plan[id_]
        except:
            return -1
        return self.garden_plan[id_].fertilizing(self)



    def get_free_garden_beds(self):
        """"This function returns free beds"""
        free_garden_beds_list = []
        for bed in self.garden_plan:
            if bed.get_plant == '':
                free_garden_beds_list.append(bed)
        return free_garden_beds_list



    def get_solid_type_free_beds(self, solid):
        """"This function returns free beds"""
        try:
            self.solid_type.index(solid)
        except:
            return []
        solid_type_free_beds = []
        for bed in self.garden_plan:
            if bed.get_garden_bed_solid_type(self) == solid:
                solid_type_free_beds.append(bed)
        return solid_type_free_beds

    def get_planted_beds(self):
        """"This function returns planted beds"""
        planted_beds = []
        for bed in self.garden_plan:
            if bed.get_plant != '':
                planted_beds.append(bed)
        return planted_beds

    def plant_garden_bed(self, id_, plant_name):
        """"This function plants"""
        try:
            id_ = int(id_)
            self.garden_plan[id_]
        except:
            return -3

        return self.garden_plan[id_].planting(plant_name)

    def collect_garden_bed(self, id_):
        """"This function collects plants"""
        try:
            id_ = int(id_)
            self.garden_plan[id_]
        except:
            return -1, ''

        return self.garden_plan[id_].collect()

class Garden_bed:
    """"Garden bed class"""
    garden_bed_length: int
    soil_type = ''
    id_ = ''
    garden_bed_width: int
    time_of_watering: dt.datetime
    time_of_fertilizing: dt.datetime
    time_of_planting: dt.datetime
    time_of_taking_care: dt.datetime
    is_planted = False
    plant_name = ''

    def __eq__(self, other):
        if(self.id_ == other.id_):
            return True
        return False



    def __init__(self, length, width, soil_type, id_):
        """"Inicializing garden bed size"""
        self.garden_bed_length = length
        self.garden_bed_width = width
        self.soil_type = soil_type
        self.id_ = id_




    def planting(self, plant_name):
        """"Function for planting garden bed"""
        if self.is_planted == False:
            self.plant_name = plant_name
            self.is_planted = True
            self.time_of_planting = dt.datetime.now()
            self.time_of_watering = dt.datetime.now()
            self.time_of_fertilizing = dt.datetime.now()
            self.time_of_taking_care = dt.datetime.now()
            return 0
        else:
            return -2




    def watering(self):
        """"Function for watering garden bed"""
        if(self.is_planted):
            self.time_of_watering = dt.datetime.now()
            return 0
        return -1



    def fertilizing(self):
        """"Function for fertilizing garden bed"""
        if(self.is_planted):
            self.time_of_fertilizing = dt.datetime.now()
            return 0
        return -1



    def take_care(self):
        """"Function for taking care garden bed"""
        if(self.is_planted):
            self.time_of_taking_care = dt.datetime.now()
            return 0
        return -1



    def collect(self):
        """"Function for collection plants"""
        if self.is_planted == True:
           self.is_planted = False
           return self.garden_bed_width*self.garden_bed_length, self.plant_name
        else:
            return 0, ''



    def get_garden_bed_size(self):
        """"Function for getting size"""
        return self.garden_bed_width * self.garden_bed_length



    def get_garden_bed_id(self):
        """"Function for getting id"""
        return self.id_



    def get_garden_bed_solid_type(self):
        """Function for getting solid type"""
        return self.soil_type


    def get_plant(self):
        """Function for getting plant name"""
        if(self.is_planted):
            return self.plant_name
        else:
            return ''
