from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use environment variables for secrets (never hardcode in repo)
import os
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("DB_IP")
port = os.getenv("POSTGRES_PORT")
db_name = os.getenv("POSTGRES_DB")
DATABASE_URL = f"postgresql://{postgres_user}:{postgres_password}@{db_host}:{port}/{db_name}"

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=10,            # number of persistent connections
    max_overflow=5,          # extra connections allowed beyond pool_size
    pool_timeout=30,         # seconds to wait before failing
    pool_recycle=1800,       # recycle connections every 30 minutes
    echo=False               # set True for SQL debug logging
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency function ()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
