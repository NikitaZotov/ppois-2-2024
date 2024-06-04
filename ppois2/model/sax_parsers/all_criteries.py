import xml.sax


class PetAnyHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.result = []
        self.current_pet = {}
        self.inside_pet = False
        self.current_tag = None

    def startElement(self, name, attrs):
        if name == 'pet':
            self.inside_pet = True
        else:
            self.current_tag = name

    def characters(self, content):
        if self.current_tag is not None and self.inside_pet:
            content = content.strip()
            if content:
                self.current_pet[self.current_tag] = content

    def endElement(self, name):
        if name == 'pet' and self.current_pet:
            self.result.append(self.current_pet)
            self.current_pet = {}
            self.inside_pet = False
        self.current_tag = None


class VetAnyHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.result = []
        self.current_vet = {}
        self.inside_vet = False
        self.current_tag = None

    def startElement(self, name, attrs):
        if name == 'vet':
            self.inside_vet = True
        else:
            self.current_tag = name

    def characters(self, content):
        if self.current_tag is not None and self.inside_vet:
            content = content.strip()
            if content:
                self.current_vet[self.current_tag] = content

    def endElement(self, name):
        if name == 'vet' and self.current_vet:
            self.result.append(self.current_vet)
            self.current_vet = {}
            self.inside_vet = False
        self.current_tag = None

