from sqlmodel import Session
from .database import engine

class BaseUnitOfWork:
    
    def __init__(self):
        self.session = None

    def __enter__(self):
        self.session = Session(engine, expire_on_commit=False)
        return self

    def __exit__(self, exc_type, *args):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()
