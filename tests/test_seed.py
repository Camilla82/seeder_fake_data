
import pytest 
import os
import re
import datetime
from unittest.mock import patch
from src.seed import Staff, Base, Department, creating_departments, creating_staff
from src.utils import init_engine
from sqlalchemy import text, create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from faker import Faker

fake = Faker()

@pytest.fixture
def session():
    # Create SQLite database
    # engine = create_engine("sqlite:///:memory:")
    # session  https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.sessionmaker
    engine = create_engine("postgresql+pg8000://postgres:password@localhost/mydatabase")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
        
    session.query(Staff).delete()
    session.commit()
    session.query(Department).delete()
    session.commit()

    # Reset the department_id sequence to 1
    session.execute(text("ALTER SEQUENCE department_department_id_seq RESTART WITH 1"))
    session.execute(text("ALTER SEQUENCE staff_staff_id_seq RESTART WITH 1"))
    session.commit()

    yield session
    session.close()

@pytest.fixture
def departments():
    return creating_departments()

@pytest.fixture
def staff(session, departments):
    return creating_staff(departments)

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
    def test_create_staff(self, session):
        department = Department(department_id=1, department_name="Engineering")
        session.add(department)

        staff = Staff(
            first_name="Camilla",
            last_name="Bertini",
            department_id=1,
            email_address="camillabertini@fakemail.com"
        )
        session.add(staff)
        session.commit()

        saved = session.query(Staff).first()

        assert saved.first_name == "Camilla"
        assert saved.last_name == "Bertini"
        assert saved.department_id == 1
        assert saved.email_address == "camillabertini@fakemail.com"
        assert isinstance(saved.created_at, datetime.datetime)
        assert isinstance(saved.last_updated, datetime.datetime)

class TestInsert:
    def test_if_departments_have_been_inserted_correctly(self, session):
        departments = [
            Department(department_name="Human Resources"),
            Department(department_name="Finance"),
            Department(department_name="Marketing"),
            Department(department_name="Research & Development")
        ]
        session.add_all(departments)
        session.commit()

        result = session.query(Department).all()

        assert len(result) == 4
        assert result[0].department_name == "Human Resources"
        assert result[1].department_name == "Finance"
        assert result[2].department_name == "Marketing"
        assert result[3].department_name == "Research & Development"

    def test_inserting_200_fake_staff_entries(self, session, staff):
        query = session.query(Staff).all()
        assert len(query) == 200, "Expected 200 staff entries"

        email_regex = r"[^@]+@[^@]+\.[^@]+"

        for person in query:
            assert isinstance(person, Staff)
            assert isinstance(person.first_name, str)
            assert isinstance(person.last_name, str)
            assert isinstance(person.department_id, int)
            assert isinstance(person.email_address, str) and re.match(email_regex, person.email_address)