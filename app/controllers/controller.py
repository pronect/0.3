from flask import request, jsonify

from app import app, db
from app.models.user import User


@app.route('/api/ping', methods=['POST'])
def ping():
    return request.form


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
    if exists:
        result = select.balance - select.hold - money
        if result > 0 and select.status is True:
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
