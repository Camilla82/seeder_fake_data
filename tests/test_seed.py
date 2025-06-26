import pytest
import os

from unittest.mock import patch
import sqlalchemy
from sqlalchemy import create_engine


class TestConnection:
    #replace the real functions with mock objects 
    @patch("sqlalchemy.create_engine")
    @patch("os.remove")
    @patch("os.path.exists")

    #test method that checks your database setup logic
    def test_db_is_initialised(self, mock_exists, mock_remove, mock_create_engine):

        
        mock_exists.return_value = True # forcing to return true - file exists
        
        if os.path.exists("my_db.db"):
            os.remove("my_db.db") # no actual file is deleted

        # engine is created
        sqlalchemy.create_engine("postgresql+pg8000://postgre:password@localhost/mydatabase", echo=True)

        mock_exists.assert_called_once_with("my_db.db") #check for the file’s existence.
        mock_remove.assert_called_once_with("my_db.db") #check if the file is removed
        mock_create_engine.assert_called_once_with("postgresql+pg8000://postgre:password@localhost/mydatabase",
            echo=True #check if the engine is created
        )

        
