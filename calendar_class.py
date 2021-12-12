import time
import datetime
from queue import PriorityQueue
import numpy as np
from copy import deepcopy
import pickle
import os.path

from task_class import Task


class Calendar():
    def __init__(self, profile=None):
        '''
        profile: name of the person
        '''
        dir_folder = os.path.dirname(__file__)
        if profile:
            self.profile_folder = f'{dir_folder}/perfils/{profile}/'
            if os.path.exists(self.profile_folder):
                with open(f'{self.profile_folder}subject_list.pickle', 'rb') as f:
                    self.subject_list = pickle.load(f)
                with open(f'{self.profile_folder}weekly_schedule.pickle', 'rb') as f:
                    self.weekly_schedule = pickle.load(f)
                with open(f'{self.profile_folder}schedule.pickle', 'rb') as f:
                    self.schedule = pickle.load(f)
            else:
                self.set_default_profile()
        else:
            self.set_default_profile()

        self.activity_types = ["Examen", "Projecte", "Estudi", "Fer treball"]
        self.default_time = {"Examen": 30, "Projecte": 20}
        self.exam_queue = PriorityQueue()
        self.project_queue = PriorityQueue()
        self.auto_schedule = False
        

    def set_default_profile(self):
        self.subject_list = ["TFG", "PE", "TAED1", "POE", "PIVA"]
        a = np.zeros((24, 7))
        a[15:21, 0:5] = True
        a[9:13, 5:7] = a[16:20, 5:7] = True
        self.weekly_schedule = a
        self.schedule = {}


    def add_to_calendar(self, t):
        str_date = datetime.datetime.strftime(t.date_time, '%Y/%m/%d')
        str_clock = datetime.datetime.strftime(t.date_time, '%H:%M')
        if not str_date in self.schedule.keys():
            self.schedule[str_date] = {}
        self.schedule[str_date][str_clock] = t


    def free_weekly_slot(self, date_schedule):
        date = date_schedule.date()
        week_day = date.weekday()
        int_hour = int(datetime.datetime.strftime(date_schedule, '%H'))
        return self.weekly_schedule[int_hour, week_day]


    def free_calendar_slot(self, date_schedule):
        str_date = datetime.datetime.strftime(date_schedule, '%Y/%m/%d')
        str_clock = datetime.datetime.strftime(date_schedule, '%H:%M')
        return str_date not in self.schedule.keys() or str_clock not in self.schedule[str_date].keys()


    def set_exam_schedule(self):
        now = datetime.datetime.now()

        if not self.exam_queue.empty():
            _, t = self.exam_queue.get()
            date_schedule = t.date_time # date of the last exam
            self.add_to_queue(t)

        while not self.exam_queue.empty():
            # print("mida cua exam", self.exam_queue.qsize())
            _, t = self.exam_queue.get()
            # print("selected exam is", t.name, "pending hours:", t.dedication)
            date_schedule = min(date_schedule, t.date_time-datetime.timedelta(hours = 1))
            possible = False
            while date_schedule > now and not possible:
                # print(date_schedule)
                date_schedule -= datetime.timedelta(hours = 1)
                possible = self.free_weekly_slot(date_schedule) and self.free_calendar_slot(date_schedule)
            if not possible:
                print("La tasca no es podrà fer. Caldrà afegir hores a l'horari.")
            else:
                # subtask creation:
                sub_t = deepcopy(t)
                sub_t.activity_type = "Estudi"
                sub_t.dedication = 1
                sub_t.date_time = date_schedule
                self.add_to_calendar(sub_t)

                t.dedication -= 1
                if t.dedication != 0:
                    self.add_to_queue(t)


    def set_project_schedule(self):
        now = datetime.datetime.now()
        date_schedule = now.replace(second=0, microsecond=0, minute=0, hour=now.hour)

        while not self.project_queue.empty():
            _, t = self.project_queue.get()
            # print("selected project is", t.name, "pending hours:", t.dedication)
            possible = False
            while date_schedule < t.date_time and not possible:
                date_schedule += datetime.timedelta(hours = 1)
                possible = self.free_weekly_slot(date_schedule) and self.free_calendar_slot(date_schedule)
            if not possible:
                print("La tasca no es podrà fer. Caldrà afegir hores a l'horari.")
            else:
                # subtask creation:
                sub_t = deepcopy(t)
                sub_t.activity_type = "Fer treball"
                sub_t.dedication = 1
                sub_t.date_time = date_schedule
                self.add_to_calendar(sub_t)

                t.dedication -= 1
                if t.dedication != 0:
                    self.add_to_queue(t)


    def set_schedule(self):
        self.set_exam_schedule()
        self.set_project_schedule()    
    

    def add_to_queue(self, t):
        if t.activity_type == "Examen":
            self.exam_queue.put((-t.date_time.timestamp(), t))
        elif t.activity_type == "Projecte":
            self.project_queue.put((t.date_time.timestamp(), t))


    def add_deadline(self, subject, activity_type, name, date, start_time, end_time=None, dedication=None):
        if activity_type not in ["Examen", "Projecte"]:
            raise Exception(f"Not a deadline activity")
        if not dedication:
            dedication = self.default_time[activity_type]
        t = Task(self.subject_list, subject, activity_type, name, date, start_time, end_time, dedication)
        self.add_to_calendar(t)
        self.add_to_queue(t)
        if self.auto_schedule:
            self.set_schedule()
            
    
    def get_schedule(self):
        return self.schedule


    def save_profile(self):
        if not os.path.exists(self.profile_folder):
            os.mkdir(self.profile_folder)

        with open(f'{self.profile_folder}subject_list.pickle', 'wb') as f:
            pickle.dump(self.subject_list, f, pickle.HIGHEST_PROTOCOL)
        
        with open(f'{self.profile_folder}weekly_schedule.pickle', 'wb') as f:
            pickle.dump(self.weekly_schedule, f, pickle.HIGHEST_PROTOCOL)

        with open(f'{self.profile_folder}schedule.pickle', 'wb') as f:
            pickle.dump(self.schedule, f, pickle.HIGHEST_PROTOCOL)