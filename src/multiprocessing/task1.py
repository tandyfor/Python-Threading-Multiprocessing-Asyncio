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

MALE = "М"
FEMALE = "Ж"

SUCCESS = "Сдал"
FAIL = "Провалил"

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
    
    def get_row(self):
        return self.name, self.status
    
    
class Examiner(Person):
    def __init__(self, name, gender):
        super().__init__(name, gender)
        self.status = "Свободен"
        self.start_time = time.time()
        self.take_dinner = False
        self.students_count = 0
        self.flunked_student = 0

    def __str__(self):
        return "Examiner " + super().__str__() + f" {self.status}"
    
    def get_work_time(self):
        return time.time() - self.start_time

    def get_row(self):
        time = f"{self.get_work_time():.2f}"
        return self.name, self.status, self.students_count, self.flunked_student, time

    def dinner(self):
        if not self.take_dinner and self.get_work_time() > 30:
            self.status = '-'
            self.take_dinner = True
            time.sleep(random.randint(12, 18))



class Exam():
    def __init__(self, examiner: Examiner, student: Student, questions: list[str]) -> None:
        self.examiner = examiner
        self.student = student
        self.questions = random.choices(questions, k=3)
        self.mood = random.choices(MOOD, MOOD_WEIGHTS, k=1)[0]

    def exam(self):
        self.examiner.status = self.student.name
        time.sleep(len(self.examiner.name) + random.randint(-1, 1))
        self.student.status = SUCCESS if self.mood != BAD else FAIL
        self.examiner.students_count += 1
        if self.student.status == FAIL:
            self.examiner.flunked_student += 1

    def get_weights(self, len: int, gender: str):
        sequence = [1/2, 1/3]
        current = 3
        for _ in range(2, len):
            current *= 2
            sequence.append(1 / current)
        return sequence[0:len] if gender == MALE else list(reversed(sequence))[0:len]
    
    def ask_questions(self):
        for question in self.questions:
            true_answers = []
            student_answers = [] 
            student_answers.append(self.get_answer(question))
            while random.random() < 1 / 3:
                student_answer = self.get_answer(question)
                if student_answer not in student_answers:
                    student_answers.append(student_answer)

            true_answers.append(self.check_answer(question))
            while random.random() < 1 / 3:
                true_answer = self.check_answer(question)
                if true_answer not in true_answers:
                    true_answers.append(true_answer)
            


    def get_answer(self, question: list[str]):
        return random.choices(question, self.get_weights(len(question), self.student.gender), k=1)[0]

    def check_answer(self, question: list[str]):
        return random.choices(question, self.get_weights(len(question), self.examiner.gender), k=1)[0]


    def validate_response(self, student_answers: list[str], true_answers: list[str]):
        student_answers.sort()
        true_answers.sort()
        true_count = 0
        for answer in student_answers:
            true_count = true_count + 1 if answer in true_answers else true_count
        
        pass



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
        


def worker(examiner: Examiner, students: list[Student], questions: list[str]):
    while not students.empty():
        start = time.time()
        student = students.get()
        student.status = "У экзаменатора"
        exam = Exam(examiner, student, questions)
        exam.exam()
        delta = time.time() - start
        print(examiner, student, f" exam time: {delta:.2f} all work time: {examiner.get_work_time():.2f}")
        examiner.dinner()
        
def printer(examiners: multiprocessing.Queue, students_list: list[Student], examers: list[Examiner]):
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

def read_file(filename: str):
    with open(filename, "r") as file:
        return file.readlines()


def main():
    students = multiprocessing.Queue()
    examiners = multiprocessing.Queue()
    
    students_list = list(map(lambda line: Student(line.split()[0], line.split()[1]), read_file("students.txt")))
    examers = list(map(lambda line: Examiner(line.split()[0], line.split()[1]), read_file("examiners.txt")))
    questions = read_file("questions.txt")

    for student in students_list:
        students.put(student)

    processes = []
    
    printer_thread = multiprocessing.Process(target=printer, args=(examiners, students_list, examers))
    printer_thread.start()

    for examiner in examers:
        p = multiprocessing.Process(target=worker, args=(examiner, students, questions))
        processes.append(p)
        p.start()


    for p in processes:
        p.join()

    printer_thread.join()

if __name__ == "__main__":
    main()