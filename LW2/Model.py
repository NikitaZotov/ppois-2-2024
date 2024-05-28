import datetime
from xmlfa import *

class Record:
    def __init__(self, student_name, father_name, father_income, mother_name, mother_income, num_brothers, num_sisters):
        self.student_name = student_name
        self.father_name = father_name
        self.father_income = father_income
        self.mother_name = mother_name
        self.mother_income = mother_income
        self.num_brothers = num_brothers
        self.num_sisters = num_sisters

class RecordModel:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def search_records(self, criteria):
        results = []
        for record in self.records:
            if self._matches_criteria(record, criteria):
                results.append(record)
        return results

    def delete_records(self, criteria):
        initial_count = len(self.records)
        self.records = [record for record in self.records if not self._matches_criteria(record, criteria)]
        deleted_count = initial_count - len(self.records)
        return deleted_count
    
    def _matches_criteria(self, record, criteria):
        if 'student_name' in criteria and criteria['student_name'] and criteria['student_name'].lower() not in record.student_name.lower():
            return False
        if 'father_name' in criteria and criteria['father_name']:
            father_name = criteria['father_name'].lower()
            if father_name not in record.father_name.lower():
                return False
        if 'mother_name' in criteria and criteria['mother_name']:
            mother_name = criteria['mother_name'].lower()
            if mother_name not in record.mother_name.lower():
                return False
        if 'num_brothers' in criteria and criteria['num_brothers'] is not None:
            if record.num_brothers != criteria['num_brothers']:
                return False
        if 'num_sisters' in criteria and criteria['num_sisters'] is not None:
            if record.num_sisters != criteria['num_sisters']:
                return False
        if 'father_income_min' in criteria and criteria['father_income_min'] is not None:
            if record.father_income < criteria['father_income_min']:
                return False
        if 'father_income_max' in criteria and criteria['father_income_max'] is not None:
            if record.father_income > criteria['father_income_max']:
                return False
        if 'mother_income_min' in criteria and criteria['mother_income_min'] is not None:
            if record.mother_income < criteria['mother_income_min']:
                return False
        if 'mother_income_max' in criteria and criteria['mother_income_max'] is not None:
            if record.mother_income > criteria['mother_income_max']:
                return False
        return True


    def load_from_file(self, file_path):
        self.records = [Record(**rec) for rec in load_records_from_xml(file_path)]

    def save_to_file(self, file_path):
        save_records_to_xml([rec.__dict__ for rec in self.records], file_path)
