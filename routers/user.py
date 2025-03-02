from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import schemas, models, utils
from database import get_db


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user_dict = user.model_dump()
    user_dict["password"] = hashed_password
    new_user = models.User(**user_dict)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User {} not found".format(id))

    return user