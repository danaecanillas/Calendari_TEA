import functools
import datetime

class Task():
    def __init__(self, subject_list, subject, activity_type, name, date, start_time, end_time = None, dedication = None):
        '''
        This function adds a study deadline or exam to the system (it adds it to calendar and to the queues)
        - subject: string
        - activity_type: exam/project (string)
        - name: string
        - date: string
        - start_time: string
        - end_time: string
        - dedication: number of hours needed for the deadline (integer)
        '''
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
        if self.activity_type == other.activity_type:
            return ((self.activity_type=="Projecte")*2-1)*self.date_time.timestamp() > ((other.activity_type=="Projecte")*2-1)*other.date_time.timestamp()
        return self.date_time.timestamp() > other.date_time.timestamp()