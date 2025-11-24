# test_db_factory.py
import pytest
from sqlalchemy.exc import OperationalError
from db_factory import get_db

def test_returns_session_object():
    session = db_factory()
    assert hasattr(session, "query")  # SQLAlchemy Session has .query

def test_in_memory_sqlite_can_execute():
    session = db_factory()
    result = session.execute("SELECT 1").scalar()
    assert result == 1

def test_custom_uri_respected(tmp_path):
    db_file = tmp_path / "test.db"
    uri = f"sqlite:///{db_file}"
    session = db_factory(uri)
    # Should create a file-backed SQLite DB
    session.execute("CREATE TABLE test (id INTEGER)")
    assert db_file.exists()

def test_invalid_uri_raises():
    with pytest.raises(OperationalError):
        # bogus URI should fail
        db_factory("sqlite:///nonexistent/path/to/db.sqlite").execute("SELECT 1")
