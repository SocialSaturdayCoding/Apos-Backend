import datetime

from flask import Flask, jsonify, request, abort
from flask_jwt_extended import create_access_token

app = Flask(__name__)
app.config.from_object('config.Config')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

from models import User, Item, Order, Coupon
from extensions import db

db.init_app(app)


@app.route('/api/v1/coupons', methods=['GET'])
def list_coupons():
    coupons = Coupon.query.all()
    return jsonify([coupon.serialize for coupon in coupons])


@app.route('/api/v1/coupons', methods=['PUT'])
def create_coupon():
    if not request.json:
        abort(400)
    if 'deliverer' not in request.json or type(request.json['deliverer']) != str:
        abort(400)
    if 'coupon' not in request.json or type(request.json['coupon']) != str:
        abort(400)
    coupon = Coupon(deliverer=request.json['deliverer'],
                    coupon=request.json['coupon'],
                    deadline=request.json.get('deadline', None),
                    creator_id=1)
    db.session.add(coupon)
    db.session.commit()
    return coupon.serialize, 201


@app.route('/api/v1/coupons/<int:coupon_id>', methods=['DELETE'])
def delete_coupon(coupon_id):
    coupon = Coupon.query.get(coupon_id)
    if not coupon:
        abort(404)
    db.session.delete(coupon)
    db.session.commit()
    return '', 204


@app.route('/api/v1/auth', methods=['POST'])
def auth():
    if not request.json:
        abort(400)
    if not (request.json['username'] and request.json['password']):
        abort(400)
    user = User.query.get(username=request.json['username'])
    if not user:
        abort(401)
    authorized = user.check_password(request.json['password'])
    if not authorized:
        abort(401)

    expires = datetime.timedelta(days=7)
    access_token = create_access_token(identity=str(user.id), expires_delta=expires)
    return {'token': access_token}, 200


@app.route('/api/v1/signup', methods=['POST'])
def signup():
    if not request.json:
        abort(400)
    if not (request.json['username'] and request.json['password']):
        abort(400)
    user = User(username=request.json['username'], password=request.json['password'])
    user.hash_password()
    user.save()
    return user.serialize, 201


if __name__ == '__main__':
    app.run()
