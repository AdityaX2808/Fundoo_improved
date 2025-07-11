from sqlalchemy import Column , Integer , String
from sqlalchemy.orm import relationship
from db.database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer , primary_key = True , index = True)
    username = Column(String , unique = True , index = True , nullable = False)
    email = Column(String , unique = True , nullable = False)
    password = Column(String , nullable = False)

    notes = relationship("Note" , back_populates = "owner")