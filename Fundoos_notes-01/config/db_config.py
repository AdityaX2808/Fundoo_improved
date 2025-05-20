import os
from dotenv import load_dotenv

load_dotenv()

class DB_Settings:
    DB_PASSWORD = os.getenv('DB_PASSWORD','Aditya%4015425')
    DB_USERNAME = os.getenv('DB_USERNAME','postgres')
    DB_HOST = os.getenv('DB_HOST','localhost')
    DB_PORT = os.getenv('DB_PORT','5432')
    DB_NAME = os.getenv('DB_NAME','TestDB')

settings = DB_Settings()

DATABASE_URL = f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
