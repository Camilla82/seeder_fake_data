from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session
import sqlite3 
from faker import Faker
import os 

# Remove old database file (only if it exists)
if os.path.exists("my_database.db"):
    os.remove("my_database.db")


Base = declarative_base()

# Person table
class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

    # Relationship: one person has many pets
    pets = relationship("Pet", back_populates="owner")

# Pet table
class Pet(Base):
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    owner_id = Column(Integer, ForeignKey('people.id'))

    # Relationship: pet belongs to one owner
    owner = relationship("Person", back_populates="pets")

# Create engine and tables
engine = create_engine('sqlite:///my_database.db', echo=True)
Base.metadata.create_all(engine)

# Insert data
with Session(engine) as session:
    person1 = Person(name="Alice", age=30)
    person2 = Person(name="Bob", age=40)

    pet1 = Pet(name="Fluffy", type="Cat", owner=person1)
    pet2 = Pet(name="Rex", type="Dog", owner=person1)
    pet3 = Pet(name="Goldie", type="Fish", owner=person2)

    session.add_all([person1, person2, pet1, pet2, pet3])
    session.commit()

with Session(engine) as session:
    # Query a person and print their pets
    alice = session.query(Person).filter_by(name="Alice").first()
    print(f"{alice.name} owns:")
    for pet in alice.pets:
        print(f"- {pet.name} ({pet.type})")