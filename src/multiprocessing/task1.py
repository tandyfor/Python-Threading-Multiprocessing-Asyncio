import random
import time
import multiprocessing.dummy as multiprocessing
import threading

import prettytable

BAD = 0
NEUTRAL = 1
GOOD = 2

MOOD = [BAD, NEUTRAL, GOOD]
MOOD_WEIGHTS = [0.125, 0.625, 0.25]

MALE = 0
FEMALE = 1 

class Person():
    def __init__(self, name, gender) -> None:
        self.name = name
        self.gender = gender
        self.status = None

    def __str__(self) -> str:
        return f"{self.name} {self.gender}"


class Student(Person):
    def __init__(self, name, gender):
        super().__init__(name, gender)
        self.status = "Очередь"

    def __str__(self):
        return "Student " + super().__str__() + f" {self.status}"
    
    def get_answer(self):
        return random.randint(2, 5)

    def get_row(self):
        return self.name, self.status
    
    
class Examiner(Person):
    def __init__(self, name, gender):
        super().__init__(name, gender)
        self.status = "Свободен"
        self.start_time = time.time()
        self.take_dinner = False

    def __str__(self):
        return "Examiner " + super().__str__() + f" {self.status}"
    
    def evaluate_work(self, answer):
        return True if answer >= 3 else False

    def do_exam(self, student: Student):
        self.status = student.name
        time.sleep(len(self.name) + random.randint(-1, 1))
        res = self.evaluate_work(student.get_answer())
        student.status = "Сдал" if res else "Провалил"

    def get_work_time(self):
        return time.time() - self.start_time

    def get_row(self):
        time = f"{self.get_work_time():.2f}"
        return self.name, self.status, None, None, time

    def dinner(self):
        if not self.take_dinner and self.get_work_time() > 30:
            self.status = '-'
            self.take_dinner = True
            time.sleep(random.randint(12, 18))



class Exam():
    def __init__(self, examiner: Examiner, student: Student) -> None:
        self.examiner = examiner
        self.student = student
        self.mood = random.choices(MOOD, MOOD_WEIGHTS, k=1)[0]
    
    def exam(self):
        self.examiner.status = self.student.name
        time.sleep(len(self.examiner.name) + random.randint(-1, 1))
        self.student.status = "Сдал" if self.mood != BAD else "Провалил"


class Viewer():
    def __init__(self) -> None:
        self.students_tabel = prettytable.PrettyTable()
        self.students_tabel.field_names = ["Студент", "Статус"]
        
        self.examiner_tabel = prettytable.PrettyTable()
        self.examiner_tabel.field_names = ["Экзаменатор", "Текущий студент", "Всего студентов", "Завалил", "Время работы"]

        self.students: list[Student]
        self.examiners: list[Examiner]

    def update_student(self):
        self.students_tabel.clear_rows()
        for student in self.students:
            self.students_tabel.add_row(student.get_row())

    def update_examiner(self):
        self.examiner_tabel.clear_rows()
        for examiner in self.examiners:
            self.examiner_tabel.add_row(examiner.get_row())

    def __str__(self):
        return f"{self.students_tabel}\n{self.examiner_tabel}"
        


def worker(examiner: Examiner):
    while not students.empty():
        start = time.time()
        student = students.get()
        student.status = "У экзаменатора"
        exam = Exam(examiner, student)
        exam.exam()
        delta = time.time() - start
        print(examiner, student, f" exam time: {delta:.2f} all work time: {examiner.get_work_time():.2f}")
        examiner.dinner()
        
def printer(examiners: multiprocessing.Queue):
    v = Viewer()
    time.sleep(0.1)
    v.students = students_list
    v.examiners = examers

    while not len(threading.enumerate()) == 2:
        v.update_examiner()
        v.update_student()
        print("\033c")
        print(v)
        print(len(threading.enumerate()))
        time.sleep(0.05)

    

if __name__ == "__main__":
    students = multiprocessing.Queue()
    examiners = multiprocessing.Queue()
    
    students_list = [
        Student("Mark", "M"),
        Student("David", "M"),
        Student("John", "M"),
        Student("Mark", "M"),
        Student("David", "M"),
        Student("John", "M"),
        Student("Mark", "M"),
        Student("David", "M"),
        Student("John", "M"),
        Student("Ray", "M")
    ]

    examers = [
        Examiner("Dmitriy", "M"),
        Examiner("Albert", "M")
    ]


    for student in students_list:
        students.put(student)

    processes = []
    
    printer_thread = multiprocessing.Process(target=printer, args=(examiners, ))
    # processes.append(p)
    printer_thread.start()

    for examiner in examers:
        p = multiprocessing.Process(target=worker, args=(examiner, ))
        processes.append(p)
        p.start()


    for p in processes:
        p.join()

    printer_thread.join()

    