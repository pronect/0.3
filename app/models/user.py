import os

from app import app
from app import db

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'new.db')


class User(db.Model):
    id = db.Column(db.String, unique=True, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    hold = db.Column(db.Float, nullable=False)
    status = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"{self.id} {self.name} {self.balance} {self.hold} {self.status}"
