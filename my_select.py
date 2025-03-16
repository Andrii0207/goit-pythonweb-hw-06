from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from config import engine
from models import Student, Teacher, Subject, Grade, Group  # припускаю, що ваші моделі у файлі `models.py`

Session = sessionmaker(bind=engine)

def select_1():
    session = Session()
    try:
        top_5_students = session.query(
            Student.name,
            func.avg(Grade.grade).label('avg_grade')
        ).join(Grade).group_by(Student.id).order_by(func.avg(Grade.grade).desc()).limit(5).all()

        return [student.name for student in top_5_students]
    finally:
        session.close()

def select_2(subject_id):
    session = Session()
    try:
        best_student = session.query(
            Student.name,
            func.avg(Grade.grade).label('avg_grade')
        ).join(Grade).filter(Grade.subject_id == subject_id).group_by(Student.id).order_by(func.avg(Grade.grade).desc()).first()

        return best_student.name if best_student else None
    finally:
        session.close()

def select_3(subject_id):
    session = Session()
    try:
        avg_grade_by_group = session.query(
            Group.name,
            func.avg(Grade.grade).label('avg_grade')
        ).select_from(Group).join(Student).join(Grade).filter(Grade.subject_id == subject_id).group_by(Group.id).all()

        return {group.name: group.avg_grade for group in avg_grade_by_group}
    finally:
        session.close()

def select_4():
    session = Session()
    try:
        avg_grade_all = session.query(
            func.avg(Grade.grade).label('avg_grade')
        ).all()

        return avg_grade_all[0].avg_grade if avg_grade_all else None
    finally:
        session.close()

def select_5(teacher_id):
    session = Session()
    try:
        courses = session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()
        return [course.name for course in courses]
    finally:
        session.close()

def select_6(group_id):
    session = Session()
    try:
        students_in_group = session.query(Student.name).filter(Student.group_id == group_id).all()
        return [student.name for student in students_in_group]
    finally:
        session.close()

def select_7(group_id, subject_id):
    session = Session()
    try:
        grades_in_group_subject = session.query(
            Student.name,
            Grade.grade
        ).join(Grade).filter(Student.group_id == group_id, Grade.subject_id == subject_id).all()

        return [(grade.name, grade.grade) for grade in grades_in_group_subject]
    finally:
        session.close()

def select_8(teacher_id):
    session = Session()
    try:
        avg_grades_by_teacher = session.query(
            func.avg(Grade.grade).label('avg_grade')
        ).join(Subject).filter(Subject.teacher_id == teacher_id).all()

        return avg_grades_by_teacher[0].avg_grade if avg_grades_by_teacher else None
    finally:
        session.close()

def select_9(student_id):
    session = Session()
    try:
        courses_by_student = session.query(Subject.name).join(Grade).filter(Grade.student_id == student_id).all()
        return [course.name for course in courses_by_student]
    finally:
        session.close()

def select_10(student_id, teacher_id):
    session = Session()
    try:
        courses_by_student_teacher = session.query(Subject.name).join(Grade).filter(
            Grade.student_id == student_id,
            Subject.teacher_id == teacher_id
        ).all()

        return [course.name for course in courses_by_student_teacher]
    finally:
        session.close()

if __name__ == "__main__":
    print("1)  Топ 5 студентів з найвищим середнім балом:", select_1())
    print("2)  Студент з найвищим балом з предмета (ID=2):", select_2(2))
    print("3)  Середній бал у групах з предмета (ID=3):", select_3(3))
    print("4)  Середній бал на потоці:", select_4())
    print("5)  Курси, які читає викладач (ID=1):", select_5(1))
    print("6)  Студенти у групі (ID=1):", select_6(1))
    print("7)  Оцінки студентів у групі (ID=1) з предмета (ID=2):", select_7(1, 2))
    print("8)  Середній бал, який ставить викладач (ID=1):", select_8(1))
    print("9)  Курси, які відвідує студент (ID=1):", select_9(1))
    print("10) Курси, які студенту (ID=1) читає викладач (ID=1):", select_10(1, 1))
