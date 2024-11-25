from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship, DeclarativeBase

class Base(DeclarativeBase):
    pass

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<Group(id={self.id}, name='{self.name}')>"

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship('Group', back_populates='students')

    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.name}', group_id={self.group_id})>"

Group.students = relationship('Student', order_by=Student.id, back_populates='group')

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<Teacher(id={self.id}, name='{self.name}')>"

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship('Teacher', back_populates='subjects')

    def __repr__(self):
        return f"<Subject(id={self.id}, name='{self.name}', teacher_id={self.teacher_id})>"

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

    def __repr__(self):
        return (
            f"<Grade(id={self.id}, student_id={self.student_id}, "
            f"subject_id={self.subject_id}, grade={self.grade}, date={self.date})>"
        )

Student.grades = relationship('Grade', order_by=Grade.id, back_populates='student')
Subject.grades = relationship('Grade', order_by=Grade.id, back_populates='subject')
