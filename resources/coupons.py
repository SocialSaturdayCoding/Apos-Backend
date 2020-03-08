from datetime import datetime

from flask_restful import Resource, abort, reqparse

from extensions import db
from models import Coupon

parser = reqparse.RequestParser()
parser.add_argument('deliverer', type=str, required=True)
parser.add_argument('coupon', type=str, required=True)
parser.add_argument('deadline', type=datetime.utcfromtimestamp)


class CouponListResource(Resource):
    def get(self):
        coupons = Coupon.query.all()
        return [coupon.serialize for coupon in coupons]

    def put(self):
        args = parser.parse_args()
        coupon = Coupon(deliverer=args['deliverer'],
                        coupon=args['coupon'],
                        deadline=args['deadline'],
                        creator_id=1)
        db.session.add(coupon)
        db.session.commit()
        return coupon.serialize, 201


class CouponResource(Resource):
    def delete(self, coupon_id):
        coupon = Coupon.query.get(coupon_id)
        if not coupon:
            abort(404, message=f"Coupon {coupon_id} does not exist")
        db.session.delete(coupon)
        db.session.commit()
        return '', 204
