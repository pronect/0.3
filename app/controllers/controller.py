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


@app.route('/api/ping', methods=['POST'])
def ping():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Invalid Content Type'}), 400

    data = request.get_json()
    return jsonify(data), 200


@app.route('/api/add', methods=['POST'])
def add():
    data = request.get_json()

    if request.content_type != 'application/json':
        return jsonify({'error': 'Invalid Content Type'}), 400

    if not all([data.get('id'), data.get('money')]):
        return jsonify({'error': 'Missing field/s (id, money)'}), 400

    id = data['id']
    money = float(data['money'])
    select = User.query.filter_by(id=id).first()

    if money != float("{0:.2f}".format(money)):
        return jsonify({'error': '2 decimal places'}), 400

    if db.session.query(User.id).filter_by(id=id).scalar() is None:
        return jsonify({'error': 'client unknown'}), 400

    if select.status is False:
        return jsonify({'error': 'account closed'}), 400

    select.balance = select.balance + money
    db.session.commit()
    data = {
        'status': '200',
        'result': 'true',
        'addition': addition(id),
        'description': 'add balance',
            }
    return jsonify(data), 200


@app.route('/api/subtract', methods=['POST'])
def substract():
    data = request.get_json()

    if request.content_type != 'application/json':
        return jsonify({'error': 'Invalid Content Type'}), 400

    if not all([data.get('id'), data.get('money')]):
        return jsonify({'error': 'Missing field/s (id, money)'}), 400

    id = data['id']
    money = float(data['money'])
    select = User.query.filter_by(id=id).first()

    if money != float("{0:.2f}".format(money)):
        return jsonify({'error': '2 decimal places'}), 400

    if db.session.query(User.id).filter_by(id=id).scalar() is None:
        return jsonify({'error': 'client unknown'}), 400

    if select.status is False:
        return jsonify({'error': 'account closed'}), 400

    if select.balance - select.hold - money < 0:
        return jsonify({'error': 'операция не возможна'}), 400

    select.hold = select.hold + money
    db.session.commit()
    data = {
        'status': '200',
        'result': 'true',
        'addition': addition(id),
        'description': 'subtract balance',
            }
    return jsonify(data), 200


@app.route('/api/status', methods=['POST'])
def status():
    data = request.get_json()

    if request.content_type != 'application/json':
        return jsonify({'error': 'Invalid Content Type'}), 400

    if not all([data.get('id')]):
        return jsonify({'error': 'Missing field/s (id)'}), 400

    if db.session.query(User.id).filter_by(id=data['id']).scalar() is None:
        return jsonify({'error': 'client unknown'}), 400

    data = {
        'status': '200',
        'result': 'true',
        'addition': addition(data['id']),
        'description': 'Остаток по балансу, открыт счет или закрыт',
            }
    return jsonify(data), 200



# добавляет нового клиента в базу
# @app.route('/api/add_user', methods=['POST'])
# def add_user():
#     client_id = request.form.get('client_id')
#     name = request.form.get('name')
#     balance = request.form.get('balance')
#     hold = request.form.get('hold')
#     state = request.form.get('state')
#     user = User(id=int(client_id), name=str(name), balance=int(balance), hold=int(hold), status=bool(state))
#     db.session.add(user)
#     db.session.commit()
#     return 'done'
