from fastapi import FastAPI
from db.database import Base , engine
from user import route as user_route
from notes import route as notes_route
from label import route as label_route

Base.metadata.create_all(bind = engine)

app = FastAPI()

app.include_router(user_route.router)
app.include_router(notes_route.router)
app.include_router(label_route.router)