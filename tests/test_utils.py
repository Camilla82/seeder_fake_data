
import pytest
from sqlalchemy.exc import SQLAlchemyError
from unittest.mock import patch
from src.utils import init_engine

@patch("src.utils.sqlalchemy_create_engine")
def test_init_engine_success(mock_engine):
    mock_engine.return_value = "mock_engine"
    result = init_engine("mock-url", echo=False) # fake url
    assert result == "mock_engine"
    mock_engine.assert_called_once_with("mock-url", echo=False)

@patch("src.utils.sqlalchemy_create_engine") # replaces the sqlalchemy_create_engine function inside utils.py with a mock
def test_init_engine_failure(mock_engine):
    mock_engine.side_effect = SQLAlchemyError("Mocked failure") # when the mock is raised, do this
    with pytest.raises(SQLAlchemyError, match="Mocked failure"): # if the error is not raised, the test fails
        init_engine(db_url="mock-url")