from flask import request, Response, jsonify
from jsonrpcserver import method, dispatch

from app import app, db
from app.models.user import User


# /api/ping (работоспособность сервиса)
@method
@app.route('/')
def ping():
    return "Status OK"


# /api/status (остаток по балансу, открыт счет или закрыт)
# >>> r = requests.post("http://127.0.0.1:5000/json")
# >>> r.json()
@method
@app.route('/json', methods=['GET', 'POST'])
def status():
    select = User.query.filter_by(id=1).first()
    data = {'id': select.id,
            'name': select.name,
            'balance / hold': [select.balance, select.hold],
            'account status': select.status}
    return jsonify(data)


# /api/status (остаток по балансу, открыт счет или закрыт)
# >>> r = requests.post("http://127.0.0.1:5000/json2", data={'id': 7})
# >>> r.json()
@app.route('/json2', methods=['GET', 'POST'])
def status2():
    if request.form.get('id'):
        select = User.query.filter_by(id=request.form.get('id')).first()
        data = {'id': select.id,
                'name': select.name,
                'balance / hold': [select.balance, select.hold],
                'account status': select.status}
        return jsonify(data)
    else:
        return jsonify({'None': 'None'})


# добавление пользователя в бд
# >>> r = requests.post("http://127.0.0.1:5000/add", data={'id': 14, 'name': 'test test', 'balance': 1000, 'hold': 0, 'status': '1'})
@app.route('/addUser', methods=['POST'])
def addUSer():
    id = request.form.get('id')
    name = request.form.get('name')
    balance = request.form.get('balance')
    hold = request.form.get('hold')
    status = request.form.get('status')
    # user = User(id='9', name='test1', balance=1000, hold=0, status=1)
    user = User(id=int(id), name=str(name), balance=int(balance), hold=int(hold), status=bool(status))
    db.session.add(user)
    db.session.commit()
    return 'done'


@app.route('/add', methods=['POST'])
def addMoney():
    id = request.form.get('id')
    money = request.form.get('money')
    select = User.query.filter_by(id=id).first()
    data = {'id': select.id,
            'name': select.name,
            'balance': select.balance
            }
    if select.status == True:
        select.balance += int(money)
        db.session.commit()
        return jsonify(data)
    else:
        return jsonify({'счет закрыт': 'none'})


@app.route('/substruct', methods=['POST'])
def subtruct():
    id = request.form.get('id')
    money = request.form.get('money')
    select = User.query.filter_by(id=id).first()
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


@app.route("/", methods=["POST"])
def index():
    req = request.get_data().decode()
    response = dispatch(req)
    return Response(str(response), response.http_status, mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True)
