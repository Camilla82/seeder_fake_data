from sqlalchemy import create_engine as sqlalchemy_create_engine
from sqlalchemy.exc import SQLAlchemyError

# username = "postgre"
# password = "password"
# hostname = "localhost" 
# name db = "mydatabase"

def init_engine(db_url="postgresql+pg8000://postgres:password@localhost/mydatabase", echo=True):
    try:
        return sqlalchemy_create_engine(db_url, echo=echo)
    except SQLAlchemyError as e:
        print("Failed to create engine:", e)
        raise