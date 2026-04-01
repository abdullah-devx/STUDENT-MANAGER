class Student:
    def __init__(self, name):
        self.name = name
        self.grades = []

    def add_grade(self, subject, score):
        self.grades.append({"subject": subject, "score": score})

    def remove_grade(self, index):
        if 0 <= index < len(self.grades):
            self.grades.pop(index)

    def get_average(self):
        if not self.grades:
            return 0.0
        return sum(g["score"] for g in self.grades) / len(self.grades)

    def get_result(self):
        avg = self.get_average()
        if avg >= 90: return "ممتاز"
        elif avg >= 75: return "جيد جداً"
        elif avg >= 60: return "جيد"
        elif avg >= 50: return "مقبول"
        else: return "راسب"

    def to_dict(self):
        return {
            "name": self.name,
            "grades": self.grades,
            "average": round(self.get_average(), 1),
            "result": self.get_result()
        }


class GradeManager:
    def __init__(self):
        self.students = {}

    def add_student(self, name):
        if name in self.students:
            raise ValueError(f"الطالب '{name}' موجود مسبقاً")
        self.students[name] = Student(name)

    def delete_student(self, name):
        if name not in self.students:
            raise ValueError(f"الطالب '{name}' غير موجود")
        del self.students[name]

    def get_student(self, name):
        if name not in self.students:
            raise ValueError(f"الطالب '{name}' غير موجود")
        return self.students[name]

    def add_grade(self, name, subject, score):
        student = self.get_student(name)
        student.add_grade(subject, score)

    def remove_grade(self, name, index):
        student = self.get_student(name)
        student.remove_grade(index)

    def get_all(self):
        return {name: s.to_dict() for name, s in self.students.items()}

    def get_class_average(self):
        avgs = [s.get_average() for s in self.students.values() if s.grades]
        if not avgs:
            return None
        return round(sum(avgs) / len(avgs), 1)
