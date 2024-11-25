import random

from faker import Faker
from sqlalchemy import text

from connect import session
from models import Group, Student, Teacher, Subject, Grade

fake = Faker()


def clear_tables():
    session.execute(text("TRUNCATE TABLE grades RESTART IDENTITY CASCADE;"))
    session.execute(text("TRUNCATE TABLE students RESTART IDENTITY CASCADE;"))
    session.execute(text("TRUNCATE TABLE subjects RESTART IDENTITY CASCADE;"))
    session.execute(text("TRUNCATE TABLE teachers RESTART IDENTITY CASCADE;"))
    session.execute(text("TRUNCATE TABLE groups RESTART IDENTITY CASCADE;"))
    session.commit()
    print("All tables cleared and IDs reset.")


def seed_groups():
    groups = [Group(name=f"Group {i + 1}") for i in range(3)]
    session.add_all(groups)
    session.commit()
    return groups


def seed_teachers():
    teachers = [Teacher(name=fake.name()) for _ in range(5)]
    session.add_all(teachers)
    session.commit()
    return teachers


def seed_subjects(teachers):
    # predefined subject names
    subject_names = [
        "Mathematics",
        "Physics",
        "Chemistry",
        "Biology",
        "History",
        "Literature",
        "Computer Science",
        "Philosophy",
        "Economics",
        "Geography"
    ]

    subjects = [
        Subject(name=name, teacher_id=random.choice(teachers).id)
        for name in subject_names
    ]
    session.add_all(subjects)
    session.commit()
    return subjects


def seed_students(groups):
    students = [
        Student(name=fake.name(), group_id=random.choice(groups).id) for _ in range(50)
    ]
    session.add_all(students)
    session.commit()
    return students


def seed_grades(students, subjects):
    grades = []
    for student in students:
        for subject in subjects:
            for _ in range(random.randint(5, 15)):
                grade = Grade(
                    student_id=student.id,
                    subject_id=subject.id,
                    grade=round(random.uniform(2, 5) / 0.25) * 0.25,  # Step of 0.25
                    date=fake.date_this_year()
                )
                grades.append(grade)
    session.add_all(grades)
    session.commit()
    print(f"{len(grades)} grades added.")


def seed_data():
    print("Seeding data...")
    clear_tables()

    groups = seed_groups()
    teachers = seed_teachers()
    subjects = seed_subjects(teachers)
    students = seed_students(groups)
    seed_grades(students, subjects)

    print("Seeding completed!")


if __name__ == "__main__":
    seed_data()
