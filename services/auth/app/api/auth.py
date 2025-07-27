from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models, db
from app.security import hash_pw, verify_pw, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, session: Session = Depends(db.get_db)):
    hashed = hash_pw(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed,
        role_id=user.role_id
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(db.get_db)):
    user = session.query(models.User).filter_by(username=form_data.username).first()
    if not user or not verify_pw(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user.username, "role": user.role.name})
    return {"access_token": token, "token_type": "bearer"}
