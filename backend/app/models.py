from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from .database import Base

# Programs table
class Program(Base):
    __tablename__ = 'programs'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    status = Column(Boolean, default=True)  # True for active, False for inactive

# Branches table
class Branch(Base):
    __tablename__ = 'branches'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(10), unique=True, nullable=False)
    status = Column(Boolean, default=True)

# Regulations table
class Regulation(Base):
    __tablename__ = 'regulations'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    status = Column(Boolean, default=True)

# Program-Branch Mapping
class ProgramBranchMapping(Base):
    __tablename__ = 'program_branch_mappings'
    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey('programs.id'), nullable=False)
    branch_id = Column(Integer, ForeignKey('branches.id'), nullable=False)
    status = Column(Boolean, default=True)

    program = relationship("Program")
    branch = relationship("Branch")

# Courses table
class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    branch_id = Column(Integer, ForeignKey('branches.id'), nullable=False)
    regulation_id = Column(Integer, ForeignKey('regulations.id'), nullable=False)
    year = Column(String(10), nullable=False)  # I, II, III, IV
    semester = Column(String(5), nullable=False)  # I, II
    course_type = Column(String(50), nullable=False)  # Theory, Lab, Project
    elective_type = Column(String(50), nullable=False)  # CORE, Professional Elective, Open Elective
    credits = Column(Float, nullable=False)
    status = Column(Boolean, default=True)

    branch = relationship("Branch")
    regulation = relationship("Regulation")

# Branch-Course Mapping
class BranchCourseMapping(Base):
    __tablename__ = 'branch_course_mappings'
    id = Column(Integer, primary_key=True, index=True)
    branch_id = Column(Integer, ForeignKey('branches.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    program_branch_mapping_id = Column(Integer, ForeignKey('program_branch_mappings.id'), nullable=False)
    regulation_id = Column(Integer, ForeignKey('regulations.id'), nullable=False)
    status = Column(Boolean, default=True)

    branch = relationship("Branch")
    course = relationship("Course")
    program_branch_mapping = relationship("ProgramBranchMapping")
    regulation = relationship("Regulation")

# Faculties table
class Faculty(Base):
    __tablename__ = 'faculties'
    id = Column(Integer, primary_key=True, index=True)
    user_type = Column(String(20), nullable=False)  # Admin or Faculty
    branch_id = Column(Integer, ForeignKey('branches.id'), nullable=True)
    honorific = Column(String(10), nullable=False)  # Dr., Mr., Mrs.
    name = Column(String(100), nullable=False)
    empid = Column(String(20), unique=True, nullable=False)
    phone = Column(String(15), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    status = Column(Boolean, default=True)

    branch = relationship("Branch")

# Faculty-Course Mapping
class FacultyCourseMapping(Base):
    __tablename__ = 'faculty_course_mappings'
    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey('faculties.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    course_type = Column(String(50), nullable=False)
    year = Column(String(10), nullable=False)
    semester = Column(String(5), nullable=False)
    academic_year = Column(String(20), nullable=False)  # e.g., 2025-2026
    elective_type = Column(String(50), nullable=False)
    status = Column(Boolean, default=True)

    faculty = relationship("Faculty")
    course = relationship("Course")

# Bloom’s Levels
class BloomsLevel(Base):
    __tablename__ = 'blooms_levels'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    status = Column(Boolean, default=True)

# Difficulty Levels
class DifficultyLevel(Base):
    __tablename__ = 'difficulty_levels'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    status = Column(Boolean, default=True)

# Units
class Unit(Base):
    __tablename__ = 'units'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    status = Column(Boolean, default=True)

# Course Outcomes
class CourseOutcome(Base):
    __tablename__ = 'course_outcomes'
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    outcome_text = Column(Text, nullable=False)
    status = Column(Boolean, default=True)

    course = relationship("Course")

# Questions
class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    co_id = Column(Integer, ForeignKey('course_outcomes.id'), nullable=False)
    blooms_level_id = Column(Integer, ForeignKey('blooms_levels.id'), nullable=False)
    difficulty_level_id = Column(Integer, ForeignKey('difficulty_levels.id'), nullable=False)
    unit_id = Column(Integer, ForeignKey('units.id'), nullable=False)
    question_text = Column(Text, nullable=False)
    image = Column(String(255), nullable=True)  # Path to image if any
    marks = Column(Float, nullable=False)
    status = Column(Boolean, default=True)

    course = relationship("Course")
    course_outcome = relationship("CourseOutcome")
    blooms_level = relationship("BloomsLevel")
    difficulty_level = relationship("DifficultyLevel")
    unit = relationship("Unit")

# Optional: Generated Question Papers
class GeneratedQP(Base):
    __tablename__ = 'generated_qps'
    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey('programs.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    assessment_type = Column(String(50), nullable=False)  # MID-1, MID-2, Regular, Supply
    date_of_exam = Column(String(20), nullable=False)
    regulation_id = Column(Integer, ForeignKey('regulations.id'), nullable=False)
    year = Column(String(10), nullable=False)
    semester = Column(String(5), nullable=False)
    academic_year = Column(String(20), nullable=False)
    questions = Column(Text, nullable=False)  # JSON or text of selected questions
    created_at = Column(String(20), nullable=False)

    program = relationship("Program")
    course = relationship("Course")
    regulation = relationship("Regulation")