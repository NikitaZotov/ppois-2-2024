import xml.etree.ElementTree as ET
import os

RECORDS_FILE = "../static/records.xml"

class RecordsManager:
    def __init__(self):
        self.records = {}
        if os.path.exists(RECORDS_FILE):
            self.load_records()

    def load_records(self):
        tree = ET.parse(RECORDS_FILE)
        root = tree.getroot()
        for record in root.findall('record'):
            level = int(record.find('level').text)
            nickname = record.find('nickname').text
            time = float(record.find('time').text)
            self.records[level] = {'nickname': nickname, 'time': time}

    def save_records(self):
        root = ET.Element("records")
        for level, record in self.records.items():
            record_element = ET.SubElement(root, "record")
            level_element = ET.SubElement(record_element, "level")
            level_element.text = str(level)
            nickname_element = ET.SubElement(record_element, "nickname")
            nickname_element.text = record['nickname']
            time_element = ET.SubElement(record_element, "time")
            time_element.text = str(record['time'])
        tree = ET.ElementTree(root)
        tree.write(RECORDS_FILE)

    def add_record(self, level, nickname, time):
        if level not in self.records or time < self.records[level]['time']:
            self.records[level] = {'nickname': nickname, 'time': time}
            self.save_records()

    def get_records_table(self):
        self.load_records()
        table = "Records Table:\n"
        for level, record in sorted(self.records.items(), key=lambda x: x[0]):
            table += f"Level {level}: {record['nickname']} - {record['time']} seconds\n"
        return table