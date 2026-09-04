from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
import models
import pytest


TEST_DATABASE_URL = "sqlite:///./test_resolveDesk.db"


engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)


def setup_test_database():
    Base.metadata.create_all(bind=engine)


def teardown_test_database():
    Base.metadata.drop_all(bind=engine)



@pytest.fixture
def test_db():
    setup_test_database()

    yield TestingSessionLocal()

    teardown_test_database()