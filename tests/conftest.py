import pytest

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from application import create_app
from application import db

@pytest.fixture(scope='session', autouse=True)
def app():
    app = create_app('test')
    return app


@pytest.fixture(scope='session', autouse=True)
def session(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    return session


@pytest.fixture(scope='function', autouse=True)
def test_client(app):
    return app.test_client()


@pytest.fixture(scope='function', autouse=True)
def teardown(session):
    session.execute('DELETE FROM partner')
    session.commit()
