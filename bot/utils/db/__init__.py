from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import keys
from .models import Base, User, Chat


class Database:
    def __init__(self):
        engine = create_engine(keys.db_url)
        self.session = sessionmaker(bind=engine)()