from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Numeric, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from faker import Faker
import os 

# Define a PostgreSQL connection string

if os.path.exists("my_db.db"):
    os.remove("my_db.db")

# username = "postgre"
# password = "password"
# hostname = "localhost" 
# name db = "mydatabase"
pg8000engine = create_engine("postgresql+pg8000://postgre:password@localhost/mydatabase", echo=True)


# DEFINE TABLES MODELS


# SET UP FAKER


# INSERT DATA FOR EACH TABLE WITH FAKER



# CLOSE SESSION

