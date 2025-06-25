from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKey
import sqlite3 
from sqlalchemy.orm import Session 
from faker import Faker
import os 

# Remove old database file (only if it exists)
if os.path.exists("my_database.db"):
    os.remove("my_database.db")

engine = create_engine('sqlite:///my_database.db', echo=True) # engine creation and log SQL generated

meta = MetaData() #obj - keeps track of all the tables, columns, keys, etc.

people = Table(

    "people", #table name
    meta, # meta obj
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False), # required column, no null values
    Column('age', Integer)

)

things = Table(
    "things",
    meta,
    Column('id', Integer, primary_key=True),
    Column('description', String, nullable=False),
    Column('value', Float),
    Column('owner', Integer, ForeignKey('people.id'))

)

meta.create_all(engine)  # creates the table

conn = engine.connect()

insert_people = people.insert().values([
    {'name' : 'Mike', 'age': 30},
    {'name' : 'Camilla', 'age': 42},
    {'name' : 'Mark', 'age': 47},
    {'name' : 'Xin', 'age': 32},
    {'name' : 'Elisa', 'age': 43},
])

insert_things = things.insert().values([
    {'owner': 2, 'description': 'Laptop', 'value': 800},
    {'owner': 2, 'description': 'Mouse', 'value': 50.50},
    {'owner': 2, 'description': 'Keyboard', 'value': 100.50},
    {'owner': 3, 'description': 'Book', 'value': 40},
    {'owner': 4, 'description': 'Bottle', 'value': 11.23},
    {'owner': 5, 'description': 'Speaker', 'value': 87},
])

conn.execute(insert_people)
conn.commit()

conn.execute(insert_things)

conn.commit()