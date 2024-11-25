import random

from connect import session
from my_select import *


def get_random_entry(model):
    """Helper function to get a random entry from a table."""
    entries = session.query(model).all()
    return random.choice(entries) if entries else None


def test_select_queries():
    print("Running tests...")
    # get random entries from tables to run the tests
    subject = get_random_entry(Subject)
    teacher = get_random_entry(Teacher)
    group = get_random_entry(Group)
    student = get_random_entry(Student)

    print("1: Top 5 students with the highest average grade")
    top_students = select_1(session)
    print(top_students)

    print("\n2: Student with the highest average grade in a specific subject")
    if subject:
        top_student_in_subject = select_2(session, subject.id)
        print(f"Subject: {subject.name}, Result:", top_student_in_subject)

    print("\n3: Average grade in groups for a specific subject")
    if subject:
        avg_group_grades = select_3(session, subject.id)
        print(f"Subject: {subject.name}, Result:", avg_group_grades)

    print("\n4: Average grade for the entire stream (avg of all grades in the table)")
    avg_stream_grade = select_4(session)
    print(avg_stream_grade)

    print("\n5: Courses taught by a specific teacher")
    if teacher:
        teacher_courses = select_5(session, teacher.id)
        print(f"Teacher: {teacher.name}, Result:", teacher_courses)

    print("\n6: List of students in a specific group")
    if group:
        group_students = select_6(session, group.id)
        print(f"Group: {group.name}, Result:", group_students)

    print("\n7: Grades of students in a specific group for a specific subject")
    if group and subject:
        group_subject_grades = select_7(session, group.id, subject.id)
        print(f"Group: {group.name}, Subject: {subject.name}, Result:", group_subject_grades)

    print("\n8: Average grade given by a specific teacher for their subjects")
    if teacher:
        avg_teacher_grades = select_8(session, teacher.id)
        print(f"Teacher: {teacher.name}, Result:", avg_teacher_grades)

    print("\n9: Courses attended by a specific student")
    if student:
        student_courses = select_9(session, student.id)
        print(f"Student: {student.name}, Result:", student_courses)

    print("\n10: Courses taught by a specific teacher to a specific student")
    if teacher and student:
        teacher_student_courses = select_10(session, teacher.id, student.id)
        print(f"Teacher: {teacher.name}, Student: {student.name}, Result:", teacher_student_courses)

    session.close()
    print("\nAll tests completed.")


if __name__ == "__main__":
    test_select_queries()
