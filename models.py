from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship('Group', back_populates='students')

Group.students = relationship('Student', order_by=Student.id, back_populates='group')

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship('Teacher', back_populates='subjects')

Teacher.subjects = relationship('Subject', order_by=Subject.id, back_populates='teacher')

class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    grade = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    student = relationship('Student', back_populates='grades')
    subject = relationship('Subject', back_populates='grades')

Student.grades = relationship('Grade', order_by=Grade.id, back_populates='student')
Subject.grades = relationship('Grade', order_by=Grade.id, back_populates='subject')
