from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
#import psycopg2

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "hjshjhdjah kjshkjdhjs"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    #sprobowac z comman line
   # app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://ewmogiki:7yNQB1LV91KX3PYvbrTGyJ_tbkwzq4Nt@surus.db.elephantsql.com/ewmogiki"
   # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
   #czemu mi ni daiała z postgresem?? dodadac connection do rabbita
  # cur = con.cursor()
    db.init_app(app)


    from .views import views
    from .auth import auth
   # from .plotting import plotting


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Measurement, Plot # importujemy, zeby zdefiniowa te klasy opisane w models.py

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
        db.create_all(app=app)
        print('Created Database!')

