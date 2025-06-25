from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship  
import os 

# Delete the database file if exists (for dev/testing)
if os.path.exists("my_database.db"):
    os.remove("my_database.db")

engine = create_engine('sqlite:///my_database.db', echo=True)

Base = declarative_base()

class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

    things = relationship('Thing', back_populates='person')

class Thing(Base):
    __tablename__ = 'things'
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    value = Column(Float)
    owner_id = Column(Integer, ForeignKey('people.id'))
    
    person = relationship('Person', back_populates='things')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Create a person
new_person = Person(name='Sam', age=20)

# Add person to session
session.add(new_person)
session.commit()

# Create a thing for Sam
new_thing = Thing(description='Laptop', value=1200.0, person=new_person)

session.add(new_thing)
session.commit()