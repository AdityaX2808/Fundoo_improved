from sqlalchemy import Column , Integer , String
from sqlalchemy.orm import relationship
from db.database import Base
from notes.model import note_label

class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer , primary_key = True , index = True)
    name = Column(String , unique = True)

    notes = relationship("Note" , secondary = note_label , back_populates = "labels")