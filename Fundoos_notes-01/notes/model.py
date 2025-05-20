from sqlalchemy import Column , Integer , String , ForeignKey , Table
from sqlalchemy.orm import relationship
from db.database import Base

note_label = Table(
    'note_label',
    Base.metadata,
    Column('note_id' , Integer , ForeignKey('notes.id')),
    Column('label_id' , Integer , ForeignKey('labels.id'))
)

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer , primary_key = True , index = True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer , ForeignKey("user.id"))

    owner = relationship("User" , back_populates = "notes")
    labels = relationship("Label" , secondary = note_label , back_populates = "notes")