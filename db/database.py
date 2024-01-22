import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

# Get command-line arguments
if len(sys.argv) > 1:
    env_arg = sys.argv[1].upper()
    if env_arg not in ["DEVELOPMENT", "TESTING","PRODUCTION"]:
        raise ValueError("Invalid environment. Choose 'DEVELOPMENT' or 'TESTING' or 'PRODUCTION'.")
else:
    env_arg = "DEVELOPMENT"

# Load environment based on the provided command-line argument or default to "DEVELOPMENT"
env = os.getenv("ENV", env_arg)
print(f"Service running in {env} Mode")
if env == "DEVELOPMENT":
    load_dotenv(".env.development")
elif env == "TESTING":
    load_dotenv(".env.testing")
elif env == "PRODUCTION":
    load_dotenv(".env.production")
else:
    raise ValueError("Invalid environment. Choose 'DEVELOPMENT' or 'TESTING' or 'PRODUCTION'.")

sql_url = os.getenv("SQLALCHEMY_DATABASE_URL") + os.getenv("Userid")+":"+os.getenv("Password") + "@" + os.getenv("Host") + "/" + os.getenv("DB")
#sql_url = "mysql+mysqlconnector://root:Falca123@localhost/schemes_input"

engine = create_engine(sql_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()