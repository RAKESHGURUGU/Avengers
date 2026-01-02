from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/programs", tags=["programs"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.Program])
def read_programs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    programs = crud.get_programs(db, skip=skip, limit=limit)
    return programs

@router.get("/{program_id}", response_model=schemas.Program)
def read_program(program_id: int, db: Session = Depends(get_db)):
    db_program = crud.get_program(db, program_id=program_id)
    if db_program is None:
        raise HTTPException(status_code=404, detail="Program not found")
    return db_program

@router.post("/", response_model=schemas.Program)
def create_program(program: schemas.ProgramCreate, db: Session = Depends(get_db)):
    return crud.create_program(db=db, program=program)

@router.put("/{program_id}", response_model=schemas.Program)
def update_program(program_id: int, program: schemas.ProgramCreate, db: Session = Depends(get_db)):
    db_program = crud.update_program(db, program_id=program_id, program=program)
    if db_program is None:
        raise HTTPException(status_code=404, detail="Program not found")
    return db_program

@router.delete("/{program_id}")
def delete_program(program_id: int, db: Session = Depends(get_db)):
    db_program = crud.delete_program(db, program_id=program_id)
    if db_program is None:
        raise HTTPException(status_code=404, detail="Program not found")
    return {"message": "Program deleted"}