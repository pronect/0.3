from app import app, db
from app.models.user import User
from flask import request, jsonify, abort, json, make_response


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


def addition(id):
    """шаблон для json. возвращает всю строку из базы"""
    select = User.query.filter_by(id=id).first()
    return {
        "id": select.id,
        "name": select.name,
        "balance": select.balance,
        "hold": select.hold,
        "state": select.status,
    }


# def response_template(id):
#     select = User.query.filter_by(id=id).first()
#     return select.name
#
#
# @app.route('/api/test', methods=['POST'])
# def api_format_source():
#     request.get_json()
#     if request.get_json() is None:
#         abort(400)
#     return jsonify(request.get_json())

# для тестов
@app.route('/api/test2', methods=['POST'])
def api():
    d = make_response()
    data = request.get_json()
    response = app.response_class(
        response=json.dumps(data),
        status=400,
        mimetype='application/json'
    )
    response = jsonify(data)
    res = response.status_code = 200
    data = {
        "status": res
    }
    return (jsonify(data))


@app.route('/api/ping', methods=['POST'])
def ping():
    data = request.get_json()
    return jsonify(data)


@app.route('/api/add', methods=['POST'])
def add():
    data = request.get_json()
    id = data['id']
    money = data['money']
    money = round(float(money), 2)
    select = User.query.filter_by(id=id).first()
    exists = db.session.query(User.id).filter_by(id=id).scalar() is not None
    if exists and select.status:
        select.balance = select.balance + money
        db.session.commit()
        data = {
            'status': '200',
            'result': 'true',
            'addition': addition(id),
            'description': 'add balance',
        }
        return jsonify(data)
    return jsonify({'description': 'Счет закрыт или пользователь не существует'})


@app.route('/api/subtract', methods=['POST'])
def substract():
    data = request.get_json()
    id = data['id']
    money = data['money']
    money = round(float(money), 2)
    select = User.query.filter_by(id=id).first()
    exists = db.session.query(User.id).filter_by(id=id).scalar() is not None
    result = select.balance - select.hold - money
    if exists and result > 0 and select.status is True:
        select.hold = select.hold + money
        db.session.commit()
        data = {
            'status': '200',
            'result': 'true',
            'addition': addition(id),
            'description': 'subtract balance',
        }
        return jsonify(data)
    return jsonify({'description': 'Счет закрыт или пользователь не существует'})


@app.route('/api/status', methods=['POST'])
def status():
    data = request.get_json()
    id = data['id']
    exists = db.session.query(User.id).filter_by(id=id).scalar() is not None
    if exists and id:
        data = {
            'status': '200',
            'result': 'true',
            'addition': addition(id),
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
