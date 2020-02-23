from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.Config')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)


from models import User, Item, Order, Coupon


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/<name>')
def hello_name(name):
    return f'Hello {name}!'


if __name__ == '__main__':
    app.run()
