from fastapi import APIRouter , Depends , HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from notes import model as note_model , schema as note_schema
from user import model as user_model
from label import model as label_model

router = APIRouter(prefix = "/notes" , tags = ["Notes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/" , response_model = note_schema.NoteResponse)
def create_note(note: note_schema.NoteCreate , user_id: int , db: Session = Depends(get_db)):
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code = 404 , detail = "User Not Found")
    
    new_note = note_model.Note(title = note.title , content = note.content , user_id = user_id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.get("/", response_model = list[note_schema.NoteResponse])
def get_all_notes(user_id: int , db: Session = Depends(get_db)):
    return db.query(note_model.Note).filter(note_model.Note.user_id == user_id).all()

@router.put("/{note_id}" , response_model = note_schema.NoteResponse)
def update_note(note_id: int , note: note_schema.NoteCreate , db: Session = Depends(get_db)):
    db_note = db.query(note_model.Note).filter(note_model.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code = 404 , detail = "Note not Found...")
    db_note.title = note.title
    db_note.content = note.content
    db.commit()
    db.refresh(db_note)
    return db_note

@router.delete("/{note_id}")
def delete_note(note_id: int , db: Session = Depends(get_db)):
    db_note = db.query(note_model.Note).filter(note_model.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code = 404 , detail = "Note  not found ....")
    db.delete(db_note)
    db.commit()
    return {"message" : "Note Deleted Successfully"}
