class Scholarship:
    @staticmethod
    def calculate_stipend(average_grade):
        if average_grade == 10.0:
            return 1000
        elif 7.0 <= average_grade < 10.0:
            return 850
        elif 5.0 <= average_grade < 7.0:
            return 750
        elif 4.0 <= average_grade < 5.0:
            return 600
        else:
            return 0
