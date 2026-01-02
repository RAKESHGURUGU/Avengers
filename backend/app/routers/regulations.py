from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/regulations",
    tags=["regulations"]
)

@router.get("/", response_model=list[schemas.Regulation])
def read_regulations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    regulations = crud.get_regulations(db, skip=skip, limit=limit)
    return regulations

@router.get("/{regulation_id}", response_model=schemas.Regulation)
def read_regulation(regulation_id: int, db: Session = Depends(get_db)):
    db_regulation = crud.get_regulation(db, regulation_id=regulation_id)
    if db_regulation is None:
        raise HTTPException(status_code=404, detail="Regulation not found")
    return db_regulation

@router.post("/", response_model=schemas.Regulation)
def create_regulation(regulation: schemas.RegulationCreate, db: Session = Depends(get_db)):
    return crud.create_regulation(db=db, regulation=regulation)

@router.put("/{regulation_id}", response_model=schemas.Regulation)
def update_regulation(regulation_id: int, regulation: schemas.RegulationCreate, db: Session = Depends(get_db)):
    db_regulation = crud.update_regulation(db, regulation_id=regulation_id, regulation=regulation)
    if db_regulation is None:
        raise HTTPException(status_code=404, detail="Regulation not found")
    return db_regulation

@router.delete("/{regulation_id}")
def delete_regulation(regulation_id: int, db: Session = Depends(get_db)):
    db_regulation = crud.delete_regulation(db, regulation_id=regulation_id)
    if db_regulation is None:
        raise HTTPException(status_code=404, detail="Regulation not found")
    return {"message": "Regulation deleted successfully"}