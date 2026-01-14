from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASE_URL = "postgresql://postgres:anika19@localhost:5432/loginapp"
engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()