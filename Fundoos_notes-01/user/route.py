from fastapi import APIRouter , Depends , HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from user import schema , model
from passlib.context import CryptContext

router = APIRouter(prefix = "/user" , tags = ["User"])

pwd_context = CryptContext(schemes = ["bcrypt"] , deprecated = "auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register" , response_model = schema.UserResponse)
def  register(user: schema.UserCreate , db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = model.User(username = user.username , email = user.email , password = hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login(user: schema.UserLogin , db: Session = Depends(get_db)):
    db_user = db.query(model.User).filter(model.User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password , db_user.password):
        raise HTTPException(status_code = 400 , detail = "Invalid Credentials")
    return {"message" : "Login Successful"}

