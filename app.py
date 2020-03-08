import datetime

from flask import request, abort
from flask_jwt_extended import create_access_token

from models import User
from extensions import db, app, api
from resources.coupons import CouponResource, CouponListResource

api.add_resource(CouponResource, '/api/v1/coupons/<int:coupon_id>')
api.add_resource(CouponListResource, '/api/v1/coupons')


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
