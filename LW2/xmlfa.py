import xml.sax
import xml.etree.ElementTree as ET

class RecordHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.current_data = ""
        self.current_record = {}
        self.records = []

    def startElement(self, tag, attributes):
        self.current_data = tag
        if tag == "record":
            self.current_record = {}

    def endElement(self, tag):
        if self.current_data == "student_name":
            self.current_record["student_name"] = self.content
        elif self.current_data == "father_name":
            self.current_record["father_name"] = self.content
        elif self.current_data == "father_income":
            self.current_record["father_income"] = float(self.content)
        elif self.current_data == "mother_name":
            self.current_record["mother_name"] = self.content
        elif self.current_data == "mother_income":
            self.current_record["mother_income"] = float(self.content)
        elif self.current_data == "num_brothers":
            self.current_record["num_brothers"] = int(self.content)
        elif self.current_data == "num_sisters":
            self.current_record["num_sisters"] = int(self.content)
        elif tag == "record":
            self.records.append(self.current_record)
        self.current_data = ""

    def characters(self, content):
        self.content = content
    
def load_records_from_xml(file_path):
    parser = xml.sax.make_parser()
    handler = RecordHandler()
    parser.setContentHandler(handler)
    parser.parse(file_path)
    return handler.records

def save_records_to_xml(records, file_path):
    root = ET.Element("records")
    for record in records:
        record_element = ET.SubElement(root, "record")
        for key, value in record.items():
            element = ET.SubElement(record_element, key)
            element.text = str(value)
    tree = ET.ElementTree(root)
    tree.write(file_path, encoding='utf-8', xml_declaration=True)