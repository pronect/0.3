from app import app
import app.controllers.controller as api

api.ping
api.add
api.substract
api.status
api.add_user


@app.route('/')
def welcome():
    return """service is alive"""

if __name__ == "__main__":
    app.run(debug=True)
