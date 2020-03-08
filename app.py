import datetime

from flask import request, abort
from flask_jwt_extended import create_access_token

from models import User
from extensions import db, app, api
from resources.coupons import CouponResource, CouponListResource
from resources.auth import Auth, Signup

api.add_resource(CouponResource, '/api/v1/coupons/<int:coupon_id>')
api.add_resource(CouponListResource, '/api/v1/coupons')
api.add_resource(Auth, '/api/v1/auth')
api.add_resource(Signup, '/api/v1/signup')

if __name__ == '__main__':
    app.run()
