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
        profile: name of the person (string)
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
                with open(f'{self.profile_folder}deadlines.pickle', 'rb') as f:
                    self.deadlines = PriorityQueue()
                    deadlines = pickle.load(f)
                    for deadline in deadlines:
                        self.deadlines.put(deadline)
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
        '''
        This function sets the default parameters for a new profile
        '''
        self.subject_list = ["TFG", "PE", "TAED1", "POE", "PIVA"] # to be changed
        a = np.zeros((24, 7))
        a[15:21, 0:5] = True
        a[9:13, 5:7] = a[16:20, 5:7] = True
        self.weekly_schedule = a
        self.schedule = {}
        self.deadlines = PriorityQueue()


    def add_to_calendar(self, t):
        '''
        This function adds task t to self.schedule
        - t: task to be added (Task)
        '''
        str_date = datetime.datetime.strftime(t.date_time, '%Y/%m/%d')
        str_clock = datetime.datetime.strftime(t.date_time, '%H:%M')
        if not str_date in self.schedule.keys():
            self.schedule[str_date] = {}
        self.schedule[str_date][str_clock] = t


    def free_weekly_slot(self, date_schedule):
        '''
        This function tells whether date_schedule is free in the weekly calendar
        - date_schedule: time slot (datetime.datetime)
        '''
        date = date_schedule.date()
        week_day = date.weekday()
        int_hour = int(datetime.datetime.strftime(date_schedule, '%H'))
        return self.weekly_schedule[int_hour, week_day]


    def free_calendar_slot(self, date_schedule):
        '''
        This function tells whether date_schedule is free in the calendar
        - date_schedule: time slot (datetime.datetime)
        '''
        str_date = datetime.datetime.strftime(date_schedule, '%Y/%m/%d')
        str_clock = datetime.datetime.strftime(date_schedule, '%H:%M')
        return str_date not in self.schedule.keys() or str_clock not in self.schedule[str_date].keys()


    def set_study_periode(self, exam, now, first_slot, last_slot):
        '''
        This function sets study times for an exam between 2 timestamps
        - exam: exam to be set (Task)
        - now: current time (datetime.datetime)
        - first_slot: first slot in chronological time where we try to set study time (last to be tried)
        - last_slot: last slot in chronological time where we try to set study time (first to be tried)
        '''
        time_slot = last_slot
        
        while time_slot > now and time_slot >= first_slot:
            if exam.dedication == 0:
                return time_slot
            if self.free_weekly_slot(time_slot) and self.free_calendar_slot(time_slot):
                # subtask creation:
                sub_t = deepcopy(exam)
                sub_t.activity_type = "Estudi"
                sub_t.dedication = 1
                sub_t.date_time = time_slot
                self.add_to_calendar(sub_t)
                exam.dedication -= 1
            time_slot -= datetime.timedelta(hours = 1)
                
        if time_slot < now:
            # raise Exception(f"La tasca no es podrà fer. Caldrà afegir hores a l'horari.")
            print(f"No dóna temps a estudiar tots els exàmens. Caldrà afegir hores a l'horari.")
            return -1
        return 0 # time_slot < first_slot
        

    def set_exam_schedule(self):
        '''
        This function sets study times in the calendar
        '''
        exams = self.exam_queue.queue
        exams = sorted(exams)
        now = datetime.datetime.now()

        ex_it = 0
        while ex_it < len(exams):
            last_slot = exams[ex_it].date_time - datetime.timedelta(hours = 2) # we leave the hour before the exam empty
            if ex_it == len(exams)-1:
                first_slot = now
            else:
                first_slot = exams[ex_it+1].date_time + datetime.timedelta(hours = 5) # we start studying 5 hours after the exam before

            exam = exams[ex_it]
            res = self.set_study_periode(exam, now, first_slot, last_slot)

            # filling up the available time after first_slot (if there is) with pending study time from future exams:
            aux_it = 0
            while type(res) == datetime.datetime and aux_it < ex_it:
                exam = exams[aux_it]
                res = self.set_study_periode(exam, now, first_slot, res)
                aux_it += 1
            if res == -1:
                return False
            ex_it += 1

        return True


    def set_project_schedule(self):
        '''
        This function sets project work times in the calendar
        '''
        now = datetime.datetime.now()
        date_schedule = now.replace(second=0, microsecond=0, minute=0, hour=now.hour)

        while not self.project_queue.empty():
            t = self.project_queue.get()
            possible = False
            while date_schedule < t.date_time and not possible:
                date_schedule += datetime.timedelta(hours = 1)
                possible = self.free_weekly_slot(date_schedule) and self.free_calendar_slot(date_schedule)
            if not possible:
                print(f"La tasca {t.name} de l'assignatura de {t.subject} no es podrà fer. Caldrà afegir hores a l'horari.")
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
        '''
        This function sets all preparation times in the calendar
        '''
        self.set_exam_schedule()
        self.set_project_schedule()    
    

    def add_to_queue(self, t):
        '''
        This function adds a task to its corresponding queue
        - t: task
        '''
        if t.activity_type == "Examen":
            self.exam_queue.put(t)
        elif t.activity_type == "Projecte":
            self.project_queue.put(t)


    def add_deadline(self, subject, activity_type, name, date, start_time, end_time=None, dedication=None):
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
        if activity_type not in ["Examen", "Projecte"]:
            raise Exception(f"Not a deadline activity")
        if not dedication:
            dedication = self.default_time[activity_type]
        t = Task(self.subject_list, subject, activity_type, name, date, start_time, end_time, dedication)
        self.add_to_calendar(t)
        self.add_to_queue(t)
        self.deadlines.put(t)
        if self.auto_schedule:
            self.set_schedule()
            
    
    def get_schedule(self):
        return self.schedule


    def get_deadline_list(self):
        '''
        This function returns a list of the deadlines
        '''
        return self.deadlines.queue


    def get_next_deadlines(self):
        '''
        This function returns a list of the next deadlines
        '''
        now = datetime.datetime.now()
        deadlines = self.get_deadline_list()
        id_t = 0
        while id_t < len(deadlines):
            if now <= deadlines[id_t].date_time:
                break
            id_t += 1
        return deadlines[id_t:min(id_t+10, len(deadlines))]
        

    def save_subject_list(self):
        '''
        This function saves self.subject_list
        '''
        if not os.path.exists(self.profile_folder):
            os.mkdir(self.profile_folder)
            
        with open(f'{self.profile_folder}subject_list.pickle', 'wb') as f:
            pickle.dump(self.subject_list, f, pickle.HIGHEST_PROTOCOL)


    def save_weekly_schedule(self):
        '''
        This function saves self.weekly_schedule
        '''
        if not os.path.exists(self.profile_folder):
            os.mkdir(self.profile_folder)

        with open(f'{self.profile_folder}weekly_schedule.pickle', 'wb') as f:
            pickle.dump(self.weekly_schedule, f, pickle.HIGHEST_PROTOCOL)
    

    def save_schedule(self):
        '''
        This function saves self.schedule
        '''
        if not os.path.exists(self.profile_folder):
            os.mkdir(self.profile_folder)

        with open(f'{self.profile_folder}schedule.pickle', 'wb') as f:
            pickle.dump(self.schedule, f, pickle.HIGHEST_PROTOCOL)


    def save_deadlines(self):
        '''
        This function saves self.deadlines
        '''
        if not os.path.exists(self.profile_folder):
            os.mkdir(self.profile_folder)

        with open(f'{self.profile_folder}deadlines.pickle', 'wb') as f:
            pickle.dump(self.get_deadline_list(), f, pickle.HIGHEST_PROTOCOL)


    def save_profile(self):
        '''
        This function saves profile features to a file
        '''
        self.save_subject_list()
        self.save_weekly_schedule()
        self.save_schedule()
        self.save_deadlines()      