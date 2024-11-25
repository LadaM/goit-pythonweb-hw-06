from sqlalchemy import func
from sqlalchemy.orm import Session
from models import Student, Grade, Subject, Teacher, Group


# 1. Find 5 students with the highest average grade across all subjects
def select_1(session: Session):
    result = (
        session.query(Student.name, func.avg(Grade.grade).label('average_grade'))
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )
    return result


# 2. Find the student with the highest average grade in a specific subject
def select_2(session: Session, subject_id: int):
    result = (
        session.query(Student.name, func.avg(Grade.grade).label('average_grade'))
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )
    return result


# 3. Find the average grade in groups for a specific subject
def select_3(session: Session, subject_id: int):
    result = (
        session.query(Group.name, func.avg(Grade.grade).label('average_grade'))
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .all()
    )
    return result


# 4. Find the average grade for the entire stream (all grades in the table)
def select_4(session: Session):
    result = session.query(func.avg(Grade.grade).label('average_grade')).scalar()
    return result


# 5. Find which courses a specific teacher teaches
def select_5(session: Session, teacher_id: int):
    result = (
        session.query(Subject.name)
        .filter(Subject.teacher_id == teacher_id)
        .all()
    )
    return result


# 6. Find the list of students in a specific group
def select_6(session: Session, group_id: int):
    result = (
        session.query(Student.name)
        .filter(Student.group_id == group_id)
        .all()
    )
    return result


# 7. Find the grades of students in a specific group for a specific subject
def select_7(session: Session, group_id: int, subject_id: int):
    result = (
        session.query(Student.name, Grade.grade)
        .join(Grade)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .all()
    )
    return result


# 8. Find the average grade given by a specific teacher for their subjects
def select_8(session: Session, teacher_id: int):
    result = (
        session.query(func.avg(Grade.grade).label('average_grade'))
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Subject.teacher_id == teacher_id)
        .scalar()
    )
    return result


# 9. Find the list of courses attended by a specific student
def select_9(session: Session, student_id: int):
    result = (
        session.query(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id)
        .distinct()
        .all()
    )
    return result


# 10. Find the list of courses taught by a specific teacher to a specific student
def select_10(session: Session, teacher_id: int, student_id: int):
    result = (
        session.query(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .distinct()
        .all()
    )
    return result
