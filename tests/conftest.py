# to set up test enviroment - coś co się będzie wykonywać przed każdym testem

import pytest

from website import create_app, db

@pytest.fixture()
def app():
  #  app = create_app("sqlite:///database2.db") #tworze pamieć a nie nowa baze danych ???ale czemu nie dziala
    app = create_app()
   # app = create_app("sqlite://")

    with app.app_context():
        db.create_all()

    yield app #wszystko co sie dzieje przed jest ustawieniem do testu

@pytest.fixture()
def client(app): ## client jest argumentem, parametrem
    return app.test_client() #umozliwia symulowanie zapytania do aplikacji 