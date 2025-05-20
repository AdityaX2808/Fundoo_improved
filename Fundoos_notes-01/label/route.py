from fastapi import APIRouter , Depends , HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from label import model as label_model , schema as label_schema
from notes import model as note_model
from typing import List

router = APIRouter(prefix = "/labels" , tags = ["Labels"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model = label_schema.LabelResponse)
def create_label(label: label_schema.LabelCreate , db: Session = Depends(get_db)):
    new_label = label_model.Label(name = label.name)
    db.add(new_label)
    db.commit()
    db.refresh(new_label)
    return new_label

@router.put("/{label_id}" , response_model = label_schema.LabelResponse)
def update_label(label_id: int , label: label_schema.LabelCreate , db: Session = Depends(get_db)):
    db_label = db.query(label_model.Label).filter(label_model.Label.id == label_id).first()
    if not db_label:
        raise HTTPException(status_code = 404 , detail = "Label not found ....")
    db_label.name = label.name
    db.commit()
    db.refresh(db_label)
    return db_label

@router.delete("/{label_id}")
def delete_label(label_id: int , db: Session = Depends(get_db)):
    db_label = db.query(label_model.Label).filter(label_model.Label.id == label_id).first()
    if not db_label:
        raise HTTPException(status_code = 404 , detail = "Label not found..... ")
    db.delete(db_label)
    db.commit()
    return {"message" : "Label deleted Successfully"}

@router.post("/assign/")
def assign_label_to_note(note_id: int , label_id: int , db: Session = Depends(get_db)):
    note = db.query(note_model.Note).filter(note_model.Note.id == note_id).first()
    label = db.query(label_model.Label).filter(label_model.Label.id == label_id).first()

    if not note or not label:
        raise HTTPException(status_code = 404 , detail = "Note or Label not found.....")
    
    note.labels.append(label)
    db.commit()
    return {"message" : "Label assigned to note"}

@router.get("/", response_model=List[label_schema.LabelResponse])
def get_all_labels(db: Session = Depends(get_db)):
    labels = db.query(label_model.Label).all()
    return labels
