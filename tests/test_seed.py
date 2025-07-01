import pytest
import os

from src.seed import Staff, Base, Department, pg8000engine
from src.utils import init_engine 
from unittest.mock import patch
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import datetime

class TestConnection:
    #replace the real functions with mock objects 
    #https://docs.python.org/3/library/unittest.mock.html 
    #https://realpython.com/python-mock-library/
    # order matters!
    @patch("src.utils.sqlalchemy_create_engine")
    @patch("os.remove")
    @patch("os.path.exists")
    def test_db_is_initialised(self, mock_exists, mock_remove, mock_create_engine):

        mock_exists.return_value = True # forcing to return true - file exists
        
        if os.path.exists("my_db.db"):
            os.remove("my_db.db") # no actual file is deleted

        # engine is created
        #sqlalchemy.create_engine("postgresql+pg8000://postgre:password@localhost/mydatabase", echo=True)
        init_engine("postgresql+pg8000://postgre:password@localhost/mydatabase", echo=True)

        mock_exists.assert_called_once_with("my_db.db") #check for the file’s existence.
        mock_remove.assert_called_once_with("my_db.db") #check if the file is removed
        mock_create_engine.assert_called_once_with("postgresql+pg8000://postgre:password@localhost/mydatabase",
            echo=True #check if the engine is created
        )

    @patch("src.utils.sqlalchemy_create_engine")
    @patch("os.remove")
    @patch("os.path.exists")
    def test_error_engine_not_created(self, mock_exists, mock_remove, mock_create_engine):
        mock_exists.return_value = False
        mock_create_engine.side_effect = SQLAlchemyError("Mocked connection error")

        with pytest.raises(SQLAlchemyError, match="Mocked connection error"):
            init_engine("postgresql+pg8000://postgre:password@localhost/mydatabase", echo=True)

class TestStaff:
    # Create fixture for connection 
    @pytest.fixture
    def session(self):
        # Create SQLite database
        # engine = create_engine("sqlite:///:memory:")
        # session  https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.sessionmaker
        engine = create_engine("postgresql+pg8000://postgres:password@localhost/mydatabase")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        return Session() 

    def test_create_staff(self, session):

        # Create department from Department class
        department = Department(department_id=1, department_name="Engineering") 
        session.add(department) 

        # Create and add a staff instance
        staff = Staff(
            first_name="Camilla",
            last_name="Bertini",
            department_id=1,
            email_address="camillabertini@fakemail.com"
        )
        session.add(staff)
        session.commit()

        # session query SELECT and returns first row
        #https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.first 
        saved = session.query(Staff).first()

        # Checking if data has been entered correctly
        assert saved.first_name == "Camilla"
        assert saved.last_name == "Bertini"
        assert saved.department_id == 1
        assert saved.email_address == "camillabertini@fakemail.com"

        # checking right data type
        assert isinstance(saved.first_name, str)
        assert isinstance(saved.last_name, str)
        assert isinstance(saved.department_id, int)
        assert isinstance(saved.email_address, str)

        # checking timestamps are created
        assert isinstance(saved.created_at, datetime.datetime)
        assert isinstance(saved.last_updated, datetime.datetime)

