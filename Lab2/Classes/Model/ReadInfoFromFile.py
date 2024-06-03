import xml.sax

class ReadFromFile(xml.sax.ContentHandler):
    def __init__(self, schedule):
        self.schedule = schedule
        self.current_data = ""
        self.number = ""
        self.first_station = ""
        self.last_station = ""
        self.departure_time = ""
        self.arrival_time = ""

    def startElement(self, tag, attributes):
        self.current_data = tag

    def endElement(self, tag):
        if self.current_data == "number":
            self.number = self.characters_data
        elif self.current_data == "first_station":
            self.first_station = self.characters_data
        elif self.current_data == "last_station":
            self.last_station = self.characters_data
        elif self.current_data == "departure_time":
            self.departure_time = self.characters_data
        elif self.current_data == "arrival_time":
            self.arrival_time = self.characters_data

        if tag == "train":
            self.schedule.addNewTrain(self.number, self.first_station, self.last_station, self.departure_time, self.arrival_time)

        self.current_data = ""

    def characters(self, content):
        self.characters_data = content

    def get_trains(self):
        return self.schedule.list_of_trains