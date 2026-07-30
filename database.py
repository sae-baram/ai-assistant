import os
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv

load_dotenv()


def get_database():
  
    db_uri = os.getenv("DATABASE_URI", "sqlite:///company.db")

    return SQLDatabase.from_uri(
        db_uri
    )