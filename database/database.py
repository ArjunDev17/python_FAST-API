# database/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Replace 'mysql+mysqlconnector://username:password@localhost/dbname' with your MySQL connection string
DATABASE_URL = "mysql+mysqlconnector://root:Falca$123@localhost/mysm"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
