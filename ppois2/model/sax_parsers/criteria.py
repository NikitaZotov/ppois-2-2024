import xml.sax


class NameBirthDateHandler(xml.sax.ContentHandler):
    def __init__(self, name, birth_date):
        self.name = name
        self.birth_date = birth_date
        self.result = []
        self.current_pet = {}
        self.inside_pet_record = False
        self.current_tag = None

    def startElement(self, name, attrs):
        if name == 'pet_record':
            self.inside_pet_record = True
        else:
            self.current_tag = name

    def characters(self, content):
        if self.current_tag is not None and self.inside_pet_record:
            content = content.strip()
            if content:
                self.current_pet[self.current_tag] = content

    def endElement(self, name):
        if name == 'pet_record' and self.current_pet:
            if (self.current_pet.get('name') == self.name and
                    self.current_pet.get('birth_date') == self.birth_date):
                self.result.append(self.current_pet)
            self.current_pet = {}
            self.inside_pet_record = False
        self.current_tag = None


class LastVisitVetNameHandler(xml.sax.ContentHandler):
    def __init__(self, last_visit_date, fio):
        self.last_visit_date = last_visit_date
        self.fio = fio
        self.result = []
        self.current_pet = {}
        self.inside_pet_record = False
        self.current_tag = None

    def startElement(self, name, attrs):
        if name == 'pet':
            self.inside_pet_record = True
        else:
            self.current_tag = name

    def characters(self, content):
        if self.current_tag is not None and self.inside_pet_record:
            content = content.strip()
            if content:
                self.current_pet[self.current_tag] = content

    def endElement(self, name):
        if name == 'pet_record' and self.current_pet:
            if (self.current_pet.get('last_visit_date') == self.last_visit_date and
                    self.current_pet.get('fio') == self.fio):
                self.result.append(self.current_pet)
            self.current_pet = {}
            self.inside_pet_record = False
        self.current_tag = None


class DiagnosisPhraseHandler(xml.sax.ContentHandler):
    def __init__(self, phrase):
        self.phrase = phrase
        self.result = []
        self.current_pet = {}
        self.inside_pet_record = False
        self.current_tag = None

    def startElement(self, name, attrs):
        if name == 'pet_record':
            self.inside_pet_record = True
        else:
            self.current_tag = name

    def characters(self, content):
        if self.current_tag is not None and self.inside_pet_record:
            content = content.strip()
            if content:
                self.current_pet[self.current_tag] = content

    def endElement(self, name):
        if name == 'pet_record' and self.current_pet:
            if self.phrase in self.current_pet.get('diagnosis'):
                self.result.append(self.current_pet)
            self.current_pet = {}
            self.inside_pet_record = False
        self.current_tag = None
