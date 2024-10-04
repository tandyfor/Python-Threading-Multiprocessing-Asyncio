import random
import time
import multiprocessing.dummy as multiprocessing
import threading

import prettytable


class Person():
    def __init__(self, name, second_name) -> None:
        self.name = name
        self.second_name = second_name

    def __str__(self) -> str:
        return f"{self.name} {self.second_name}"


class Student(Person):
    def __init__(self, name, second_name):
        super().__init__(name, second_name)
        self.status = "Очередь"

    def __str__(self):
        return "Student " + super().__str__() + f" {self.status}"
    
    def get_answer(self):
        return random.randint(2, 5)

    def get_row(self):
        return self.name, self.status
    
    
class Examiner(Person):
    def __init__(self, name, second_name):
        super().__init__(name, second_name)
        self.status = "Свободен"
        self.start_time = time.time()
        self.student = None

    def __str__(self):
        return "Examiner " + super().__str__() + f" {self.status}"
    
    def evaluate_work(self, answer):
        return True if answer >= 3 else False

    def do_exam(self, student: Student):
        self.student = student
        time.sleep(len(self.name) + random.randint(-1, 1))
        res = self.evaluate_work(student.get_answer())
        student.status = "Сдал" if res else "Провалил"

    def get_work_time(self):
        return time.time() - self.start_time

    def get_row(self):
        student = self.student.name if (self.student) else None
        time = f"{self.get_work_time():.2f}"
        return self.name, self.student, None, None, time


class Viewer():
    def __init__(self) -> None:
        self.students_tabel = prettytable.PrettyTable()
        self.students_tabel.field_names = ["Студент", "Статус"]
        self.examiner_tabel = prettytable.PrettyTable()
        self.examiner_tabel.field_names = ["Экзаменатор", "Текущий студент", "Всего студентов", "Завалил", "Время работы"]

    def add_student(self, process_students: multiprocessing.Queue):
        if not process_students.empty():
            data = process_students.get().get_row()
            self.students_tabel.add_row(data)

    def add_examiner(self, examiners: multiprocessing.Queue):
        if not examiners.empty():
            data = examiners.get().get_row()
            self.examiner_tabel.add_row(data)

    def update_student(self, student: Student):
        pass

    def update_examiner(self, examiner: Examiner):
        pass

    def __str__(self):
        return f"{self.students_tabel}\n{self.examiner_tabel}"
        


def worker(examiner: Examiner):
    while not students.empty():
        start = time.time()
        student = students.get()
        student.status = "У экзаменатора"
        process_students.put(student)
        examiner.do_exam(student)
        examiners.put(examiner)
        delta = time.time() - start
        print(examiner, student, f" exam time: {delta:.2f} all work time: {examiner.get_work_time():.2f}")
        process_students.put(student)
        
def printer(process_students: multiprocessing.Queue, examiners: multiprocessing.Queue):
    v = Viewer()
    time.sleep(0.1)

    # while not students.empty() or not process_students.empty():
    while True: # TODO: Signal for stop. When examiners free, and students quere are empty.
        v.add_student(process_students)
        v.add_examiner(examiners)
        print("\033c")
        print(v)
        print(len(threading.enumerate()))
        time.sleep(0.1)
        if len(threading.enumerate()) == 2 and process_students.empty() and examiners.empty():
            break

    

if __name__ == "__main__":
    students = multiprocessing.Queue()
    process_students = multiprocessing.Queue()
    examiners = multiprocessing.Queue()
    
    students_list = [
        Student("Mark", "Jonson"),
        Student("David", "Martinez"),
        Student("John", "Brown"),
        Student("Ray", "Charles")
    ]

    examers = [
        Examiner("Dmitriy", "Fedorov"),
        Examiner("Albert", "Einshtein")
    ]


    for student in students_list:
        students.put(student)

    processes = []
    
    p = multiprocessing.Process(target=printer, args=(process_students, examiners))
    processes.append(p)
    p.start()

    for examiner in examers:
        p = multiprocessing.Process(target=worker, args=(examiner, ))
        processes.append(p)
        p.start()


    for p in processes:
        p.join()

    