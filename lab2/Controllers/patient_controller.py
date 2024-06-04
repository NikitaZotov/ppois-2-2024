import math
from Models.patient import Patient

class PatientController:
    def __init__(self):
        self.patients_list = []
        self.rec_per_page = 10
        self.current_page = 1
        self.total_pages = 1

    def add_patient(self, patient):
        self.patients_list.append(patient)
        self.update_total_pages()

    def delete_patient(self, delete_type, query):
        indices_to_delete = []
        for i, patient in enumerate(self.patients_list):
            if delete_type == "ФИО пациента или адресу прописки" and (query.lower() in patient.full_name.lower() or query.lower() in patient.address.lower()):
                indices_to_delete.append(i)
            elif delete_type == "Дата рождения" and query == patient.birth_date:
                indices_to_delete.append(i)
            elif delete_type == "ФИО врача или дате приема" and (query.lower() in patient.doctor_name.lower() or query == patient.appointment_date):
                indices_to_delete.append(i)

        for index in reversed(indices_to_delete):
            del self.patients_list[index]

    def search_patient(self, search_type, query):
        results = []
        for patient in self.patients_list:
            if search_type == "ФИО пациента или адресу прописки" and (query.lower() in patient.full_name.lower() or query.lower() in patient.address.lower()):
                results.append(patient)
            elif search_type == "Дата рождения" and query == patient.birth_date:
                results.append(patient)
            elif search_type == "ФИО врача или дате приема" and (query.lower() in patient.doctor_name.lower() or query == patient.appointment_date):
                results.append(patient)
        return results

    def update_total_pages(self):
        self.total_pages = math.ceil(len(self.patients_list) / self.rec_per_page)

    def get_patients_for_page(self):
        start_index = (self.current_page - 1) * self.rec_per_page
        end_index = self.current_page * self.rec_per_page
        return self.patients_list[start_index:end_index]

    def save_data(self, file_path):
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("<Patients>\n")
            for patient in self.patients_list:
                file.write(f"  <Patient>\n")
                file.write(f"    <Full_Name>{patient.full_name}</Full_Name>\n")
                file.write(f"    <Address>{patient.address}</Address>\n")
                file.write(f"    <Birth_Date>{patient.birth_date}</Birth_Date>\n")
                file.write(f"    <Appointment_Date>{patient.appointment_date}</Appointment_Date>\n")
                file.write(f"    <Doctor_Name>{patient.doctor_name}</Doctor_Name>\n")
                file.write(f"    <Conclusion>{patient.conclusion}</Conclusion>\n")
                file.write(f"  </Patient>\n")
            file.write("</Patients>\n")

    def load_data(self, file_path):
        import xml.sax

        class PatientHandler(xml.sax.ContentHandler):
            def __init__(self):
                self.current_element = ""
                self.full_name = ""
                self.address = ""
                self.birth_date = ""
                self.appointment_date = ""
                self.doctor_name = ""
                self.conclusion = ""
                self.patients_list = []

            def startElement(self, name, attrs):
                self.current_element = name

            def characters(self, content):
                if self.current_element == "Full_Name":
                    self.full_name += content.strip()
                elif self.current_element == "Address":
                    self.address += content.strip()
                elif self.current_element == "Birth_Date":
                    self.birth_date += content.strip()
                elif self.current_element == "Appointment_Date":
                    self.appointment_date += content.strip()
                elif self.current_element == "Doctor_Name":
                    self.doctor_name += content.strip()
                elif self.current_element == "Conclusion":
                    self.conclusion += content.strip()

            def endElement(self, name):
                if name == "Patient":
                    patient = Patient(self.full_name, self.address, self.birth_date, self.appointment_date, self.doctor_name, self.conclusion)
                    self.patients_list.append(patient)
                    self.full_name = ""
                    self.address = ""
                    self.birth_date = ""
                    self.appointment_date = ""
                    self.doctor_name = ""
                    self.conclusion = ""

        handler = PatientHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(file_path)
        self.patients_list = handler.patients_list
        self.update_total_pages()
