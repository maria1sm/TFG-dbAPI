from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

load_dotenv()

azure_mysql_config = {
    "user": os.getenv("AZURE_MYSQL_USER"),
    "password": os.getenv("AZURE_MYSQL_PASSWORD"),
    "host": os.getenv("AZURE_MYSQL_HOST"),
    "port": os.getenv("AZURE_MYSQL_PORT"),
    "database": os.getenv("AZURE_MYSQL_DATABASE"),
}

# Construct the database URL
SQLALCHEMY_DATABASE_URL = (
    f"mysql+mysqlconnector://{azure_mysql_config['user']}:{azure_mysql_config['password']}"
    f"@{azure_mysql_config['host']}:{azure_mysql_config['port']}/{azure_mysql_config['database']}"
)

# Add SSL parameters
ssl_args = {
    "ssl_disabled": False,
}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=ssl_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


