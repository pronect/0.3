import time

from app import db
from app.models.user import User

# Получаем список id всех клиентов
session = db.session
lst = session.query(User.id).all()
ids = []
for id in lst:
    ids.append(id[0])


# Вычет суммы hold из баланса клиента
def subhold():
    for id in ids:
        select = User.query.filter_by(id=id).first()
        if (select.balance - select.hold) >= 0 and select.status is True:
            select.balance = select.balance - select.hold
            select.hold = 0
            db.session.commit()


#while True:
#    time.sleep(10)
subhold()
