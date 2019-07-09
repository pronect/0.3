from flask import request, jsonify

from app import app, db
from app.models.user import User


@app.route('/api/ping', methods=['POST'])
def ping():
    data = {
        'status': 'http статус запроса',
        'result': 'true',
        'addition': 'none',
        'description': 'Работоспособность сервиса',
    }
    return jsonify(data)


@app.route('/api/add', methods=['POST'])
def add():
    client_id = request.form.get('client_id')
    money = int(request.form.get('money'))
    select = User.query.filter_by(id=client_id).first()
    data = {
        'status': '200',
        'result': 'true',
        'addition': {
            'id:': select.id,
            'ФИО:': select.name,
            'Баланс:': select.balance,
            'Статус счета:': select.status,
        },
        'description': 'пополнение баланса',
    }
    if select.status:
        select.balance += money
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
        data = {
            'status': '<200>',
            'result': 'true',
            'addition': {
                'id:': select.id,
                'ФИО:': select.name,
                'Баланс:': select.balance,
                'Статус счета:': select.status,
            },
            'description': 'уменьшение баланса',
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
            'status': '<http_status>',
            'result': '<bool:operation_status>',
            'addition': (select.balance, select.status),
            'description': 'остаток по балансу, открыт счет или закрыт',
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
