import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

SUPABASE_CON = os.environ.get("SUPABASE_CON")

if not SUPABASE_CON:
    raise ValueError("Environment variables must be set...")

engine = create_engine(
    SUPABASE_CON
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()