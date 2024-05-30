import datetime as dt

class Garden:

    """"This class creates model of garden as place"""

    def __init__(self):
        self.garden_plan = []
        self.solid_type = []

    """"Function for adding garden bed"""

    def add_garden_bed(self, length, width, soil_typ):
        id_ = len(self.garden_plan)
        try:
            length = int(length)
            width = int(width)
        except ValueError:
            return -1
        #добавить если элемента нет в массиве видов почв добавить
        self.garden_plan.append(Garden_bed(length, width, soil_typ, id_))
        return 0

    """"Function for watering plants"""

    def water_plants(self, id_):
        try:
            id_ = int(id_)
            self.garden_plan[id_]
        except:
            return -1
        return self.garden_plan[id_].watering(self)

    """"Function for taking care of plants"""

    def take_care_of_plant(self, id_):
        try:
            id_ = int(id_)
            self.garden_plan[id_]
        except:
            return -1
        return  self.garden_plan[id_].take_care(self)

    """"Function for fertilizing plants"""

    def fertilizing_lant(self, id_):
        try:
            id_ = int(id_)
            self.garden_plan[id_]
        except:
            return -1
        return self.garden_plan[id_].fertilizing(self)

    """"This function returns free beds"""

    def get_free_garden_beds(self):
        free_garden_beds_list = []
        for bed in self.garden_plan:
            if bed.get_plant == '':
                free_garden_beds_list.append(bed)
        return free_garden_beds_list

    """"This function returns free beds"""

    def get_solid_type_free_beds(self, solid):
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
        planted_beds = []
        for bed in self.garden_plan:
            if bed.get_plant != '':
                planted_beds.append(bed)
        return planted_beds

    def plant_garden_bed(self, id_, plant_name):
        try:
            id_ = int(id_)
            self.garden_plan[id_]
        except:
            return -3

        return self.garden_plan[id_].planting(plant_name)

    def collect_garden_bed(self, id_):
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

    """"Inicializing garden bed size"""

    def __init__(self, length, width, soil_type, id_):
        self.garden_bed_length = length
        self.garden_bed_width = width
        self.soil_type = soil_type
        self.id_ = id_


    """"Function for planting garden bed"""

    def planting(self, plant_name):
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


    """"Function for watering garden bed"""

    def watering(self):
        if(self.is_planted):
            self.time_of_watering = dt.datetime.now()
            return 0
        return -1

    """"Function for fertilizing garden bed"""

    def fertilizing(self):
        if(self.is_planted):
            self.time_of_fertilizing = dt.datetime.now()
            return 0
        return -1

    """"Function for taking care garden bed"""

    def take_care(self):
        if(self.is_planted):
            self.time_of_taking_care = dt.datetime.now()
            return 0
        return -1

    """"Function for collection plants"""

    def collect(self):
        if self.is_planted == True:
           self.is_planted = False
           return self.garden_bed_width*self.garden_bed_length, self.plant_name
        else:
            return 0, ''

    """"Function for getting size"""

    def get_garden_bed_size(self):
        return self.garden_bed_width * self.garden_bed_length

    """"Function for getting id"""

    def get_garden_bed_id(self):
        return self.id_

    """Function for getting solid type"""

    def get_garden_bed_solid_type(self):
        return self.soil_type

    """Function for getting plant name"""
    def get_plant(self):
        if(self.is_planted):
            return self.plant_name
        else:
            return ''
