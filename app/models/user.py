import os

from app import app
from app import db

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')



class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    hold = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"{self.id} {self.name} {self.balance} {self.hold} {self.status}"


# user = User(id='9', name='test1', balance=1000, hold=0, status=1)
select = User.query.filter_by(id=4).first()
print(select.status)