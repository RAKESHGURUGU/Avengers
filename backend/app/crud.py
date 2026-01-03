from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

# Programs
def get_programs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Program).offset(skip).limit(limit).all()

def get_program(db: Session, program_id: int):
    return db.query(models.Program).filter(models.Program.id == program_id).first()

def create_program(db: Session, program: schemas.ProgramCreate):
    db_program = models.Program(**program.dict())
    db.add(db_program)
    db.commit()
    db.refresh(db_program)
    return db_program

def update_program(db: Session, program_id: int, program: schemas.ProgramUpdate):
    db_program = db.query(models.Program).filter(models.Program.id == program_id).first()
    if db_program:
        update_data = program.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_program, key, value)
        db.commit()
        db.refresh(db_program)
    return db_program

def delete_program(db: Session, program_id: int):
    db_program = db.query(models.Program).filter(models.Program.id == program_id).first()
    if db_program:
        db.delete(db_program)
        db.commit()
    return db_program

# Branches
def get_branches(db: Session, skip: int = 0, limit: int = 100):
    branches = db.query(models.Branch).offset(skip).limit(limit).all()
    # Add program_name to each branch
    for branch in branches:
        mapping = db.query(models.ProgramBranchMapping).filter(models.ProgramBranchMapping.branch_id == branch.id).first()
        if mapping:
            program = db.query(models.Program).filter(models.Program.id == mapping.program_id).first()
            branch.program_name = program.name if program else None
    return branches

def get_branch(db: Session, branch_id: int):
    branch = db.query(models.Branch).filter(models.Branch.id == branch_id).first()
    if branch:
        mapping = db.query(models.ProgramBranchMapping).filter(models.ProgramBranchMapping.branch_id == branch.id).first()
        if mapping:
            program = db.query(models.Program).filter(models.Program.id == mapping.program_id).first()
            branch.program_name = program.name if program else None
    return branch

def create_branch(db: Session, branch: schemas.BranchCreate):
    # Extract program_id
    program_id = branch.program_id
    branch_data = branch.dict()
    del branch_data['program_id']
    
    db_branch = models.Branch(**branch_data)
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    
    # Create mapping
    mapping = schemas.ProgramBranchMappingCreate(program_id=program_id, branch_id=db_branch.id)
    create_program_branch_mapping(db, mapping)
    
    # Add program_name to response
    program = db.query(models.Program).filter(models.Program.id == program_id).first()
    db_branch.program_name = program.name if program else None
    
    return db_branch

def update_branch(db: Session, branch_id: int, branch: schemas.BranchCreate):
    db_branch = db.query(models.Branch).filter(models.Branch.id == branch_id).first()
    if db_branch:
        # Extract program_id
        program_id = branch.program_id
        branch_data = branch.dict()
        del branch_data['program_id']
        
        # Update branch fields
        for key, value in branch_data.items():
            setattr(db_branch, key, value)
        db.commit()
        db.refresh(db_branch)
        
        # Update mapping
        existing_mapping = db.query(models.ProgramBranchMapping).filter(models.ProgramBranchMapping.branch_id == branch_id).first()
        if existing_mapping:
            existing_mapping.program_id = program_id
            db.commit()
        else:
            # Create new mapping if not exists
            mapping = schemas.ProgramBranchMappingCreate(program_id=program_id, branch_id=branch_id)
            create_program_branch_mapping(db, mapping)
        
        # Add program_name
        program = db.query(models.Program).filter(models.Program.id == program_id).first()
        db_branch.program_name = program.name if program else None
    return db_branch

def delete_branch(db: Session, branch_id: int):
    db_branch = db.query(models.Branch).filter(models.Branch.id == branch_id).first()
    if db_branch:
        db.delete(db_branch)
        db.commit()
    return db_branch

# Regulations
def get_regulations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Regulation).offset(skip).limit(limit).all()

def get_regulation(db: Session, regulation_id: int):
    return db.query(models.Regulation).filter(models.Regulation.id == regulation_id).first()

def create_regulation(db: Session, regulation: schemas.RegulationCreate):
    db_regulation = models.Regulation(**regulation.dict())
    db.add(db_regulation)
    db.commit()
    db.refresh(db_regulation)
    return db_regulation

def update_regulation(db: Session, regulation_id: int, regulation: schemas.RegulationCreate):
    db_regulation = db.query(models.Regulation).filter(models.Regulation.id == regulation_id).first()
    if db_regulation:
        for key, value in regulation.dict().items():
            setattr(db_regulation, key, value)
        db.commit()
        db.refresh(db_regulation)
    return db_regulation

def delete_regulation(db: Session, regulation_id: int):
    db_regulation = db.query(models.Regulation).filter(models.Regulation.id == regulation_id).first()
    if db_regulation:
        db.delete(db_regulation)
        db.commit()
    return db_regulation

# Program-Branch Mappings
def get_program_branch_mappings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ProgramBranchMapping).offset(skip).limit(limit).all()

def create_program_branch_mapping(db: Session, mapping: schemas.ProgramBranchMappingCreate):
    db_mapping = models.ProgramBranchMapping(**mapping.dict())
    db.add(db_mapping)
    db.commit()
    db.refresh(db_mapping)
    return db_mapping

# Program-Branch Mappings
def get_program_branch_mappings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ProgramBranchMapping).offset(skip).limit(limit).all()

def create_program_branch_mapping(db: Session, mapping: schemas.ProgramBranchMappingCreate):
    db_mapping = models.ProgramBranchMapping(**mapping.dict())
    db.add(db_mapping)
    db.commit()
    db.refresh(db_mapping)
    return db_mapping

# Courses
def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Course).offset(skip).limit(limit).all()

def get_course(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()

def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def update_course(db: Session, course_id: int, course: schemas.CourseCreate):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if db_course:
        for key, value in course.dict().items():
            setattr(db_course, key, value)
        db.commit()
        db.refresh(db_course)
    return db_course

def delete_course(db: Session, course_id: int):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if db_course:
        db.delete(db_course)
        db.commit()
    return db_course

# Branch-Course Mappings
def get_branch_course_mappings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.BranchCourseMapping).offset(skip).limit(limit).all()

def create_branch_course_mapping(db: Session, mapping: schemas.BranchCourseMappingCreate):
    db_mapping = models.BranchCourseMapping(**mapping.dict())
    db.add(db_mapping)
    db.commit()
    db.refresh(db_mapping)
    return db_mapping

# Faculties
def get_faculties(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Faculty).offset(skip).limit(limit).all()

def get_faculty(db: Session, faculty_id: int):
    return db.query(models.Faculty).filter(models.Faculty.id == faculty_id).first()

def create_faculty(db: Session, faculty: schemas.FacultyCreate):
    db_faculty = models.Faculty(**faculty.dict())
    db.add(db_faculty)
    db.commit()
    db.refresh(db_faculty)
    return db_faculty

def update_faculty(db: Session, faculty_id: int, faculty: schemas.FacultyCreate):
    db_faculty = db.query(models.Faculty).filter(models.Faculty.id == faculty_id).first()
    if db_faculty:
        for key, value in faculty.dict().items():
            setattr(db_faculty, key, value)
        db.commit()
        db.refresh(db_faculty)
    return db_faculty

def delete_faculty(db: Session, faculty_id: int):
    db_faculty = db.query(models.Faculty).filter(models.Faculty.id == faculty_id).first()
    if db_faculty:
        db.delete(db_faculty)
        db.commit()
    return db_faculty

# Faculty-Course Mappings
def get_faculty_course_mappings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.FacultyCourseMapping).offset(skip).limit(limit).all()

def create_faculty_course_mapping(db: Session, mapping: schemas.FacultyCourseMappingCreate):
    db_mapping = models.FacultyCourseMapping(**mapping.dict())
    db.add(db_mapping)
    db.commit()
    db.refresh(db_mapping)
    return db_mapping

# Blooms Levels
def get_blooms_levels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.BloomsLevel).offset(skip).limit(limit).all()

def create_blooms_level(db: Session, level: schemas.BloomsLevelCreate):
    db_level = models.BloomsLevel(**level.dict())
    db.add(db_level)
    db.commit()
    db.refresh(db_level)
    return db_level

# Difficulty Levels
def get_difficulty_levels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DifficultyLevel).offset(skip).limit(limit).all()

def create_difficulty_level(db: Session, level: schemas.DifficultyLevelCreate):
    db_level = models.DifficultyLevel(**level.dict())
    db.add(db_level)
    db.commit()
    db.refresh(db_level)
    return db_level

# Units
def get_units(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Unit).offset(skip).limit(limit).all()

def create_unit(db: Session, unit: schemas.UnitCreate):
    db_unit = models.Unit(**unit.dict())
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit

# Course Outcomes
def get_course_outcomes(db: Session, course_id: int):
    return db.query(models.CourseOutcome).filter(models.CourseOutcome.course_id == course_id).all()

def create_course_outcome(db: Session, outcome: schemas.CourseOutcomeCreate):
    db_outcome = models.CourseOutcome(**outcome.dict())
    db.add(db_outcome)
    db.commit()
    db.refresh(db_outcome)
    return db_outcome

# Questions
def get_questions(db: Session, course_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Question).filter(models.Question.course_id == course_id).offset(skip).limit(limit).all()

def create_question(db: Session, question: schemas.QuestionCreate):
    db_question = models.Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

# Generated QPs
def get_generated_qps(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.GeneratedQP).offset(skip).limit(limit).all()

def create_generated_qp(db: Session, qp: schemas.GeneratedQPCreate):
    qp_data = qp.dict()
    # Ensure created_at is present; if not, set to current ISO timestamp
    if not qp_data.get('created_at'):
        qp_data['created_at'] = datetime.utcnow().isoformat()
    db_qp = models.GeneratedQP(**qp_data)
    db.add(db_qp)
    db.commit()
    db.refresh(db_qp)
    return db_qp