from src.utils import init_engine
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Numeric, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from faker import Faker
import os 
import random 

# Define a PostgreSQL connection string


if os.path.exists("my_db.db"):
        os.remove("my_db.db")

pg8000engine = init_engine() # see utils

# declarative models 
# SQLAlchemy generates the appropriate SQL
#https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/basic_use.html
# declarative_base Construct a base class for declarative class definitions.
# sales schema: 
Base = declarative_base() # all mapped classes should inherit this base class

# class SalesOrder(Base):
#     __tablename__ = 'sales_order'
#     pass

# class Counterparty(Base):
#     __tablename__ = 'counterparty'
#     pass

# class Currency(Base):
#     __tablename__ = 'currency'
#     pass

# class Date(Base):
#     __tablename__ = 'date'
#     pass

class Department(Base):
    __tablename__ = 'department'
    department_id = Column(Integer, primary_key=True)
    department_name = Column(String)
    
# class Design(Base):
#     __tablename__ = 'design'
#     pass

# class Location(Base):
#     __tablename__ = 'location'
#     pass

#https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
#https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html 
#https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#declarative-table-with-mapped-column
class Staff(Base):
    __tablename__ = 'staff'
    staff_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey('department.department_id'), nullable=False)
    email_address = Column(String, nullable=False)
    # timestamp columns 
    #https://docs.sqlalchemy.org/en/20/core/defaults.html#client-invoked-sql-expressions
    # created_at = Column(DateTime, default=func.now()) # add created at column
    last_updated = Column(DateTime, default=func.now()) 
    created_at = Column(DateTime, default=func.now()) # add created at column
    last_updated = Column(DateTime, default=func.now()) # add last updated column
# Drop and create tables
# https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.drop_all
# https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all

# metadata holds information about all the ORM-mapped tables declared 
#https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.MetaData
try:
    Base.metadata.drop_all(pg8000engine)  #drop all the know tables to Base.metadata
    Base.metadata.create_all(pg8000engine) # create all the know tables to Base.metadata
except SQLAlchemyError as e:
    print("Failed to drop and create tables:", e)
    raise

# SET UP SESSION
#https://docs.sqlalchemy.org/en/20/orm/session_basics.html
#https://docs.sqlalchemy.org/en/20/orm/quickstart.html#create-objects-and-persist
#https://www.youtube.com/watch?v=529LYDgRTgQ&t=2287s&ab_channel=NeuralNine

Session = sessionmaker(pg8000engine)
session = Session()

# FAKE DATA
fake = Faker()


# add x departments names

def creating_departments(): 
    departments = [
        Department(department_id=1, department_name="Human Resources"),
        Department(department_id=2, department_name="Finance"),
        Department(department_id=3,department_name="Marketing"),
        Department(department_id=4,department_name="Research & Development")
    ]

    session.add_all(departments)
    session.commit()
    return departments

#https://faker.readthedocs.io/
#add staff 
## loop? for each entry add this
#https://docs.sqlalchemy.org/en/14/orm/query.html

departments = session.query(Department).all() # fetchin all the rows
def creating_staff(departments):
     
    for _ in range(200):
        # random department https://docs.python.org/3/library/random.html
        # create staff member 
        dept = random.choice(departments)
        staff = Staff(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            department_id=dept.department_id,
            email_address=fake.email(),
        )
        session.add(staff)
    session.commit()
    return staff 



# CLOSE SESSION
session.close()