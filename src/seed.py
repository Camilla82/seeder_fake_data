from src.utils import init_engine
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Numeric, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from faker import Faker
import os 

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

# SET UP FAKER

fake = Faker()

# INSERT DATA FOR EACH TABLE WITH FAKER



# CLOSE SESSION

