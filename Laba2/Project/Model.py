# app/model.py
import xml.sax

class Record:
    def __init__(self, faculty="", department="", professor="", rank="", degree="", experience=0):
        self.faculty = faculty
        self.department = department
        self.professor = professor
        self.rank = rank
        self.degree = degree
        self.experience = experience

    def equals(self, other):
        return (
            self.faculty == other.faculty and
            self.department == other.department and
            self.professor == other.professor and
            self.rank == other.rank and
            self.degree == other.degree and
            self.experience == other.experience
        )

class RecordsHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.records = []
        self.current_data = ""
        self.professor = ""
        self.department = ""
        self.rank = ""
        self.faculty = ""
        self.degree = ""
        self.experience = 0
        self.buffer = ""

    def startElement(self, tag, attributes):
        self.current_data = tag
        self.buffer = ""

    def endElement(self, tag):
        if self.current_data == "professor":
            self.professor = self.buffer
        elif self.current_data == "department":
            self.department = self.buffer
        elif self.current_data == "rank":
            self.rank = self.buffer
        elif self.current_data == "faculty":
            self.faculty = self.buffer
        elif self.current_data == "degree":
            self.degree = self.buffer
        elif self.current_data == "experience":
            self.experience = int(self.buffer)
        elif tag == "record":
            self.records.append(Record(self.faculty, self.department, self.professor, self.rank, self.degree, self.experience))
            self.professor = ""
            self.department = ""
            self.rank = ""
            self.faculty = ""
            self.degree = ""
            self.experience = 0
        self.current_data = ""

    def characters(self, content):
        if self.current_data:
            self.buffer += content.strip()

