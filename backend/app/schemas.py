from pydantic import BaseModel
from typing import Optional

# Program schemas
class ProgramBase(BaseModel):
    name: str

class ProgramCreate(ProgramBase):
    pass

class Program(ProgramBase):
    id: int
    status: bool

    class Config:
        from_attributes = True

# Branch schemas
class BranchBase(BaseModel):
    name: str
    code: str

class BranchCreate(BranchBase):
    pass

class Branch(BranchBase):
    id: int
    status: bool

    class Config:
        from_attributes = True

# Regulation schemas
class RegulationBase(BaseModel):
    name: str

class RegulationCreate(RegulationBase):
    pass

class Regulation(RegulationBase):
    id: int
    status: bool

    class Config:
        from_attributes = True

# Program-Branch Mapping
class ProgramBranchMappingBase(BaseModel):
    program_id: int
    branch_id: int

class ProgramBranchMappingCreate(ProgramBranchMappingBase):
    pass

class ProgramBranchMapping(ProgramBranchMappingBase):
    id: int
    status: bool

    class Config:
        from_attributes = True

# Course schemas
class CourseBase(BaseModel):
    name: str
    code: str
    branch_id: int
    regulation_id: int
    year: str
    semester: str
    course_type: str
    elective_type: str
    credits: float

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    status: bool

    class Config:
        from_attributes = True

# Branch-Course Mapping
class BranchCourseMappingBase(BaseModel):
    branch_id: int
    course_id: int
    program_branch_mapping_id: int
    regulation_id: int

class BranchCourseMappingCreate(BranchCourseMappingBase):
    pass

class BranchCourseMapping(BranchCourseMappingBase):
    id: int
    status: bool

    class Config:
        from_attributes = True

# Faculty schemas
class FacultyBase(BaseModel):
    user_type: str
    branch_id: Optional[int] = None
    honorific: str
    name: str
    empid: str
    phone: str
    email: str
    password_hash: str

class FacultyCreate(FacultyBase):
    pass

class Faculty(FacultyBase):
    id: int
    status: bool

    class Config:
        from_attributes = True

# Faculty-Course Mapping
class FacultyCourseMappingBase(BaseModel):
    faculty_id: int
    course_id: int
    course_type: str
    year: str
    semester: str
    academic_year: str
    elective_type: str

class FacultyCourseMappingCreate(FacultyCourseMappingBase):
    pass

class FacultyCourseMapping(FacultyCourseMappingBase):
    id: int
    status: bool

    class Config:
        from_attributes = True

# Blooms Level
class BloomsLevelBase(BaseModel):
    name: str

class BloomsLevelCreate(BloomsLevelBase):
    pass

class BloomsLevel(BloomsLevelBase):
    id: int
    status: bool

    class Config:
        from_attributes = True

# Difficulty Level
class DifficultyLevelBase(BaseModel):
    name: str

class DifficultyLevelCreate(DifficultyLevelBase):
    pass

class DifficultyLevel(DifficultyLevelBase):
    id: int
    status: bool

    class Config:
        from_attributes = True

# Unit
class UnitBase(BaseModel):
    name: str

class UnitCreate(UnitBase):
    pass

class Unit(UnitBase):
    id: int
    status: bool

    class Config:
        from_attributes = True

# Course Outcome
class CourseOutcomeBase(BaseModel):
    course_id: int
    outcome_text: str

class CourseOutcomeCreate(CourseOutcomeBase):
    pass

class CourseOutcome(CourseOutcomeBase):
    id: int
    status: bool

    class Config:
        from_attributes = True

# Question
class QuestionBase(BaseModel):
    course_id: int
    co_id: int
    blooms_level_id: int
    difficulty_level_id: int
    unit_id: int
    question_text: str
    image: Optional[str] = None
    marks: float

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    status: bool

    class Config:
        from_attributes = True

# Generated QP
class GeneratedQPBase(BaseModel):
    program_id: int
    course_id: int
    assessment_type: str
    date_of_exam: str
    regulation_id: int
    year: str
    semester: str
    academic_year: str
    questions: str  # JSON string

class GeneratedQPCreate(GeneratedQPBase):
    pass

class GeneratedQP(GeneratedQPBase):
    id: int

    class Config:
        from_attributes = True