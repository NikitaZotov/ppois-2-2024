import xml.etree.ElementTree as ET

class Pet:
    def __init__(self, pets_name, date_of_birth, last_appointment, veterinarian, diagnosis):
        self.pets_name = pets_name
        self.date_of_birth = date_of_birth
        self.last_appointment = last_appointment
        self.veterinarian = veterinarian
        self.diagnosis = diagnosis

class PetModel:
    def __init__(self):
        self.records = []
        self._observers = []

    def save_to_xml(self, file_path):
        root = ET.Element("pets")
        for record in self.records:
            pet_element = ET.SubElement(root, "pet")
            for key, value in record.__dict__.items():
                ET.SubElement(pet_element, key).text = str(value)

        tree = ET.ElementTree(root)
        tree.write(file_path, encoding="utf-8", xml_declaration=True)

    def load_from_xml(self, file_path):
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            self.records.clear()
            for pet_element in root.findall("pet"):
                record = {}
                for child in pet_element:
                    record[child.tag] = child.text
                pet = Pet(**record)
                self.records.append(pet)
            return self.records
        except Exception as e:
            raise Exception(f"Error loading XML file: {str(e)}")

    def perform_search(self, search_criteria) -> list[Pet]:
        search_results = []
        for record in self.records:
            if self.matches_criteria(record, search_criteria):
                search_results.append(record)
        self.notify_observers()
        return search_results

    def matches_criteria(self, record, search_criteria):
        for key, value in search_criteria.items():
            if key == 'phrase_diagnosis':
                if value not in record.diagnosis:
                    return False
            elif key == 'pet_name':
                if value != record.pets_name:
                    return False
            elif key == 'dob':
                if value != record.date_of_birth:
                    return False
            elif key == 'last_appointment':
                if value != record.last_appointment:
                    return False
            elif key == 'veterinarian':
                if value != record.veterinarian:
                    return False
        return True

    def add_pet(self, pet_info):
        pet = Pet(*pet_info)
        self.records.append(pet)
        self.notify_observers()

    def delete_items(self, search_criteria):
        items_to_delete = []
        for record in self.records:
            if self.matches_criteria(record, search_criteria):
                items_to_delete.append(record)

        for item in items_to_delete:
            self.records.remove(item)
        self.notify_observers()

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for x in self._observers:
            x.model_is_changed()
