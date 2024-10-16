from app.core.db import Base, engine
from .services.users.models import *

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()