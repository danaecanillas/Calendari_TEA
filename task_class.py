import functools
import datetime

class Task():
    def __init__(self, subject_list, subject, activity_type, name, date, start_time, end_time = None, dedication = None):
        if activity_type not in ["Examen", "Projecte", "Estudi", "Fer treball"]:
            raise Exception(f"Not a correct activity")
        self.activity_type = activity_type
        if subject not in subject_list:
            raise Exception(f"Not a correct subject")
        self.subject = subject
        self.name = name
        self.date_time = datetime.datetime.strptime(date + " " + start_time, '%Y/%m/%d %H:%M')
        self.end_time = end_time
        self.dedication = dedication
        self.finished = False


    def finish(self):
        self.finished = True

    
    def __gt__(self, other):
        return self.dedication < other.dedication