from sqlalchemy import create_engine, text
import sqlite3 
from sqlalchemy.orm import Session 
from faker import Faker

# Initialize Faker
fake = Faker()

# use engine to connect database 

engine = create_engine('sqlite:///my_database.db', echo=True)

conn = engine.connect() # connection obj

# create db
conn.execute(text("CREATE TABLE IF NOT EXISTS people (name str, age int)"))

conn.commit() # commit changes 

#sessions

session = Session(engine) # starting session with this database

# generate one row of fake data
session.execute(text('INSERT INTO PEOPLE(name, age) VALUES("Camilla", 42);'))

# Generate and insert fake data
for _ in range(10):  # insert 10 fake records
    name = fake.unique.name()
    age = fake.random_int(min=18, max=80)
    session.execute(text("INSERT INTO people (name, age) VALUES (:name, :age)"),
                    {"name": name, "age": age})

session.commit()

