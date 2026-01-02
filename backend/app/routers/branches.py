from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/branches", tags=["branches"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.Branch])
def read_branches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    branches = crud.get_branches(db, skip=skip, limit=limit)
    return branches

@router.get("/{branch_id}", response_model=schemas.Branch)
def read_branch(branch_id: int, db: Session = Depends(get_db)):
    db_branch = crud.get_branch(db, branch_id=branch_id)
    if db_branch is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    return db_branch

@router.post("/", response_model=schemas.Branch)
def create_branch(branch: schemas.BranchCreate, db: Session = Depends(get_db)):
    return crud.create_branch(db=db, branch=branch)

@router.put("/{branch_id}", response_model=schemas.Branch)
def update_branch(branch_id: int, branch: schemas.BranchCreate, db: Session = Depends(get_db)):
    db_branch = crud.update_branch(db, branch_id=branch_id, branch=branch)
    if db_branch is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    return db_branch

@router.delete("/{branch_id}")
def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    db_branch = crud.delete_branch(db, branch_id=branch_id)
    if db_branch is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    return {"message": "Branch deleted"}