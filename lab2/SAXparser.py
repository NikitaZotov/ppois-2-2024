import xml.sax


class StudentHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.students = []
        self.current_student = {}
        self.current_element = ""

    def startElement(self, name, attrs):
        self.current_element = name
        if name == "student":
            self.current_student = {}

    def characters(self, content):
        if self.current_element == "name":
            self.current_student["name"] = content.strip()
        elif self.current_element == "group":
            self.current_student["group"] = content.strip()
        elif self.current_element == "exam_title":
            self.current_student["exam_title"] = content.strip().split(";")
        elif self.current_element == "exam_grade":
            self.current_student["exam_grade"] = content.strip().split(";")

    def endElement(self, name):
        if name == "student":
            self.students.append(self.current_student)
            self.current_student = {}
        self.current_element = ""


if __name__ == "__main__":
    parser = xml.sax.make_parser()
    handler = StudentHandler()
    parser.setContentHandler(handler)
    parser.parse("data.xml")
    for student in handler.students:
        print(student)
