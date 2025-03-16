import random
from faker import Faker

from config import engine, SessionLocal
from models import Student, Group, Teacher, Subject, Grade

fake = Faker()


def seed_db():
    session = SessionLocal()

    groups = [Group(name=f"Group {i}") for i in range(1, 3)]
    session.add_all(groups)
    session.commit()

    teachers = [Teacher(name=fake.name()) for _ in range(5)]
    session.add_all(teachers)
    session.commit()

    subjects = [Subject(name=fake.word(), teacher=random.choice(teachers)) for _ in range(10)]
    session.add_all(subjects)
    session.commit()

    students = [Student(name=fake.name(), group=random.choice(groups)) for _ in range(20)]
    session.add_all(students)
    session.commit()

    for student in students:
        for _ in range(20):
            grade = Grade(
                student=student,
                subject=random.choice(subjects),
                grade=random.randint(60, 100)
            )
            session.add(grade)

    session.commit()
    session.close()


if __name__ == "__main__":
    seed_db()