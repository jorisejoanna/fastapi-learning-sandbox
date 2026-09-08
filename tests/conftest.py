"""
conftest.py is a special file that Pytest automatically recognizes to set up test configurations
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base
from day12_main import app, get_db

#1. in-memory SQLite database URL (lives strictly in RAM!!!)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"      

#2. SQLite engine with StaticPool (allows multi-threaded test access to RAM DB)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#3. PYTEST FIXTURE: runs automatically for each test function
@pytest.fixture(scope="function")
def client():
    
    #A. create all tables fresh in RAM SQLite
    Base.metadata.create_all(bind=engine)   

    #B. dependency override: force FastAPI to use our RAM SQLite instead of Neon!!!
    def override_get_db():
        db =TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    #C. yield the test client to the test function
    with TestClient(app) as test_client:
        yield test_client

    #D. tear down: wipe all tables in RAM after the test finishes wooohooo!
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

