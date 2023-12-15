from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
#import psycopg2

db = SQLAlchemy()
DB_NAME = "database.db"
#DB_NAME = "data_monitoring"


#def create_app():
def create_app(database_uri="sqlite:///database.db"):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "hjshjhdjah kjshkjdhjs"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
     #app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
     #psycopg2.connect(database="data_monitoring", user="postgres", password="albertina", host="localhost", port="5432")
     # conn = psycopg2.connect(database="data_monitoring", user="postgres", password="albertina", host="localhost", port="5432")
  # cur = con.cursor()
    db.init_app(app)


    from .views import views
    from .auth import auth
   # from .plotting import plotting


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Measurement, Graph # importujemy, zeby zdefiniowa te klasy opisane w models.py

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
       # db.create_all(app=app)
        db.create_all(app=app)
        print('Created Database!')

