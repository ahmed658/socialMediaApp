from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix = "/users",
    tags=["Users"]
)

@router.post("/", response_model=schemas.UserOut)
def add_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    user.password = utils.hashPassword(user.password)
    newUser = models.User(**user.model_dump())
    try:
        db.add(newUser)
        db.commit()
        db.refresh(newUser)
        return newUser
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{error}")
    
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} is not found!")
    return user