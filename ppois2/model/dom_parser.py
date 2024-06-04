from xml.dom.minidom import parse


class PetRecordsManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.dom = parse(file_path)

    def add_pet_record(self, name, birth_date, last_visit_date, diagnosis, vet_fio):
        new_record = self.create_pet_record(name, birth_date, last_visit_date, diagnosis, vet_fio)
        self.dom.documentElement.appendChild(new_record)
        self.save_xml()

    def create_pet_record(self, name, birth_date, last_visit_date, diagnosis, vet_fio):
        pet_record = self.dom.createElement('pet_record')
        pet_record.appendChild(self.create_pet(name, birth_date, last_visit_date, diagnosis))
        pet_record.appendChild(self.create_vet(vet_fio))
        return pet_record

    def create_pet(self, name, birth_date, last_visit_date, diagnosis):
        pet = self.dom.createElement('pet')
        pet.appendChild(self.create_element_with_text('name', name))
        pet.appendChild(self.create_element_with_text('birth_date', birth_date))
        pet.appendChild(self.create_element_with_text('last_visit_date', last_visit_date))
        pet.appendChild(self.create_element_with_text('diagnosis', diagnosis))
        return pet

    def create_vet(self, fio):
        vet = self.dom.createElement('vet')
        vet.appendChild(self.create_element_with_text('fio', fio))
        return vet

    def create_element_with_text(self, tag_name, text):
        element = self.dom.createElement(tag_name)
        text_node = self.dom.createTextNode(text)
        element.appendChild(text_node)
        return element

    def save_xml(self):
        xml_str = self.dom.toprettyxml(indent="   ")
        xml_str = '\n'.join([line for line in xml_str.split('\n') if line.strip()])
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(xml_str)

    def remove_by_name_and_birth_date(self, pet_name, pet_birth_date):
        pet_records = self.dom.getElementsByTagName('pet_record')
        for pet_record in pet_records:
            pet = pet_record.getElementsByTagName('pet')[0]
            name = pet.getElementsByTagName('name')[0].firstChild.data
            birth_date = pet.getElementsByTagName('birth_date')[0].firstChild.data
            if name == pet_name and birth_date == pet_birth_date:
                self.dom.documentElement.removeChild(pet_record)
                break
        self.save_xml()

    def remove_by_last_visit_and_fio(self, pet_last_visit, vet_fio):
        pet_records = self.dom.getElementsByTagName('pet_record')
        for pet_record in pet_records:
            pet = pet_record.getElementsByTagName('pet')[0]
            vet = pet_record.getElementsByTagName('vet')[0]
            last_visit_date = pet.getElementsByTagName('last_visit_date')[0].firstChild.data
            fio = vet.getElementsByTagName('fio')[0].firstChild.data
            if last_visit_date == pet_last_visit and fio == vet_fio:
                self.dom.documentElement.removeChild(pet_record)
                break
        self.save_xml()

    def remove_by_diagnosis_phrase(self, phrase):
        pet_records = self.dom.getElementsByTagName('pet_record')
        for pet_record in pet_records:
            pet = pet_record.getElementsByTagName('pet')[0]
            diagnosis = pet.getElementsByTagName('diagnosis')[0].firstChild.data
            if phrase in diagnosis:
                self.dom.documentElement.removeChild(pet_record)
                break
        self.save_xml()
