import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# RETTELSE: Opdateret til root-brugeren og port 5432
# DATABASE_URL = "postgresql://root:password@localhost:5432/tasks"
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://root:root@localhost:5432/tasks")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
  db = SessionLocal()
  try:
      yield db
  finally:
      db.close()
