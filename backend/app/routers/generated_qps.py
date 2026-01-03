from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/generated_qps", tags=["generated_qps"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.GeneratedQP)
def create_generated_qp(qp: schemas.GeneratedQPCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_generated_qp(db=db, qp=qp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[schemas.GeneratedQP])
def list_generated_qps(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        return crud.get_generated_qps(db=db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{qp_id}", response_model=schemas.GeneratedQP)
def get_generated_qp(qp_id: int, db: Session = Depends(get_db)):
    try:
        qp = crud.get_generated_qps(db=db, skip=0, limit=100)
        # crud doesn't have a single-get helper; use query via crud.get_generated_qps and filter
        for item in qp:
            if item.id == qp_id:
                return item
        raise HTTPException(status_code=404, detail="Generated QP not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
