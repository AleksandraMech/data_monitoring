from website import db #importowanie z current pacage(website) db-objectu
from flask_login import UserMixin
from sqlalchemy.sql import func


class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True) #unikalne identyfikowanie każdego obiektu
    values = db.Column(db.String(10000))
    file = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #patrzac na user_id możemy zobaczyć jaki user to stworzył
   # plot = db.relationship('Plot')
   


class Plot(db.Model):
    id = db.Column(db.Integer, primary_key=True) #unikalne identyfikowanie każdego obiektu
    values = db.Column(db.String(10000))
    measurement_id = db.Column(db.Integer, db.ForeignKey('measurement.id')) #patrzac na measurement_id możemy zobaczyć jaki measure to stworzył


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #relacja jedna do wielu (jeden user i wiele notatek); 


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True) #unique=true -zaden inny user nie może mieć takiego samego maila
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    measurement = db.relationship('Measurement')