from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import crud, schemas, models
from .auth import get_password_hash

def populate_database():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Add Programs if not exist
        programs = ["B.Tech", "M.Tech", "MBA", "MCA"]
        for prog in programs:
            if not db.query(models.Program).filter(models.Program.name == prog).first():
                crud.create_program(db, schemas.ProgramCreate(name=prog))

        # Add Branches if not exist
        branches = [
            {"name": "Computer Science", "code": "CSE"},
            {"name": "Information Technology", "code": "IT"},
            {"name": "Electronics", "code": "ECE"}
        ]
        for branch in branches:
            if not db.query(models.Branch).filter(models.Branch.code == branch["code"]).first():
                crud.create_branch(db, schemas.BranchCreate(**branch))

        # Add Regulations if not exist
        regulations = ["AR23", "AR21", "AR20"]
        for reg in regulations:
            if not db.query(models.Regulation).filter(models.Regulation.name == reg).first():
                crud.create_regulation(db, schemas.RegulationCreate(name=reg))

        # Add Faculty if not exist
        if not db.query(models.Faculty).filter(models.Faculty.username == "rakesh").first():
            rakesh = schemas.FacultyCreate(
                user_type="Faculty",
                branch_id=1,
                honorific="Mr.",
                name="Rakesh",
                empid="FAC002",
                phone="1234567890",
                username="rakesh",
                email="rakesh@websaga.com",
                password_hash=get_password_hash("1234")
            )
            crud.create_faculty(db, rakesh)

        print("Database populated with sample data")
    finally:
        db.close()

if __name__ == "__main__":
    populate_database()