<<<<<<< HEAD
from flask import request, jsonify

from app import app, db
from app.models.user import User



@app.route('/api/ping', methods=['POST'])
def ping():
    return "Status OK"


@app.route('/api/add', methods=['POST'])
def add():
    client_id = request.form.get('client_id')
    money = request.form.get('money')
    select = User.query.filter_by(id=client_id).first()
    data = {'id': select.id,
            'name': select.name,
            'balance': select.balance
            }
    if select.status:
        select.balance += int(money)
        db.session.commit()
        return jsonify(data)
    else:
        return jsonify({'счет закрыт': 'none'})


@app.route('/api/substruct', methods=['POST'])
def substract():
    client_id = request.form.get('client_id')
    money = request.form.get('money')
    select = User.query.filter_by(id=client_id).first()
    result = select.balance - select.hold - int(money)
    if result > 0:
        select.balance -= int(money)
        db.session.commit()
        data = {'id': select.id,
                'name': select.name,
                'balance': select.balance
                }
        return jsonify(data)
    else:
        return jsonify({
            'none': 'операция не возможна',
            'select': select.balance,
            'hold': select.hold,
            'операция': money})


@app.route('/api/status', methods=['POST'])
def status():
    client_id = request.form.get('client_id')
    if client_id:
        select = User.query.filter_by(id=client_id).first()
        data = {
            'id': select.id,
            'name': select.name,
            'balance / hold': [select.balance, select.hold],
            'account status': select.status,
        }
        return jsonify(data)
    else:
        return jsonify({'None': 'None'})


@app.route('/api/add_user', methods=['POST'])
def add_user():
    client_id = request.form.get('client_id')
    name = request.form.get('name')
    balance = request.form.get('balance')
    hold = request.form.get('hold')
    state = request.form.get('state')
    user = User(id=int(client_id), name=str(name), balance=int(balance), hold=int(hold), status=bool(state))
    db.session.add(user)
    db.session.commit()
    return 'done'
=======
from app import db
from app.models.user import User

u1 = User(id='26c940a1-7228-4ea2-a3bc-e6460b172040', name='Бессонов Дмитрий', balance='1000', hold='0', status=1)
db.session.add(u1)
db.session.commit()
>>>>>>> 7d99597d12b8b8f420930826a7b67779dc9e8675
