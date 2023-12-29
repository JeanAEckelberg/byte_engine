from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = 'postgresql+psycopg2://byteuser:bytepassword@localhost:5432/byteserver'

engine = create_engine(
    DB_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
