import pytest
import os
from unittest.mock import patch
from sqlalchemy import create_engine
import sqlalchemy

@patch("sqlalchemy.create_engine")
@patch("os.path.exists")
@patch("os.remove")
def test_db_is_initialised(mock_exists, mock_remove, mock_create_engine):

    # set up mocks

    mock_exists.return_value = True # my file exists
    
    if os.path.exists("my_db.db"):
        os.remove("my_db.db")

    sqlalchemy.create_engine("postgresql+pg8000://postgre:password@localhost/mydatabase", echo=True)

    mock_exists.assert_called_once_with("my_db.db")
    mock_remove.assert_called_once_with("my_db.db")
    mock_create_engine.assert_called_once_with("postgresql+pg8000://postgre:password@localhost/mydatabase",
        echo=True
    )

        
