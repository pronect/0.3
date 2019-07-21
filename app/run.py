from app.controllers.controller import app


@app.route('/')
def welcome():
    return """service is alive"""


if __name__ == "__main__":
    app.run(debug=True)
