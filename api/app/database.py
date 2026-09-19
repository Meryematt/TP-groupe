from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:0101@localhost:5432/postgres"
 
engine = create_engine(DATABASE_URL)
 
SessionLocal = sessionmaker(bind=engine, autocommit=False)
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    

