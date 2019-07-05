import os

<<<<<<< HEAD
from app import app, db
=======
from app import app
from app import db
>>>>>>> 7d99597d12b8b8f420930826a7b67779dc9e8675

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')


<<<<<<< HEAD
=======

>>>>>>> 7d99597d12b8b8f420930826a7b67779dc9e8675
class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    hold = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"{self.id} {self.name} {self.balance} {self.hold} {self.status}"
<<<<<<< HEAD
=======


# user = User(id='9', name='test1', balance=1000, hold=0, status=1)
select = User.query.filter_by(id=4).first()
print(select.status)
>>>>>>> 7d99597d12b8b8f420930826a7b67779dc9e8675
