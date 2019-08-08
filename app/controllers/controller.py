from app import app, db
from app.models.user import User
from flask import request, jsonify, abort


@app.route('/api/test', methods=['POST'])
def api_format_source():
    request.get_json()
    print(request.get_json())
    if request.json is None:
        abort(400)
    return jsonify(request.get_json())


@app.route('/api/test2', methods=['POST'])
def api():
    data = request.get_json()
    print(data)
    select = User.query.filter_by(id=data['client_id']).first()
    data2 = {
        'id': select.id,
        'name': select.name
    }
    return jsonify(data2)


@app.route('/api/ping', methods=['POST'])
def ping():
    fields = [k for k in request.form]
    values = [request.form[k] for k in request.form]
    data = dict(zip(fields, values))
    return jsonify(data)


@app.route('/api/add', methods=['POST'])
def add():
    client_id = request.form.get('client_id')
    money = float(request.form.get('money'))
    select = User.query.filter_by(id=client_id).first()
    exists = db.session.query(User.id).filter_by(id=client_id).scalar() is not None
    if exists and select.status:
        data = {
            'status': '200',
            'result': 'true',
            'addition': {
                'id:': select.id,
                'ФИО:': select.name,
                'Текущий баланс:': select.balance,
                'Статус счета:': select.status,
                'Сумма операции:': money,
            },
            'description': 'Пополнение баланса',
        }
        select.balance = select.balance + money
        db.session.commit()
        return jsonify(data)
    return jsonify({'description': 'Счет закрыт или пользователь не существует'})


@app.route('/api/substruct', methods=['POST'])
def substract():
    client_id = request.form.get('client_id')
    money = float(request.form.get('money'))
    select = User.query.filter_by(id=client_id).first()
    exists = db.session.query(User.id).filter_by(id=client_id).scalar() is not None
    result = select.balance - select.hold - money
    if exists and result > 0 and select.status is True:
        select.hold = select.hold + money
        db.session.commit()
        data = {
            'status': '200',
            'result': 'true',
            'addition': {
                'id:': select.id,
                'ФИО:': select.name,
                'Баланс:': select.balance,
                'Статус счета:': select.status,
                'Сумма операции:': money,
            },
            'description': 'Уменьшение баланса',
        }
        return jsonify(data)
    return jsonify({'description': 'Счет закрыт или пользователь не существует'})


@app.route('/api/status', methods=['POST'])
def status():
    client_id = request.form.get('client_id')
    exists = db.session.query(User.id).filter_by(id=client_id).scalar() is not None
    if exists and client_id:
        select = User.query.filter_by(id=client_id).first()
        data = {
            'status': '200',
            'result': 'true',
            'addition': {
                'Баланс:': select.balance,
                'Статус счета:': select.status
            },
            'description': 'Остаток по балансу, открыт счет или закрыт',
        }
        return jsonify(data)
    return jsonify({'info': 'Не указан id клиента, либо пользваотель не существует'})


# добавляет нового клиента в базу
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
