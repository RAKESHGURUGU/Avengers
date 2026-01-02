from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import SessionLocal
from ..auth import verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    username = credentials.username
    password = credentials.password

    faculty = db.query(models.Faculty).filter(models.Faculty.username == username).first()

    if not faculty or not verify_password(password, faculty.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return {"message": "Login successful", "user": {"id": faculty.id, "name": faculty.name, "role": faculty.user_type}}
def get_all_users(db: Session = Depends(get_db)):
    faculties = db.query(models.Faculty).all()
    return [{"id": f.id, "name": f.name, "email": f.email, "user_type": f.user_type, "empid": f.empid} for f in faculties]